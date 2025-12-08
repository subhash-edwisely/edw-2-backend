from models.problem import Problem
from models.editorial import Editorial
from models.hint import Hint
from models.constraint import Constraint
from models.snippet import Snippet
from models.problem_tag import ProblemTag
from models.tag import Tag
from models.language import Language
from models.testcase import Testcase
from db import db




def fetch_all_problems():
    problems = Problem.query.all()
    return [
        {
            "id": p.id,
            "title": p.title,
            "description": p.description,
            "difficulty": p.difficulty,
            "xp_reward": p.xp_reward,
            "created_at": p.created_at
        } for p in problems
    ]




def fetch_problem_by_id(problem_id: int):
    problem = Problem.query.get(problem_id)
    if not problem:
        return None
    
    return {
            "id": problem.id,
            "title": problem.title,
            "description": problem.description,
            "difficulty": problem.difficulty,
            "xp_reward": problem.xp_reward,
            "created_at": problem.created_at
        }





def fetch_problem_editorial(problem_id: int):
    editorial = Editorial.query.filter_by(problem_id=problem_id).first()
    if not editorial:
        return None
    
    return {
        "id": editorial.id,
        "problem_id": editorial.problem_id,
        "content": editorial.content_markdown,
        "videoUrl": editorial.videoUrl,
        "created_at": editorial.created_at
    }






def fetch_problem_hints(problem_id: int):
    hints = Hint.query.filter_by(problem_id=problem_id).order_by(Hint.order).all()

    return [
        {
            "id": h.id,
            "problem_id": h.problem_id,
            "content": h.content,
            "order": h.order,
            "created_at": h.created_at
        }

        for h in hints
    ]





def fetch_problem_constraints(problem_id: int):
    constraints = Constraint.query.filter_by(problem_id=problem_id).order_by(Constraint.order).all()


    return [
        {
            "id": c.id,
            "problem_id": c.problem_id,
            "content": c.description,
            "order": c.order,
            "created_at": c.created_at
        }

        for c in constraints
    ]


   

def fetch_problem_snippets(problem_id: int):
    snippets = Snippet.query.filter_by(problem_id=problem_id).all()


    return [
        {
            "id": s.id,
            "problem_id": s.problem_id,
            "code": s.code,
            "language_name": s.language.name if s.language else None,
            "created_at": s.created_at
        }

        for s in snippets
    ]




def fetch_problem_tags(problem_id: int):
    tags = ProblemTag.query.filter_by(problem_id=problem_id).all()

    return [
        {
            "id": t.tag_id,
            "name": t.tag.name if t.tag else None,
            "category": t.tag.category if t.tag else None,
        }

        for t in tags
    ]


def fetch_problem_testcases(problem_id: int):
    testcases = Testcase.query.filter_by(problem_id=problem_id).order_by(Testcase.order).all()

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
    ]

def create_new_problem(data: dict):
    
    data = {
        "title": "Two Sum",
        "description": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.\n\nYou may assume that each input would have exactly one solution, and you may not use the same element twice.\n\nYou can return the answer in any order.",
        "xpReward": 10,
        "difficulty": "Easy",
        "hints": [
            {
                "content": "Try using a hash map to store the numbers you've seen so far.",
                "order": 1
            },
            {
                "content": "For each number, check if target - current number exists in your hash map.",
                "order": 2
            },
            {
                "content": "The time complexity can be reduced to O(n) with this approach.",
                "order": 3
            }
        ],

        "constraints": [
            {
                "description": "2 <= nums.length <= 10^4",
                "order": 1
            },
            {
                "description": "-10^9 <= nums[i] <= 10^9",
                "order": 2
            },
            {
                "description": "-10^9 <= target <= 10^9",
                "order": 3
            },
            {
                "description": "Only one valid answer exists",
                "order": 4
            }
        ],
        
        "editorial": {
                "title": "Two sum",

                    "overview": """
                The **Two Sum** problem asks us to find two indices such that their values add up to a given target.

                A few common approaches are:
                - Brute Force using nested loops
                - Hash Map for an optimal O(n) solution

                Below are detailed explanations of both approaches.
                """,

                    "approaches": [
                        {
                            "id": "brute_force",
                            "title": "Approach 1: Brute Force",
                            "explanation": """
                The simplest idea is to check every possible pair of numbers.

                ### Algorithm
                1. Loop through each index `i`
                2. For each `i`, loop through each index `j > i`
                3. If `nums[i] + nums[j] == target`, return `[i, j]`

                ### Why it works
                We explore all combinations, so if a solution exists, we will find it.

                ### Complexity
                - Time: O(n²)
                - Space: O(1)
                """,
                            "code": {
                                "python": """
                class Solution:
                    def twoSum(self, nums, target):
                        for i in range(len(nums)):
                            for j in range(i + 1, len(nums)):
                                if nums[i] + nums[j] == target:
                                    return [i, j]
                """,
                                "java": """
                class Solution {
                    public int[] twoSum(int[] nums, int target) {
                        for (int i = 0; i < nums.length; i++) {
                            for (int j = i + 1; j < nums.length; j++) {
                                if (nums[i] + nums[j] == target) {
                                    return new int[]{i, j};
                                }
                            }
                        }
                        return new int[]{};
                    }
                }
                """,
                                "cpp": """
                class Solution {
                public:
                    vector<int> twoSum(vector<int>& nums, int target) {
                        for (int i = 0; i < nums.size(); i++) {
                            for (int j = i + 1; j < nums.size(); j++) {
                                if (nums[i] + nums[j] == target) {
                                    return {i, j};
                                }
                            }
                        }
                        return {};
                    }
                };
                """
                            }
                        },

                        {
                            "id": "optimal_hashmap",
                            "title": "Approach 2: Hash Map (Optimal O(n))",
                            "explanation": """
                We can solve the problem in **one pass** using a hash map.

                ### Key Idea
                While iterating over the array:
                - Compute the complement: `target - nums[i]`
                - If the complement is already in the map → we found the answer
                - Otherwise, store the current number in the map

                ### Algorithm
                1. Create an empty hash map
                2. Loop through each index `i`
                3. Let `num = nums[i]`
                4. Compute `complement = target - num`
                5. If complement is in the map, return `[map[complement], i]`
                6. Otherwise, store `map[num] = i`

                ### Complexity
                - Time: O(n)
                - Space: O(n)
                """,
                            "code": {
                                "python": """
                class Solution:
                    def twoSum(self, nums, target):
                        seen = {}
                        for i, value in enumerate(nums):
                            complement = target - value
                            if complement in seen:
                                return [seen[complement], i]
                            seen[value] = i
                """,
                                "java": """
                class Solution {
                    public int[] twoSum(int[] nums, int target) {
                        Map<Integer, Integer> seen = new HashMap<>();

                        for (int i = 0; i < nums.length; i++) {
                            int complement = target - nums[i];

                            if (seen.containsKey(complement)) {
                                return new int[]{seen.get(complement), i};
                            }

                            seen.put(nums[i], i);
                        }

                        return new int[]{};
                    }
                }
                """,
                                "cpp": """
                class Solution {
                public:
                    vector<int> twoSum(vector<int>& nums, int target) {
                        unordered_map<int, int> seen;

                        for (int i = 0; i < nums.size(); i++) {
                            int complement = target - nums[i];

                            if (seen.count(complement)) {
                                return {seen[complement], i};
                            }

                            seen[nums[i]] = i;
                        }

                        return {};
                    }
                };
                """
                            }
                        }
                    ],

                    "videoUrl": "https://www.youtube.com/watch?v=KLlXCFG5TnA"
        },

        "testcases": [
            {
                "input": "[2,7,11,15]\n9",
                "expectedOutput": "[0,1]",
                "isHidden": False,
                "order": 1,
                "explanation": ""
            },
            {
                "input": "[3,2,4]\n6",
                "expectedOutput": "[1,2]",
                "isHidden": False,
                "order": 2,
                "explanation": ""
            },
            {
                "input": "[3,3]\n6",
                "expectedOutput": "[0,1]",
                "isHidden": False,
                "order": 3,
                "explanation": ""
            },
            {
                "input": "[1,5,3,7,8,9]\n12",
                "expectedOutput": "[2,4]",
                "isHidden": True,
                "order": 4,
                "explanation": ""
            },
            {
                "input": "[-1,-2,-3,-4,-5]\n-8",
                "expectedOutput": "[2,4]",
                "isHidden": True,
                "order": 5,
                "explanation": ""
            }
        ],

        "tags": [
            {
                "name": "Array",
                "category": "topic"
            },
            {
                "name": "Hash Table",
                "category": "topic"
            },
            {
                "name": "Google",
                "category": "company"
            },
            {
                "name": "Amazon",
                "category": "company"
            }
        ],

        "snippets": [
            {
                "code": "class Solution:\n    def twoSum(self, nums, target):\n        pass",
                "lang": "python",
                "compiler_language_id": 71
            },
            {
                "code": "class Solution {\n    public int[] twoSum(int[] nums, int target) {\n        return new int[]{};\n    }\n}",
                "lang": "java",
                "compiler_language_id": 63
            },
            {
                "code": "class Solution {\npublic:\n    vector<int> twoSum(vector<int>& nums, int target) {\n        return {};\n    }\n};",
                "lang": "cpp",
                "compiler_language_id": 42
            }
        ]
    }



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
            content=c.get('description'),
            order=h.get('order'),
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





    
