from db import db
from models import AIHelp, HelpTypeEnum

def create_ai_help(user_id, problem_id, help_type, xp_cost, prompt, response):
    if help_type not in HelpTypeEnum.__members__:
        raise ValueError(f"Invalid help_type: {help_type}")

    ai_help = AIHelp(
        user_id=user_id,
        problem_id=problem_id,
        help_type=HelpTypeEnum[help_type],
        xp_cost=xp_cost,
        prompt=prompt,
        response=response
    )
    db.session.add(ai_help)
    db.session.commit()
    return ai_help
