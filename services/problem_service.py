from models.problem import Problem, DifficultyEnum
from models.editorial import Editorial
from models.hint import Hint
from models.constraint import Constraint
from models.snippet import Snippet
from models.problem_tag import ProblemTag
from models.tag import Tag
from models.language import Language
from models.testcase import Testcase
from models.submission import Submission
from models.solved_problem import SolvedProblem
from sqlalchemy.orm import joinedload, selectinload
from db import db
from data import get_data
import time
import random
from collections import Counter
from sqlalchemy.orm import joinedload
from sqlalchemy import func
import random

def fetch_all_problems(user_id):
    solved_ids = {
        s.problem_id
        for s in SolvedProblem.query
            .filter_by(user_id=user_id)
            .with_entities(SolvedProblem.problem_id)
            .all()
    }

    problems = Problem.query.options(
        selectinload(Problem.tags).selectinload(ProblemTag.tag),
    ).all()

    return [
        {
            "id": problem.id,
            "title": problem.title,
            "description": problem.description,
            "difficulty": problem.difficulty.value if problem.difficulty else None,
            "xp_reward": problem.xp_reward,
            "created_at": problem.created_at,
            "acceptance_rate": problem.acceptance_rate,
            "tags": [
                {
                    "id": t.tag_id,
                    "name": t.tag.name if t.tag else None,
                    "category": t.tag.category.value if t.tag and t.tag.category else None,
                }
                for t in problem.tags
            ],
            "solved_status": problem.id in solved_ids
        }
        for problem in problems
    ]

    # problems = Problem.query.all()
    # return [
    #     {
    #         "id": p.id,
    #         "title": p.title,
    #         "description": p.description,
    #         "difficulty": p.difficulty.value if p.difficulty else None,
    #         "xp_reward": p.xp_reward,
    #         "created_at": p.created_at
    #     } for p in problems
    # ]

    # start = time.time()
    # print("Sovled ids start : ", start)

    # solved_ids = [int(s.problem_id) for s in SolvedProblem.query.filter_by(user_id=user_id).with_entities(SolvedProblem.problem_id).all()]

    # solved_ids_end = time.time()
    # print("Solved ids end : ", round((solved_ids_end - start)*1e3) , "ms")


    # problems = Problem.query.options(
    #     selectinload(Problem.tags).selectinload(ProblemTag.tag),
    # ).all()


    # print("ALL problems end : ", round((time.time() - solved_ids_end)*1e3))


    # print("SOlved ids  :",[(id, type(id)) for id in solved_ids])


    # for problem in problems:
    #     print(problem.id , type(problem.id))
    #     if problem.id in solved_ids:
    #         print('yessssssss')



    # return [
    #     {
    #         "id": problem.id,
    #         "title": problem.title,
    #         "description": problem.description,
    #         "difficulty": problem.difficulty.value if problem.difficulty else None,
    #         "xp_reward": problem.xp_reward,
    #         "created_at": problem.created_at,
    #         "acceptance_rate": problem.acceptance_rate,
    #         "tags": [
    #             {
    #                 "id": t.tag_id,
    #                 "name": t.tag.name if t.tag else None,
    #                 "category": t.tag.category.value if t.tag and t.tag.category else None,
    #             }

    #             for t in problem.tags
    #         ],
    #         "solved_status": int(problem.id) in solved_ids
    #     } 
        
    #     for problem in problems
    # ]

    





def fetch_problem_by_id(problem_id: int, user_id):


    # problem = Problem.query.filter(Problem.id == problem_id).first()
    # editorial = Editorial.query.join(Problem).filter(Problem.id == problem_id).first()
    # hints = Hint.query.join(Problem).filter(Problem.id == problem_id).order_by(Hint.order).all()
    # constraints = Constraint.query.join(Problem).filter(Problem.id == problem_id).order_by(Constraint.order).all()
    # snippets = Snippet.query.join(Problem).filter(Problem.id == problem_id).all()
    # tags = Tag.query.join(ProblemTag).join(Problem).filter(Problem.id == problem_id).order_by(Tag.order).all()
    # testcases = Testcase.query.join(Problem).filter(Problem.id == problem_id).order_by(Testcase.order).all()


    start = time.time()
    print("Start time", start)


    problem = (
        Problem.query.options(
            joinedload(Problem.editorial),
            selectinload(Problem.hints),
            selectinload(Problem.constraints),
            selectinload(Problem.snippets).selectinload(Snippet.language),
            selectinload(Problem.tags).selectinload(ProblemTag.tag),
            selectinload(Problem.testcases),
        ).filter(Problem.id == problem_id).first()
    )

    problem_query_end_time = time.time()

    print("Prolem query total time taken : ", round((problem_query_end_time - start)*1e3), "ms")




    languages = {snippet.language for snippet in problem.snippets if snippet.language is not None}

    print("Languages:", languages)


    lang_query_end_time = time.time()

    print("lang query total time taken : ", round((lang_query_end_time - problem_query_end_time)*1e3),"ms")


    if not problem:
        return None
    
    submissions = Submission.query.filter_by(user_id=user_id, problem_id=problem_id).all()


    sub_query_end_time = time.time()

    print("sub query total time taken : ", round((sub_query_end_time - lang_query_end_time)*1e3), "ms")




    return {
            "id": problem.id,
            "title": problem.title,
            "description": problem.description,
            "difficulty": problem.difficulty.value if problem.difficulty else None,
            "xp_reward": problem.xp_reward,
            "created_at": problem.created_at,
            "acceptance_rate": problem.acceptance_rate, 
            "editorial": {
                "id": problem.editorial.id,
                "problem_id": problem.editorial.problem_id,
                "content": problem.editorial.content_markdown,
                "videoUrl": problem.editorial.videoUrl,
                "created_at": problem.editorial.created_at
            },
            "hints": [
                {
                    "id": h.id,
                    "problem_id": h.problem_id,
                    "content": h.content,
                    "order": h.order,
                    "created_at": h.created_at
                }

                for h in problem.hints
            ],
            "constraints": [
                {
                    "id": c.id,
                    "problem_id": c.problem_id,
                    "content": c.description,
                    "order": c.order,
                    "created_at": c.created_at
                }

                for c in problem.constraints
            ],
            "snippets": [
                {
                    "id": s.id,
                    "problem_id": s.problem_id,
                    "code": s.code,
                    "language_name": s.language.name if s.language else None,
                    "language_id": s.language.id if s.language else None,
                    "created_at": s.created_at
                }

                for s in problem.snippets
            ],
            "tags": [
                {
                    "id": t.tag_id,
                    "name": t.tag.name if t.tag else None,
                    "category": t.tag.category.value if t.tag and t.tag.category else None,
                }

                for t in problem.tags
            ],
            "testcases": [
                {
                    "id": tc.id,
                    "input": tc.input_data,
                    "expected_output": tc.expected_output,
                    "input_to_show": tc.input_to_show,
                    "expected_output_to_show": tc.expected_output_to_show,
                    "explanation": tc.explanation,
                    "isHidden": tc.isHidden,
                    "order": tc.order,
                    "created_at": tc.created_at
                }
                
                for tc in problem.testcases if not tc.isHidden
            ],
            "submissions": [{
                "id": sub.id,
                "user_id": sub.user_id,
                "problem_id": sub.problem_id,
                "status": sub.status,
                "created_at": sub.created_at,
                "totalExecTime": sub.total_exec_time,
                "totalExecMemory": sub.total_exec_memory,
                "language_name": sub.language_name,
                "mode": sub.submission_answer.mode.value
            } for sub in submissions ],

            "languages": [{
                "id": lang.id,
                "name": lang.name,
                "compiler_language_id": lang.compiler_language_id
            } for lang in languages]
        }


def fetch_all_testcases(problem_id: int):
    testcases = Testcase.query.filter_by(problem_id=problem_id)
    return [
            {
                "id": tc.id,
                "input": tc.input_data,
                "expected_output": tc.expected_output,
                "explanation": tc.explanation,
                "isHidden": tc.isHidden,
                "order": tc.order,
                "created_at": tc.created_at
            }
            
            for tc in testcases
        ],




# def fetch_problem_editorial(problem_id: int):
#     editorial = Editorial.query.filter_by(problem_id=problem_id).first()
#     if not editorial:
#         return None
    
#     return {
#         "id": editorial.id,
#         "problem_id": editorial.problem_id,
#         "content": editorial.content_markdown,
#         "videoUrl": editorial.videoUrl,
#         "created_at": editorial.created_at
#     }






# def fetch_problem_hints(problem_id: int):
#     hints = Hint.query.filter_by(problem_id=problem_id).order_by(Hint.order).all()

#     return [
#         {
#             "id": h.id,
#             "problem_id": h.problem_id,
#             "content": h.content,
#             "order": h.order,
#             "created_at": h.created_at
#         }

#         for h in hints
#     ]





# def fetch_problem_constraints(problem_id: int):
#     constraints = Constraint.query.filter_by(problem_id=problem_id).order_by(Constraint.order).all()


#     return [
#         {
#             "id": c.id,
#             "problem_id": c.problem_id,
#             "content": c.description,
#             "order": c.order,
#             "created_at": c.created_at
#         }

#         for c in constraints
#     ]


   

# def fetch_problem_snippets(problem_id: int):
#     snippets = Snippet.query.filter_by(problem_id=problem_id).all()


#     return [
#         {
#             "id": s.id,
#             "problem_id": s.problem_id,
#             "code": s.code,
#             "language_name": s.language.name if s.language else None,
#             "language_id": s.language.id if s.language else None,
#             "created_at": s.created_at
#         }

#         for s in snippets
#     ]




# def fetch_problem_tags(problem_id: int):
#     tags = ProblemTag.query.filter_by(problem_id=problem_id).all()

#     return [
#         {
#             "id": t.tag_id,
#             "name": t.tag.name if t.tag else None,
#             "category": t.tag.category.value if t.tag and t.tag.category else None,
#         }

#         for t in tags
#     ]


# def fetch_problem_testcases(problem_id: int):
#     testcases = Testcase.query.filter_by(problem_id=problem_id).order_by(Testcase.order).all()

#     return [
#         {
#             "id": tc.id,
#             "input": tc.input_data,
#             "expected_output": tc.expected_output,
#             "explanation": tc.explanation,
#             "isHidden": tc.isHidden,
#             "order": tc.order,
#             "created_at": tc.created_at
#         }
        
#         for tc in testcases
    # ]

def create_new_problem(data):
    
    data = get_data()[0]

    print(Problem.query.filter_by(title=data.get('title')).first()) 
    if Problem.query.filter_by(title=data.get('title')).first() != None:    
        print('helllooo')
        return None


    problem = Problem(
        title=data.get('title'),
        description=data.get('description'),
        difficulty=data.get('difficulty'),
        xp_reward=data.get('xp_reward', 0),
    )

    db.session.add(problem)
    db.session.flush() # get problem.id


    
    
    editorial = Editorial(
        content_markdown=data.get('editorial'),
        videoUrl=data['editorial']['videoUrl'],
        problem_id=problem.id
    )

    db.session.add(editorial)




    hints_data = data.get('hints', [])
    for h in hints_data:
        hint = Hint(
            content=h.get('content'),
            order=h.get('order'),
            problem_id=problem.id
        )

        db.session.add(hint)


    constraints_data = data.get('constraints', [])
    for c in constraints_data:
        constraint = Constraint(
            description=c.get('description'),
            order=c.get('order'),
            problem_id=problem.id
        )

        db.session.add(constraint)


    tags_data = data.get("tags", [])
    for t in tags_data:

        tag = Tag.query.filter_by(name=t.get("name")).first()
        if not tag:
            tag = Tag(
                name=t.get("name"),
                category=t.get("category")
            )

            db.session.add(tag)
            db.session.flush()

        problem_tag = ProblemTag(
            problem_id=problem.id,
            tag_id=tag.id
        )

        db.session.add(problem_tag)



    snippets_data = data.get("snippets", [])
    for s in snippets_data:
        
        lang_name = s.get("lang")
        language = Language.query.filter_by(name=lang_name).first()
        if not language:
            language = Language(
                name=lang_name,
                compiler_language_id=s.get("compiler_language_id")
            )

            db.session.add(language)
            db.session.flush()
        

        snippet = Snippet(
            code=s.get("code"),
            problem_id=problem.id,
            language_id=language.id
        )

        db.session.add(snippet)
    

    testcases_data = data.get("testcases", [])
    for tc in testcases_data:

        testcase = Testcase(
            input_data=tc.get('input'),
            expected_output=tc.get("expectedOutput"),
            explanation=tc.get("explanation"),
            isHidden=tc.get('isHidden'),
            order=tc.get('order'),
            
            problem_id=problem.id
        )

        db.session.add(testcase)
    



    

    db.session.commit()
    return {
        "success": True,
        "message": "Data stored successfully",
        "data": {
            "id": problem.id,
            "title": problem.title
        }
    }



def fetch_daily_challenge(user_id: int):
    """
    Select a daily challenge for the user based on:
    - Problems the user has not solved
    - Slightly harder difficulty than user's average
    - Prefer problems from topics user has solved most
    """

    # 1️⃣ Fetch solved problem IDs
    solved_problem_ids = [pid for (pid,) in db.session.query(SolvedProblem.problem_id)
                          .filter(SolvedProblem.user_id == user_id).all()]

    # 2️⃣ Fetch top 3 favorite topics
    topic_counts = (
        db.session.query(Tag.id, func.count(SolvedProblem.id).label("solved_count"))
        .join(ProblemTag, ProblemTag.tag_id == Tag.id)
        .join(Problem, Problem.id == ProblemTag.problem_id)
        .join(SolvedProblem, SolvedProblem.problem_id == Problem.id)
        .filter(SolvedProblem.user_id == user_id, Tag.category == "Topic")
        .group_by(Tag.id)
        .order_by(func.count(SolvedProblem.id).desc())
        .limit(3)
        .all()
    )
    favorite_topics = [t.id for t in topic_counts]

    # 3️⃣ Determine target difficulty
    diff_map = {DifficultyEnum.Easy: 1, DifficultyEnum.Medium: 2, DifficultyEnum.Hard: 3}
    solved_difficulties = db.session.query(Problem.difficulty, func.count(SolvedProblem.id)) \
        .join(SolvedProblem, SolvedProblem.problem_id == Problem.id) \
        .filter(SolvedProblem.user_id == user_id) \
        .group_by(Problem.difficulty).all()

    if solved_difficulties:
        avg_diff = sum(diff_map[d] * c for d, c in solved_difficulties) / sum(c for _, c in solved_difficulties)
        target_num = min(3, round(avg_diff + 0.5))
    else:
        target_num = 1

    num_to_diff = {1: DifficultyEnum.Easy, 2: DifficultyEnum.Medium, 3: DifficultyEnum.Hard}
    target_diff = num_to_diff[target_num]

    # 4️⃣ Query candidate problems
    query = db.session.query(Problem).options(joinedload(Problem.tags).joinedload(ProblemTag.tag)) \
        .filter(~Problem.id.in_(solved_problem_ids), Problem.difficulty == target_diff)

    if favorite_topics:
        query = query.join(Problem.tags).filter(ProblemTag.tag_id.in_(favorite_topics))

    candidates = query.all()

    # fallback if no candidates
    if not candidates:
        candidates = db.session.query(Problem).options(joinedload(Problem.tags).joinedload(ProblemTag.tag)) \
            .filter(~Problem.id.in_(solved_problem_ids), Problem.difficulty == target_diff).all()
    if not candidates:
        candidates = db.session.query(Problem).options(joinedload(Problem.tags).joinedload(ProblemTag.tag)) \
            .filter(~Problem.id.in_(solved_problem_ids)).all()
    if not candidates:
        return None

    # 5️⃣ Pick random problem
    selected = random.choice(candidates)

    # 6️⃣ Return frontend-ready JSON
    return {
        "id": selected.id,
        "title": selected.title,
        "description": selected.description,
        "difficulty": selected.difficulty.value if selected.difficulty else "Medium",
        "xp_reward": selected.xp_reward,
        "tags": [{"id": pt.tag.id, "name": pt.tag.name, "category": pt.tag.category.value} 
                 for pt in selected.tags if pt.tag]
    }

    # --- Step 1: get IDs of problems already solved ---
    solved_problem_ids = (
        db.session.query(SolvedProblem.problem_id)
        .filter(SolvedProblem.user_id == user_id)
        .all()
    )
    solved_problem_ids = [pid for (pid,) in solved_problem_ids]

    # --- Step 2: get user's most solved topics ---
    topic_counts = (
        db.session.query(Tag.id, Tag.name, func.count(SolvedProblem.id).label("solved_count"))
        .join(ProblemTag, ProblemTag.tag_id == Tag.id)
        .join(Problem, Problem.id == ProblemTag.problem_id)
        .join(SolvedProblem, SolvedProblem.problem_id == Problem.id)
        .filter(SolvedProblem.user_id == user_id, Tag.category == "Topic")
        .group_by(Tag.id, Tag.name)
        .order_by(func.count(SolvedProblem.id).desc())
        .all()
    )

    favorite_topics = [t.id for t in topic_counts[:3]]  # top 3 topics

    # --- Step 3: determine target difficulty ---
    # Map difficulty to numeric for averaging
    diff_map = {"Easy": 1, "Medium": 2, "Hard": 3}

    solved_difficulties = (
        db.session.query(Problem.difficulty, func.count(SolvedProblem.id))
        .join(SolvedProblem, SolvedProblem.problem_id == Problem.id)
        .filter(SolvedProblem.user_id == user_id)
        .group_by(Problem.difficulty)
        .all()
    )

    if solved_difficulties:
        avg_diff_num = sum(diff_map[d] * c for d, c in solved_difficulties) / sum(c for _, c in solved_difficulties)
        target_diff_num = min(3, round(avg_diff_num + 0.5))  # slightly harder
    else:
        target_diff_num = 1  # default Easy

    num_to_diff = {1: "Easy", 2: "Medium", 3: "Hard"}
    target_difficulty = num_to_diff[target_diff_num]

    # --- Step 4: query candidate problems ---
    query = (
        db.session.query(Problem)
        .options(joinedload(Problem.tags).joinedload(ProblemTag.tag))
        .filter(~Problem.id.in_(solved_problem_ids))
        .filter(Problem.difficulty == target_difficulty)
    )

    # prioritize favorite topics
    if favorite_topics:
        query = query.join(Problem.tags).filter(ProblemTag.tag_id.in_(favorite_topics))

    candidates = query.all()

    # fallback if no candidate in favorite topics
    if not candidates:
        candidates = (
            db.session.query(Problem)
            .options(joinedload(Problem.tags).joinedload(ProblemTag.tag))
            .filter(~Problem.id.in_(solved_problem_ids))
            .filter(Problem.difficulty == target_difficulty)
            .all()
        )

    # fallback if still no candidates
    if not candidates:
        candidates = (
            db.session.query(Problem)
            .options(joinedload(Problem.tags).joinedload(ProblemTag.tag))
            .filter(~Problem.id.in_(solved_problem_ids))
            .all()
        )

    if not candidates:
        return None

    return random.choice(candidates)

    # --- Step 1: get problem IDs user has already solved ---
    solved_problem_ids = (
        db.session.query(SolvedProblem.problem_id)
        .filter(SolvedProblem.user_id == user_id)
        .all()
    )
    solved_problem_ids = [pid for (pid,) in solved_problem_ids]

    # --- Step 2: get the user's most solved topics ---
    topic_counts = (
        db.session.query(Tag.id, Tag.name, func.count(SolvedProblem.id).label("solved_count"))
        .join(ProblemTag, ProblemTag.tag_id == Tag.id)
        .join(Problem, Problem.id == ProblemTag.problem_id)
        .join(SolvedProblem, SolvedProblem.problem_id == Problem.id)
        .filter(SolvedProblem.user_id == user_id, Tag.category == "Topic")
        .group_by(Tag.id, Tag.name)
        .order_by(func.count(SolvedProblem.id).desc())
        .all()
    )

    favorite_topics = [t.id for t in topic_counts[:3]]  # top 3 topics

    # --- Step 3: determine target difficulty ---
    # Find average difficulty of user's solved problems
    solved_difficulties = (
        db.session.query(Problem.difficulty, func.count(SolvedProblem.id))
        .join(SolvedProblem, SolvedProblem.problem_id == Problem.id)
        .filter(SolvedProblem.user_id == user_id)
        .group_by(Problem.difficulty)
        .all()
    )
    # Map to numeric: Easy=1, Medium=2, Hard=3
    diff_map = {"Easy": 1, "Medium": 2, "Hard": 3}
    if solved_difficulties:
        avg_diff_num = sum(diff_map[d.value if isinstance(d, DifficultyEnum) else d] * c for d, c in solved_difficulties) / sum(c for _, c in solved_difficulties)
        # bump difficulty by +0.5, max 3
        target_diff_num = min(3, round(avg_diff_num + 0.5))
    else:
        target_diff_num = 1  # default Easy

    num_to_diff = {1: DifficultyEnum.Easy, 2: DifficultyEnum.Medium, 3: DifficultyEnum.Hard}
    target_difficulty = num_to_diff[target_diff_num]

    # --- Step 4: query candidate problems ---
    query = (
        db.session.query(Problem)
        .options(joinedload(Problem.tags).joinedload(ProblemTag.tag))
        .filter(~Problem.id.in_(solved_problem_ids))
        .filter(Problem.difficulty == target_difficulty)
    )

    # prioritize favorite topics if available
    if favorite_topics:
        query = query.join(Problem.tags).filter(ProblemTag.tag_id.in_(favorite_topics))

    candidates = query.all()

    # fallback: if no candidates in preferred topics, relax topic constraint
    if not candidates:
        candidates = (
            db.session.query(Problem)
            .options(joinedload(Problem.tags).joinedload(ProblemTag.tag))
            .filter(~Problem.id.in_(solved_problem_ids))
            .filter(Problem.difficulty == target_difficulty)
            .all()
        )

    if not candidates:
        # fallback: pick any unsolved problem
        candidates = (
            db.session.query(Problem)
            .options(joinedload(Problem.tags).joinedload(ProblemTag.tag))
            .filter(~Problem.id.in_(solved_problem_ids))
            .all()
        )

    if not candidates:
        return None

    # --- Step 5: pick one randomly from candidates ---
    return random.choice(candidates)

    """
    Select a daily challenge for the user based on:
    1. Problems the user hasn't solved yet
    2. Prefer problems in topics the user is familiar with
    3. Slightly increase difficulty over user's current average
    """

    # 1️⃣ Fetch all problem IDs the user has already solved
    solved_problem_ids = (
        db.session.query(SolvedProblem.problem_id)
        .filter(SolvedProblem.user_id == user_id)
        .all()
    )
    solved_problem_ids = [pid for (pid,) in solved_problem_ids]

    # 2️⃣ Fetch unsolved problems
    unsolved_problems = (
        db.session.query(Problem)
        .options(joinedload(Problem.tags).joinedload("tag"))  # eager load tags
        .filter(~Problem.id.in_(solved_problem_ids))
        .all()
    )

    if not unsolved_problems:
        # If user solved everything, just return a random problem
        return db.session.query(Problem).order_by(func.random()).first()

    # 3️⃣ Compute user's difficulty preference
    solved_by_diff = (
        db.session.query(Problem.difficulty, db.func.count(SolvedProblem.id))
        .join(SolvedProblem, SolvedProblem.problem_id == Problem.id)
        .filter(SolvedProblem.user_id == user_id)
        .group_by(Problem.difficulty)
        .all()
    )
    solved_by_diff_dict = {diff: count for diff, count in solved_by_diff}

    # Determine preferred difficulty (lowest solved count = challenge)
    difficulty_order = [DifficultyEnum.Easy, DifficultyEnum.Medium, DifficultyEnum.Hard]
    preferred_difficulty = min(difficulty_order, key=lambda d: solved_by_diff_dict.get(d, 0))

    # 4️⃣ Filter unsolved problems by preferred difficulty if available
    filtered_problems = [p for p in unsolved_problems if p.difficulty == preferred_difficulty]
    if not filtered_problems:
        filtered_problems = unsolved_problems

    # 5️⃣ Rank by matching tags/topics user already solved
    solved_tags = (
        db.session.query(Problem.tags)
        .join(SolvedProblem, SolvedProblem.problem_id == Problem.id)
        .filter(SolvedProblem.user_id == user_id)
        .all()
    )
    solved_tag_ids = {pt.tag_id for pt_list in solved_tags for pt in pt_list}

    def tag_match_score(problem):
        problem_tag_ids = {pt.tag_id for pt in problem.tags}
        return len(problem_tag_ids & solved_tag_ids)

    filtered_problems.sort(key=tag_match_score, reverse=True)

    # 6️⃣ Return top scored problem, fallback to random if tie
    top_score = tag_match_score(filtered_problems[0])
    top_problems = [p for p in filtered_problems if tag_match_score(p) == top_score]

    return random.choice(top_problems)

    """
    Fetch a Daily Challenge problem for the user, based on:
    - Problems the user has not solved
    - Difficulty progression (Easy → Medium → Hard)
    - Topics the user has solved least
    - Tie-breakers: lower acceptance rate, older problems
    """

    # 1️⃣ Get all solved problem IDs for the user
    solved = SolvedProblem.query.filter_by(user_id=user_id).all()
    solved_ids = {s.problem_id for s in solved}

    # 2️⃣ Count how many problems solved per topic
    topic_counter = Counter()
    for s in solved:
        problem = Problem.query.get(s.problem_id)
        for pt in problem.tags:
            if pt.tag and pt.tag.category.name == "Topic":
                topic_counter[pt.tag.name] += 1

    # 3️⃣ Determine target difficulty
    solved_difficulty_counts = Counter([s.problem.difficulty for s in solved])
    if solved_difficulty_counts[DifficultyEnum.Easy] >= 3:
        target_difficulty = DifficultyEnum.Medium
    elif solved_difficulty_counts[DifficultyEnum.Medium] >= 3:
        target_difficulty = DifficultyEnum.Hard
    else:
        target_difficulty = DifficultyEnum.Easy

    # 4️⃣ Fetch all unsolved problems
    unsolved_problems = Problem.query.filter(~Problem.id.in_(solved_ids)).options(
        db.selectinload(Problem.tags).selectinload(ProblemTag.tag)
    ).all()

    if not unsolved_problems:
        # fallback: pick first problem in DB if user solved everything
        problem = Problem.query.options(
            db.selectinload(Problem.tags).selectinload(ProblemTag.tag)
        ).first()
        if not problem:
            return None
    else:
        # 5️⃣ Score each problem
        problem_scores = []
        for p in unsolved_problems:
            score = 0
            # Matching target difficulty gets +2
            if p.difficulty == target_difficulty:
                score += 2

            # Topics the user has solved less get higher score
            for pt in p.tags:
                if pt.tag and pt.tag.category.name == "Topic":
                    score += max(0, 3 - topic_counter.get(pt.tag.name, 0))

            # Optional: tie-breaker using acceptance rate (lower = harder)
            score += max(0, (100 - p.acceptance_rate) / 50)  # normalize 0-2

            problem_scores.append((score, p))

        # Sort by score descending, then by creation date ascending
        problem_scores.sort(key=lambda x: (-x[0], x[1].created_at))
        problem = problem_scores[0][1]

    # 6️⃣ Organize tags by category for frontend
    tag_dict = {}
    for pt in problem.tags:
        if pt.tag:
            category = pt.tag.category.value if pt.tag.category else "General"
            tag_dict.setdefault(category, []).append(pt.tag.name)

    # 7️⃣ Return problem
    return {
        "id": problem.id,
        "title": problem.title,
        "description": problem.description,
        "difficulty": problem.difficulty.value if problem.difficulty else "Medium",
        "xp": problem.xp_reward,
        "tags": tag_dict
    }

