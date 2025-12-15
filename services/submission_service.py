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
import time
import math

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
                # "mode": sub_ans.mode.value,
                "created_at": convert_to_ist(sub_ans.created_at)
            })


        submissions_data.append({
            "id": sub.id,
            "user_id": sub.user_id,
            "problem_id": sub.problem_id,
            "status": sub.status,
            "created_at": convert_to_ist(sub.created_at),
            "totalExecTime": sub_ans.totalExecTime,
            "totalExecMemory": sub_ans.totalExecMemory,
            "language_name": sub_ans.language_name
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
    Stops execution early if any test case fails in Submit mode.
    """

    print("dataaaaa:", data)

    # --- 1) Validate / extract ---
    user_id = data.get("user_id")
    problem_id = data.get("problem_id")
    source_code = data.get("source_code")
    language_name = data.get("language_name")
    mode = data.get("mode", "Submit")

    print('modeeeee:', mode)

    lang_obj = Language.query.filter_by(name=language_name.lower()).first()
    judge0_lang_id = lang_obj.compiler_language_id
    print(judge0_lang_id)

    if(mode.lower() == "run"):
        testcases = Testcase.query.filter_by(problem_id=problem_id, isHidden=False)
    else:
        testcases = Testcase.query.filter_by(problem_id=problem_id)

    submissions_data = [
        {
            "source_code": source_code,
            "language_id": judge0_lang_id,
            "stdin": tc.input_data,
            "expected_output": tc.expected_output
        }
        for tc in testcases
    ]

    submission_results = []
    batch_size = 50
    early_exit = False  # Flag to stop processing remaining batches
    failed_status = None  # Store the failed status

    for i in range(math.ceil(len(submissions_data)/batch_size)):
        
        if early_exit and mode.lower() == "submit":
            # Skip remaining batches if we already found a failure
            break

        batch_post_res = requests.post(
            url=f"{JUDGE0_URL}/submissions/batch?base64_encoded=false&wait=false",
            json={"submissions": submissions_data[50*i: 50*(i+1)]}
        )

        print(f"batch resssssss : {i} : ", batch_post_res.json())

        submission_results_batch = []

        for token_obj in batch_post_res.json():

            token = token_obj['token']

            while True:

                get_res = requests.get(
                    url=f"{JUDGE0_URL}/submissions/{token}?base64_encoded=false"
                )

                result = get_res.json()
                
                # Check if processing is complete (not queued or processing)
                if(result['status']['id'] not in [1, 2]):
                    submission_results_batch.append(result)
                    
                    # CHECK FOR EARLY EXIT IN SUBMIT MODE
                    if mode.lower() == "submit" and result["status"]['id'] != 3:
                        early_exit = True
                        failed_status = result["status"]["description"]
                        print(f"Test case failed with status: {failed_status}. Stopping further execution.")
                    
                    break
                
                time.sleep(0.1)
            
            # Break out of token loop if we found a failure in Submit mode
            if early_exit and mode.lower() == "submit":
                break

        submission_results.extend(submission_results_batch)
        
        # Break out of batch loop if we found a failure in Submit mode
        if early_exit and mode.lower() == "submit":
            break

    print(submission_results)

    # --- Calculate metrics based on results we have ---
    total_time = 0.0
    total_memory = 0.0
    max_time = 0.0
    max_memory = 0.0
    overall_status = "AC"  # Accepted
    testcase_count = len(submission_results)
    
    for r in submission_results:
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

    avg_time = total_time / testcase_count if testcase_count > 0 else 0
    avg_memory = total_memory / testcase_count if testcase_count > 0 else 0

    # --- Store everything in DB (only after completion) ---
    try:
        # Create Submission record with final status
        submission = Submission(
            user_id=user_id, 
            problem_id=problem_id, 
            status=overall_status,
            total_exec_time=total_time,
            total_exec_memory=total_memory,
            language_name=language_name
        )
        db.session.add(submission)
        db.session.flush()  # Get submission.id without committing

        # Store SubmissionAnswer
        submission_answer = SubmissionAnswer(
            submission_id=submission.id,
            code=source_code,
            language_id=lang_obj.id,
            totalExecTime=total_time,
            totalExecMemory=total_memory,
            status=overall_status,
            mode=mode.capitalize()
        )
        db.session.add(submission_answer)

        # Store TestcaseResults (only for test cases that were executed)
        executed_testcases = list(testcases)[:len(submission_results)]
        for tc, res in zip(executed_testcases, submission_results):

            print(res)

            time_in_seconds = float(res.get("time") or 0)
            memory_in_kb = float(res.get("memory") or 0)
            
            tc_result = TestcaseResult(
                problem_id=problem_id,
                submission_id=submission.id,
                testcase_id=tc.id,
                status=res["status"]["description"],
                execTime=time_in_seconds * 1000,  # Convert to milliseconds
                execMemory=memory_in_kb / 1024,   # Convert to MB
                expected_output=res.get("stdout") or "No stdout",
                error_message=(res.get("stderr") or res.get("compile_output") or "")
            )
            db.session.add(tc_result)

        # --- If accepted, handle SolvedProblem and XP ---
        if overall_status == "AC":
            existing = SolvedProblem.query.filter_by(
                user_id=user_id, 
                problem_id=problem_id
            ).first()
            
            if not existing:
                xp_gain = Problem.query.get(problem_id).xp_reward
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

    # --- Return structured response ---
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
        "executed_testcase_count": len(submission_results),  # May be less than total if early exit
        "testcase_results": [
            {
                "testcase_id": tc.id,
                "status": res["status"]["description"],
                "time": float(res.get("time") or 0) * 1000,  # milliseconds
                "memory": float(res.get("memory") or 0) / 1024,  # MB
                "output": res.get("stdout") or ""
            }
            for tc, res in zip(list(testcases)[:len(submission_results)], submission_results)
        ]
    }