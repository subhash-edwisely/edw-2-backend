from app import create_app
from db import db
from models.snippet import Snippet
from sqlalchemy import text

# Create Flask app
app = create_app()

def update_snippet_code(problem_id, language_id, new_code):
    snippet = Snippet.query.filter_by(
        problem_id=problem_id,
        language_id=language_id
    ).first()

    if not snippet:
        print("Snippet not found")
        return

    snippet.code = new_code
    db.session.commit()
    print("Snippet updated successfully")


# def update_testcase_table():
    #





if __name__ == "__main__":

    new_code = "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\nclass Solution:\n    def mergeTwoLists(self, list1, list2):\n        pass\n\nif __name__ == '__main__':\n    import sys\n    \n    def list_to_linkedlist(arr):\n        if not arr:\n            return None\n        head = ListNode(arr[0])\n        current = head\n        for val in arr[1:]:\n            current.next = ListNode(val)\n            current = current.next\n        return head\n    \n    def linkedlist_to_list(head):\n        result = []\n        current = head\n        while current:\n            result.append(current.val)\n            current = current.next\n        return result\n    \n    lines = sys.stdin.read().strip().split('\n')\n    line1 = lines[0] if len(lines) > 0 else ''\n    line2 = lines[1] if len(lines) > 1 else ''\n    \n    list1 = list(map(int, line1.split())) if line1 else []\n    list2 = list(map(int, line2.split())) if line2 else []\n    \n    head1 = list_to_linkedlist(list1)\n    head2 = list_to_linkedlist(list2)\n    \n    sol = Solution()\n    result_head = sol.mergeTwoLists(head1, head2)\n    result = linkedlist_to_list(result_head)\n    print(result)"
    with app.app_context():   # :fire: REQUIRED
        update_snippet_code(
            problem_id=4,
            language_id=1,
            new_code=new_code
        )






