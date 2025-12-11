import requests
import time
import pytz
from datetime import datetime
from db import db
from models.submission import Submission
from models.submissions_answer import SubmissionAnswer
from models.testcase_result import TestcaseResult
from models.language import Language
from models.testcase import Testcase
from models.solved_problem import SolvedProblem
from models.problem import Problem
from models.submissions_answer import ModeEnum
from models.user import User

JUDGE0_URL = "http://16.171.168.56:2358" 
POLL_TIMEOUT = 300  # 5 minutes max polling time
POLL_INTERVAL = 1   # Poll every 1 second
IST = pytz.timezone('Asia/Kolkata')


def convert_to_ist(utc_dt):
    """Convert UTC datetime to IST"""
    if utc_dt is None:
        return None
    if utc_dt.tzinfo is None:
        utc_dt = pytz.utc.localize(utc_dt)
    return utc_dt.astimezone(IST).isoformat()

def fetch_submissions_of_user_for_problem(user_id: int, problem_id: int):
    submissions = Submission.query.filter_by(user_id=user_id, problem_id=problem_id).all()
    
    submissions_data = []
    submission_answers = []

    for sub in submissions:
        submissions_data.append({
            "id": sub.id,
            "user_id": sub.user_id,
            "problem_id": sub.problem_id,
            "status": sub.status,
            "created_at": convert_to_ist(sub.created_at),
        })

        sub_ans = SubmissionAnswer.query.filter_by(submission_id=sub.id).first()
        if sub_ans:
            lang = Language.query.filter_by(id=sub_ans.language_id).first()
            submission_answers.append({
                "id": sub_ans.id,
                "submission_id": sub_ans.submission_id,
                "code": sub_ans.code,
                "language_id": sub_ans.language_id,
                "language_name": lang.name if lang else None,
                "totalExecTime": sub_ans.totalExecTime,
                "totalExecMemory": sub_ans.totalExecMemory,
                "status": sub_ans.status,
                "mode": sub_ans.mode,
                "created_at": convert_to_ist(sub_ans.created_at)
            })
    
    return {
        "submissions": submissions_data,
        "submission_answers": submission_answers
    }


def fetch_submissions_of_user(user_id: int):
    submissions = Submission.query.filter_by(user_id=user_id).all()
    submissions_data = []
    for sub in submissions:
        submissions_data.append({
            "id": sub.id,
            "user_id": sub.user_id,
            "problem_id": sub.problem_id,
            "status": sub.status,
            "created_at": convert_to_ist(sub.created_at),
        })
    
    return submissions_data


def create_new_submission(data):
    """
    Expects data:
    {
      "user_id": int,
      "problem_id": int,
      "source_code": str,
      "language_name": str,
      "mode": "Submit" or "Run"   # optional
    }
    
    Only stores data in DB after Judge0 completes execution.
    """

    # --- 1) Validate / extract ---
    user_id = data.get("user_id")
    problem_id = data.get("problem_id")
    source_code = data.get("source_code")
    language_name = data.get("language_name")
    mode = data.get("mode", "Submit")

    if not all([user_id, problem_id, source_code, language_name]):
        raise Exception("Missing required fields (user_id, problem_id, source_code, language_name)")

    # Validate language
    language_obj = Language.query.filter_by(name=language_name).first()
    if not language_obj:
        raise Exception(f"Invalid language name: {language_name}")
    judge0_lang_id = language_obj.compiler_language_id

    # Validate problem and get testcases
    problem = Problem.query.get(problem_id)
    if not problem:
        raise Exception(f"Problem not found: {problem_id}")
    
    testcases = Testcase.query.filter_by(problem_id=problem_id).order_by(Testcase.order).all()
    if not testcases:
        raise Exception(f"No testcases found for problem: {problem_id}")

    # --- 2) Prepare Judge0 batch payload ---
    submissions_payload = [
        {
            "source_code": source_code,
            "language_id": judge0_lang_id,
            "stdin": tc.input_data,
            "expected_output": tc.expected_output
        }
        for tc in testcases
    ]

    # --- 3) Send batch to Judge0 ---
    try:
        resp = requests.post(
            f"{JUDGE0_URL}/submissions/batch?base64_encoded=false",
            json={"submissions": submissions_payload},
            timeout=30
        )
        resp.raise_for_status()
        batch = resp.json()
        
        if not batch or not isinstance(batch, list):
            raise Exception("Invalid response from Judge0")
        
        tokens = [s['token'] for s in batch]
        
        if not tokens:
            raise Exception("No tokens received from Judge0")
            
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to submit to Judge0: {str(e)}")

    # --- 4) Poll until all finished with timeout ---
    start_time = time.time()
    results = None
    
    while True:
        # Check timeout
        if time.time() - start_time > POLL_TIMEOUT:
            raise Exception("Submission timed out waiting for Judge0")
        
        try:
            poll = requests.get(
                f"{JUDGE0_URL}/submissions/batch",
                params={"tokens": ",".join(tokens), "base64_encoded": "false"},
                timeout=30
            )
            poll.raise_for_status()
            results = poll.json()
            
            # Check if all finished (status.id not in [1=In Queue, 2=Processing])
            if results and 'submissions' in results:
                if all(r["status"]["id"] not in (1, 2) for r in results['submissions']):
                    break
                    
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to poll Judge0: {str(e)}")
        
        time.sleep(POLL_INTERVAL)

    # --- 5) Validate results ---
    if not results or 'submissions' not in results:
        raise Exception("Invalid results from Judge0")
    
    if len(results['submissions']) != len(testcases):
        raise Exception("Mismatch between testcases and results")

    # --- 6) Aggregate totals and determine overall status ---
    # Convert: time from seconds to milliseconds, memory from KB to MB
    total_time = 0.0
    total_memory = 0.0
    max_time = 0.0
    max_memory = 0.0
    overall_status = "AC"  # Accepted
    testcase_count = len(results["submissions"])
    
    for r in results["submissions"]:
        # Add execution metrics (convert s->ms and KB->MB)
        time_in_seconds = float(r.get("time") or 0)
        memory_in_kb = float(r.get("memory") or 0)
        
        time_ms = time_in_seconds * 1000  # Convert seconds to milliseconds
        memory_mb = memory_in_kb / 1024   # Convert KB to MB
        
        total_time += time_ms
        total_memory += memory_mb
        max_time = max(max_time, time_ms)
        max_memory = max(max_memory, memory_mb)
        
        # Check if not accepted (Judge0 status 3 = Accepted)
        if r["status"]["id"] != 3:
            overall_status = r["status"]["description"]
            # Don't break - continue to calculate total time/memory
    
    avg_time = total_time / testcase_count if testcase_count > 0 else 0
    avg_memory = total_memory / testcase_count if testcase_count > 0 else 0

    # --- 7) NOW store everything in DB (only after completion) ---
    try:
        # Create Submission record with final status
        submission = Submission(
            user_id=user_id, 
            problem_id=problem_id, 
            status=overall_status
        )
        db.session.add(submission)
        db.session.flush()  # Get submission.id without committing

        # Store SubmissionAnswer
        mode_enum = ModeEnum.Submit if mode.lower() == "submit" else ModeEnum.Run
        submission_answer = SubmissionAnswer(
            submission_id=submission.id,
            code=source_code,
            language_id=language_obj.id,
            totalExecTime=total_time,
            totalExecMemory=total_memory,
            status=overall_status,
            mode=mode_enum
        )
        db.session.add(submission_answer)

        # Store TestcaseResults
        for tc, res in zip(testcases, results["submissions"]):
            time_in_seconds = float(res.get("time") or 0)
            memory_in_kb = float(res.get("memory") or 0)
            
            tc_result = TestcaseResult(
                problem_id=problem_id,
                submission_id=submission.id,
                testcase_id=tc.id,
                status=res["status"]["description"],
                execTime=time_in_seconds * 1000,  # Convert to milliseconds
                execMemory=memory_in_kb / 1024,   # Convert to MB
                expected_output=tc.expected_output,
                error_message=(res.get("stderr") or res.get("compile_output") or "")
            )
            db.session.add(tc_result)

        # --- 8) If accepted, handle SolvedProblem and XP ---
        if overall_status == "AC":
            existing = SolvedProblem.query.filter_by(
                user_id=user_id, 
                problem_id=problem_id
            ).first()
            
            if not existing:
                xp_gain = getattr(problem, "xp", 0) or 0
                solved = SolvedProblem(
                    user_id=user_id,
                    problem_id=problem_id,
                    xp_earned=xp_gain,
                    tookAIHelp=False
                )
                db.session.add(solved)

                # Update user's total XP
                user = User.query.get(user_id)
                if user:
                    user.total_xp = (user.total_xp or 0) + xp_gain

        # Commit all changes at once
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        raise Exception(f"Failed to store submission data: {str(e)}")

    # --- 9) Return structured response ---
    return {
        "submission_id": submission.id,
        "submission_status": overall_status,
        "total_time": total_time,  # in milliseconds (SUM - actual time taken)
        "avg_time": avg_time,  # in milliseconds (per test case)
        "max_time": max_time,  # in milliseconds (slowest test case)
        "total_memory": total_memory,  # in MB (SUM)
        "avg_memory": avg_memory,  # in MB (per test case)
        "max_memory": max_memory,  # in MB (highest memory usage)
        "testcase_count": testcase_count,
        "testcase_results": [
            {
                "testcase_id": tc.id,
                "status": res["status"]["description"],
                "time": float(res.get("time") or 0) * 1000,  # milliseconds
                "memory": float(res.get("memory") or 0) / 1024  # MB
            }
            for tc, res in zip(testcases, results["submissions"])
        ]
    }