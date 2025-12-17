from models.problem import Problem
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

    start = time.time()
    print("Sovled ids start : ", start)

    solved_ids = [int(s.problem_id) for s in SolvedProblem.query.filter_by(user_id=user_id).with_entities(SolvedProblem.problem_id).all()]

    solved_ids_end = time.time()
    print("Solved ids end : ", round((solved_ids_end - start)*1e3) , "ms")


    problems = Problem.query.options(
        selectinload(Problem.tags).selectinload(ProblemTag.tag),
    ).all()


    print("ALL problems end : ", round((time.time() - solved_ids_end)*1e3))


    print("SOlved ids  :",[(id, type(id)) for id in solved_ids])


    for problem in problems:
        print(problem.id , type(problem.id))
        if problem.id in solved_ids:
            print('yessssssss')



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
            "solved_status": int(problem.id) in solved_ids
        } 
        
        for problem in problems
    ]

    





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



def fetch_daily_challenge():
    problems = Problem.query.all()
    if not problems:
        return None
    
    problem = random.choice(problems)
    
    # Organize tags by category
    tag_dict = {}
    for pt in problem.tags:
        if pt.tag:  # Make sure tag exists
            category = pt.tag.category.value if pt.tag.category else "General"
            if category not in tag_dict:
                tag_dict[category] = []
            tag_dict[category].append(pt.tag.name)
    
    return {
        "id": problem.id,
        "title": problem.title,
        "description": problem.description,
        "difficulty": problem.difficulty.value,
        "xp": problem.xp_reward,
        "tags": tag_dict  # Now tags are grouped by category
    }


        
