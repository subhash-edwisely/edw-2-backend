from services.submission_service import (
    fetch_submission_by_id,
    create_new_submission
)

from utils.response import success, error

# def get_submissions_of_user_for_problem(user_id: int, problem_id: int):
#     try: 
#         submissions = fetch_submissions_of_user_for_problem(user_id, problem_id)
#         return success(data=submissions)
    
#     except Exception as e:
#         return error(str(e))
    



# def get_submissions_of_user(user_id: int):
#     try:
#         submissions = fetch_submissions_of_user(user_id)
#         return success(data=submissions)
    
#     except Exception as e:
#         return error(str(e))



def get_submission_by_id(submission_id: int):
    try:
        submission = fetch_submission_by_id(submission_id)
        return success(data=submission)
    
    except Exception as e:
        return error(str(e))
    

def create_submission(data):
    try:
        new_submission = create_new_submission(data)
        return success(new_submission)
    
    except Exception as e:
        return error(str(e))