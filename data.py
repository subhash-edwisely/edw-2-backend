problem_1 = {
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
                "compiler_language_id": 62
            },
            {
                "code": "class Solution {\npublic:\n    vector<int> twoSum(vector<int>& nums, int target) {\n        return {};\n    }\n};",
                "lang": "cpp",
                "compiler_language_id": 54
            }
        ]
    }





# ---------------------------------------------------------------------






problem_2 = {
    "title": "Reverse Linked List",
    "description": "Given the head of a singly linked list, reverse the list, and return the reversed list.\n\nA singly linked list is a data structure where each node contains a value and a pointer to the next node in the sequence.",
    "xpReward": 15,
    "difficulty": "Easy",
    "hints": [
        {
            "content": "Think about using three pointers: previous, current, and next.",
            "order": 1
        },
        {
            "content": "You need to change the direction of the 'next' pointers as you traverse the list.",
            "order": 2
        },
        {
            "content": "Don't forget to handle the edge case of an empty list or a single node.",
            "order": 3
        },
        {
            "content": "Consider solving this both iteratively and recursively for practice.",
            "order": 4
        }
    ],
    "constraints": [
        {
            "description": "The number of nodes in the list is in the range [0, 5000]",
            "order": 1
        },
        {
            "description": "-5000 <= Node.val <= 5000",
            "order": 2
        }
    ],
    "editorial": {
        "title": "Reverse Linked List",
        "overview": """
The **Reverse Linked List** problem is a fundamental linked list manipulation problem that tests your understanding of pointer operations.

The goal is to reverse the direction of all the 'next' pointers in a singly linked list, making the last node become the first and vice versa.

### Key Approaches:
- Iterative approach using three pointers
- Recursive approach using the call stack
- Both solutions achieve O(n) time complexity

This problem is frequently asked in technical interviews and serves as a building block for more complex linked list problems.
        """,
        "approaches": [
            {
                "id": "iterative",
                "title": "Approach 1: Iterative Solution",
                "explanation": """
The iterative approach uses three pointers to reverse the list in a single pass.

### Algorithm
1. Initialize three pointers: `prev = None`, `current = head`, `next = None`
2. Iterate through the list:
   - Save the next node: `next = current.next`
   - Reverse the pointer: `current.next = prev`
   - Move prev forward: `prev = current`
   - Move current forward: `current = next`
3. Return `prev` as the new head

### Why it works
At each step, we're breaking the forward link and creating a backward link. By the time we finish traversing, all links are reversed.

### Visualization
Original: 1 -> 2 -> 3 -> None
Step 1:   None <- 1    2 -> 3 -> None
Step 2:   None <- 1 <- 2    3 -> None
Step 3:   None <- 1 <- 2 <- 3

### Complexity
- Time: O(n) - single pass through the list
- Space: O(1) - only using three pointers
            """,
                "code": {
                    "python": """
class Solution:
    def reverseList(self, head):
        prev = None
        current = head
        
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        
        return prev
            """,
                    "java": """
class Solution {
    public ListNode reverseList(ListNode head) {
        ListNode prev = null;
        ListNode current = head;
        
        while (current != null) {
            ListNode nextNode = current.next;
            current.next = prev;
            prev = current;
            current = nextNode;
        }
        
        return prev;
    }
}
            """,
                    "cpp": """
class Solution {
public:
    ListNode* reverseList(ListNode* head) {
        ListNode* prev = nullptr;
        ListNode* current = head;
        
        while (current != nullptr) {
            ListNode* nextNode = current->next;
            current->next = prev;
            prev = current;
            current = nextNode;
        }
        
        return prev;
    }
};
            """
                }
            },
            {
                "id": "recursive",
                "title": "Approach 2: Recursive Solution",
                "explanation": """
The recursive approach leverages the call stack to reverse the list from the end backwards.

### Key Idea
The recursion goes deep until it reaches the last node, which becomes the new head. As the recursion unwinds, each node's next pointer is reversed.

### Algorithm
1. Base case: if head is None or head.next is None, return head
2. Recursively call reverseList on head.next to get the new head
3. Set head.next.next = head (reverse the link)
4. Set head.next = None (break the old link)
5. Return the new head

### How it works
The recursion reaches the last node first, making it the new head. As we return from each recursive call, we reverse the pointer of the current node.

### Example trace (for 1->2->3):
- Call reverseList(1): waits for reverseList(2)
- Call reverseList(2): waits for reverseList(3)
- Call reverseList(3): returns 3 (base case)
- Back in reverseList(2): set 3.next = 2, return 3
- Back in reverseList(1): set 2.next = 1, return 3
- Result: 3->2->1->None

### Complexity
- Time: O(n) - visiting each node once
- Space: O(n) - recursion call stack depth
            """,
                "code": {
                    "python": """
class Solution:
    def reverseList(self, head):
        # Base case: empty list or single node
        if not head or not head.next:
            return head
        
        # Recursively reverse the rest of the list
        new_head = self.reverseList(head.next)
        
        # Reverse the pointer
        head.next.next = head
        head.next = None
        
        return new_head
            """,
                    "java": """
class Solution {
    public ListNode reverseList(ListNode head) {
        // Base case: empty list or single node
        if (head == null || head.next == null) {
            return head;
        }
        
        // Recursively reverse the rest of the list
        ListNode newHead = reverseList(head.next);
        
        // Reverse the pointer
        head.next.next = head;
        head.next = null;
        
        return newHead;
    }
}
            """,
                    "cpp": """
class Solution {
public:
    ListNode* reverseList(ListNode* head) {
        // Base case: empty list or single node
        if (head == nullptr || head->next == nullptr) {
            return head;
        }
        
        // Recursively reverse the rest of the list
        ListNode* newHead = reverseList(head->next);
        
        // Reverse the pointer
        head->next->next = head;
        head->next = nullptr;
        
        return newHead;
    }
};
            """
                }
            }
        ],
        "videoUrl": "https://www.youtube.com/watch?v=N_Y4lZBEi0g"
    },
    "testcases": [
        {
            "input": "[1,2,3,4,5]",
            "expectedOutput": "[5,4,3,2,1]",
            "isHidden": False,
            "order": 1,
            "explanation": "The list is reversed: 5 becomes the head, followed by 4, 3, 2, and 1."
        },
        {
            "input": "[1,2]",
            "expectedOutput": "[2,1]",
            "isHidden": False,
            "order": 2,
            "explanation": "Simple two-node reversal."
        },
        {
            "input": "[]",
            "expectedOutput": "[]",
            "isHidden": False,
            "order": 3,
            "explanation": "Empty list remains empty."
        },
        {
            "input": "[1]",
            "expectedOutput": "[1]",
            "isHidden": True,
            "order": 4,
            "explanation": "Single node list remains unchanged."
        },
        {
            "input": "[1,2,3,4,5,6,7,8,9,10]",
            "expectedOutput": "[10,9,8,7,6,5,4,3,2,1]",
            "isHidden": True,
            "order": 5,
            "explanation": "Longer list reversal test."
        }
    ],
    "tags": [
        {
            "name": "Linked List",
            "category": "topic"
        },
        {
            "name": "Recursion",
            "category": "topic"
        },
        {
            "name": "Facebook",
            "category": "company"
        },
        {
            "name": "Microsoft",
            "category": "company"
        },
        {
            "name": "Amazon",
            "category": "company"
        }
    ],
    "snippets": [
        {
            "code": "# Definition for singly-linked list.\n# class ListNode:\n#     def __init__(self, val=0, next=None):\n#         self.val = val\n#         self.next = next\nclass Solution:\n    def reverseList(self, head):\n        pass",
            "lang": "python",
            "compiler_language_id": 71
        },
        {
            "code": "/**\n * Definition for singly-linked list.\n * public class ListNode {\n *     int val;\n *     ListNode next;\n *     ListNode() {}\n *     ListNode(int val) { this.val = val; }\n *     ListNode(int val, ListNode next) { this.val = val; this.next = next; }\n * }\n */\nclass Solution {\n    public ListNode reverseList(ListNode head) {\n        return null;\n    }\n}",
            "lang": "java",
            "compiler_language_id": 62
        },
        {
            "code": "/**\n * Definition for singly-linked list.\n * struct ListNode {\n *     int val;\n *     ListNode *next;\n *     ListNode() : val(0), next(nullptr) {}\n *     ListNode(int x) : val(x), next(nullptr) {}\n *     ListNode(int x, ListNode *next) : val(x), next(next) {}\n * };\n */\nclass Solution {\npublic:\n    ListNode* reverseList(ListNode* head) {\n        return nullptr;\n    }\n};",
            "lang": "cpp",
            "compiler_language_id": 54
        }
    ]
}


########################################################################






problem_3 = {
    "title": "Valid Parentheses",
    "description": "Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.\n\nAn input string is valid if:\n1. Open brackets must be closed by the same type of brackets.\n2. Open brackets must be closed in the correct order.\n3. Every close bracket has a corresponding open bracket of the same type.",
    "xpReward": 12,
    "difficulty": "Easy",
    "hints": [
        {
            "content": "A stack is the perfect data structure for this problem.",
            "order": 1
        },
        {
            "content": "When you encounter an opening bracket, push it onto the stack.",
            "order": 2
        },
        {
            "content": "When you encounter a closing bracket, check if it matches the top of the stack.",
            "order": 3
        },
        {
            "content": "At the end, the stack should be empty for the string to be valid.",
            "order": 4
        }
    ],
    "constraints": [
        {
            "description": "1 <= s.length <= 10^4",
            "order": 1
        },
        {
            "description": "s consists of parentheses only '()[]{}'",
            "order": 2
        }
    ],
    "editorial": {
        "title": "Valid Parentheses",
        "overview": """
The **Valid Parentheses** problem is a classic stack-based problem that tests your understanding of Last-In-First-Out (LIFO) data structures.

The challenge is to ensure that every opening bracket has a corresponding closing bracket of the same type, and they are properly nested.

### Examples of valid strings:
- "()" - simple pair
- "()[]{}" - multiple types properly ordered
- "{[]}" - properly nested

### Examples of invalid strings:
- "(]" - wrong closing bracket
- "([)]" - improper nesting
- "(((" - missing closing brackets

### Key Insight:
The most recently opened bracket must be closed first. This LIFO behavior makes a stack the perfect data structure.
        """,
        "approaches": [
            {
                "id": "stack_approach",
                "title": "Approach 1: Stack-Based Solution",
                "explanation": """
We use a stack to keep track of opening brackets and match them with their corresponding closing brackets.

### Algorithm
1. Create an empty stack
2. Create a mapping of closing to opening brackets: {')': '(', '}': '{', ']': '['}
3. Iterate through each character in the string:
   - If it's an opening bracket '(', '{', or '[', push it onto the stack
   - If it's a closing bracket:
     - Check if the stack is empty (invalid case)
     - Pop from the stack and check if it matches the expected opening bracket
     - If it doesn't match, return False
4. After processing all characters, check if the stack is empty
   - If empty: all brackets were properly matched (return True)
   - If not empty: some opening brackets weren't closed (return False)

### Why it works
The stack naturally handles the "most recent opening bracket must be closed first" requirement. When we encounter a closing bracket, we check against the most recently added opening bracket (top of stack).

### Example Walkthrough: "{[()]}"
- Read '{': push to stack → ['{']]
- Read '[': push to stack → ['{', '[']
- Read '(': push to stack → ['{', '[', '(']
- Read ')': matches '(' on top → pop → ['{', '[']
- Read ']': matches '[' on top → pop → ['{']
- Read '}': matches '{' on top → pop → []
- Stack is empty → Valid!

### Complexity
- Time: O(n) - single pass through the string
- Space: O(n) - worst case all opening brackets
            """,
                "code": {
                    "python": """
class Solution:
    def isValid(self, s):
        stack = []
        mapping = {')': '(', '}': '{', ']': '['}
        
        for char in s:
            if char in mapping:
                # It's a closing bracket
                top_element = stack.pop() if stack else '#'
                
                if mapping[char] != top_element:
                    return False
            else:
                # It's an opening bracket
                stack.append(char)
        
        return not stack
            """,
                    "java": """
class Solution {
    public boolean isValid(String s) {
        Stack<Character> stack = new Stack<>();
        Map<Character, Character> mapping = new HashMap<>();
        mapping.put(')', '(');
        mapping.put('}', '{');
        mapping.put(']', '[');
        
        for (char c : s.toCharArray()) {
            if (mapping.containsKey(c)) {
                // It's a closing bracket
                char topElement = stack.isEmpty() ? '#' : stack.pop();
                
                if (topElement != mapping.get(c)) {
                    return false;
                }
            } else {
                // It's an opening bracket
                stack.push(c);
            }
        }
        
        return stack.isEmpty();
    }
}
            """,
                    "cpp": """
class Solution {
public:
    bool isValid(string s) {
        stack<char> st;
        unordered_map<char, char> mapping = {
            {')', '('},
            {'}', '{'},
            {']', '['}
        };
        
        for (char c : s) {
            if (mapping.count(c)) {
                // It's a closing bracket
                char topElement = st.empty() ? '#' : st.top();
                if (!st.empty()) st.pop();
                
                if (mapping[c] != topElement) {
                    return false;
                }
            } else {
                // It's an opening bracket
                st.push(c);
            }
        }
        
        return st.empty();
    }
};
            """
                }
            },
            {
                "id": "optimized_stack",
                "title": "Approach 2: Optimized Stack (No HashMap)",
                "explanation": """
We can optimize the solution slightly by avoiding the hash map lookup.

### Key Idea
Instead of storing opening brackets in the stack, we can store their corresponding closing brackets. This way, when we encounter a closing bracket, we just compare it directly with the top of the stack.

### Algorithm
1. Create an empty stack
2. For each character:
   - If '(', push ')' onto stack
   - If '{', push '}' onto stack
   - If '[', push ']' onto stack
   - If it's a closing bracket:
     - Check if stack is empty OR top doesn't match current char → return False
     - Otherwise pop from stack
3. Return whether stack is empty

### Why this works
By storing the expected closing bracket, we eliminate the need for a hash map lookup. The comparison becomes a simple equality check.

### Example: "([)]"
- Read '(': push ')' → [')']
- Read '[': push ']' → [')', ']']
- Read ')': top is ']', doesn't match → return False

### Complexity
- Time: O(n) - single pass through the string
- Space: O(n) - stack space in worst case
            """,
                "code": {
                    "python": """
class Solution:
    def isValid(self, s):
        stack = []
        
        for char in s:
            if char == '(':
                stack.append(')')
            elif char == '{':
                stack.append('}')
            elif char == '[':
                stack.append(']')
            elif not stack or stack.pop() != char:
                return False
        
        return len(stack) == 0
            """,
                    "java": """
class Solution {
    public boolean isValid(String s) {
        Stack<Character> stack = new Stack<>();
        
        for (char c : s.toCharArray()) {
            if (c == '(') {
                stack.push(')');
            } else if (c == '{') {
                stack.push('}');
            } else if (c == '[') {
                stack.push(']');
            } else if (stack.isEmpty() || stack.pop() != c) {
                return false;
            }
        }
        
        return stack.isEmpty();
    }
}
            """,
                    "cpp": """
class Solution {
public:
    bool isValid(string s) {
        stack<char> st;
        
        for (char c : s) {
            if (c == '(') {
                st.push(')');
            } else if (c == '{') {
                st.push('}');
            } else if (c == '[') {
                st.push(']');
            } else if (st.empty() || st.top() != c) {
                return false;
            } else {
                st.pop();
            }
        }
        
        return st.empty();
    }
};
            """
                }
            }
        ],
        "videoUrl": "https://www.youtube.com/watch?v=WTzjTskDFMg"
    },
    "testcases": [
        {
            "input": "\"()\"",
            "expectedOutput": "true",
            "isHidden": False,
            "order": 1,
            "explanation": "Simple valid pair of parentheses."
        },
        {
            "input": "\"()[]{}\"",
            "expectedOutput": "true",
            "isHidden": False,
            "order": 2,
            "explanation": "Multiple types of brackets, all properly matched."
        },
        {
            "input": "\"(]\"",
            "expectedOutput": "false",
            "isHidden": False,
            "order": 3,
            "explanation": "Opening '(' is closed with ']' which doesn't match."
        },
        {
            "input": "\"([)]\"",
            "expectedOutput": "false",
            "isHidden": True,
            "order": 4,
            "explanation": "Brackets are interleaved incorrectly - '[' should be closed before ')'."
        },
        {
            "input": "\"{[]}\"",
            "expectedOutput": "true",
            "isHidden": True,
            "order": 5,
            "explanation": "Properly nested brackets."
        },
        {
            "input": "\"((((\"",
            "expectedOutput": "false",
            "isHidden": True,
            "order": 6,
            "explanation": "Opening brackets without any closing brackets."
        }
    ],
    "tags": [
        {
            "name": "Stack",
            "category": "topic"
        },
        {
            "name": "String",
            "category": "topic"
        },
        {
            "name": "Google",
            "category": "company"
        },
        {
            "name": "Facebook",
            "category": "company"
        },
        {
            "name": "Amazon",
            "category": "company"
        },
        {
            "name": "Microsoft",
            "category": "company"
        }
    ],
    "snippets": [
        {
            "code": "class Solution:\n    def isValid(self, s):\n        pass",
            "lang": "python",
            "compiler_language_id": 71
        },
        {
            "code": "class Solution {\n    public boolean isValid(String s) {\n        return false;\n    }\n}",
            "lang": "java",
            "compiler_language_id": 62
        },
        {
            "code": "class Solution {\npublic:\n    bool isValid(string s) {\n        return false;\n    }\n};",
            "lang": "cpp",
            "compiler_language_id": 54
        }
    ]
}









###########################################################












problem_4 = {
    "title": "Merge Two Sorted Lists",
    "description": "You are given the heads of two sorted linked lists list1 and list2.\n\nMerge the two lists into one sorted list. The list should be made by splicing together the nodes of the first two lists.\n\nReturn the head of the merged linked list.",
    "xpReward": 15,
    "difficulty": "Medium",
    "hints": [
        {
            "content": "Use a dummy node to simplify edge cases and make the code cleaner.",
            "order": 1
        },
        {
            "content": "Compare the values at the current positions of both lists and attach the smaller one.",
            "order": 2
        },
        {
            "content": "Don't forget to attach any remaining nodes from either list after one becomes empty.",
            "order": 3
        },
        {
            "content": "This problem can also be solved recursively - think about the base case and recursive relation.",
            "order": 4
        }
    ],
    "constraints": [
        {
            "description": "The number of nodes in both lists is in the range [0, 50]",
            "order": 1
        },
        {
            "description": "-100 <= Node.val <= 100",
            "order": 2
        },
        {
            "description": "Both list1 and list2 are sorted in non-decreasing order",
            "order": 3
        }
    ],
    "editorial": {
        "title": "Merge Two Sorted Lists",
        "overview": """
The **Merge Two Sorted Lists** problem is a fundamental linked list problem that combines two pre-sorted lists into a single sorted list.

This problem is similar to the merge step in merge sort and teaches important concepts about:
- Linked list manipulation
- Pointer management
- Maintaining sorted order while merging

### Key Challenge:
We need to traverse both lists simultaneously, comparing values and building a new merged list while preserving the sorted order.

### Example:
Input: list1 = [1,2,4], list2 = [1,3,4]
Output: [1,1,2,3,4,4]

### Approaches:
- Iterative solution using a dummy node
- Recursive solution leveraging the call stack
        """,
        "approaches": [
            {
                "id": "iterative_dummy",
                "title": "Approach 1: Iterative with Dummy Node",
                "explanation": """
We use a dummy node to simplify the logic and avoid special cases for the head of the result list.

### Algorithm
1. Create a dummy node to serve as the start of the merged list
2. Create a current pointer initialized to the dummy node
3. While both list1 and list2 are not None:
   - Compare list1.val and list2.val
   - Attach the smaller node to current.next
   - Move the pointer of the list from which we took the node
   - Move current to current.next
4. After the loop, one or both lists may be exhausted
5. Attach the remaining nodes from whichever list is not empty
6. Return dummy.next (the actual head of merged list)

### Why use a dummy node?
Without a dummy node, we'd need special logic to handle the first node of the result. The dummy node lets us treat all nodes uniformly.

### Example Walkthrough: list1=[1,2,4], list2=[1,3,4]
- dummy -> None, current = dummy
- Compare 1 and 1: take from list1 → dummy -> 1
- Compare 2 and 1: take 1 from list2 → dummy -> 1 -> 1
- Compare 2 and 3: take 2 from list1 → dummy -> 1 -> 1 -> 2
- Compare 4 and 3: take 3 from list2 → dummy -> 1 -> 1 -> 2 -> 3
- Compare 4 and 4: take from list1 → dummy -> 1 -> 1 -> 2 -> 3 -> 4
- list1 empty, attach remaining list2 → dummy -> 1 -> 1 -> 2 -> 3 -> 4 -> 4

### Complexity
- Time: O(n + m) where n and m are the lengths of the two lists
- Space: O(1) - only using pointers, not creating new nodes
            """,
                "code": {
                    "python": """
class Solution:
    def mergeTwoLists(self, list1, list2):
        # Create a dummy node
        dummy = ListNode(0)
        current = dummy
        
        # Traverse both lists
        while list1 and list2:
            if list1.val <= list2.val:
                current.next = list1
                list1 = list1.next
            else:
                current.next = list2
                list2 = list2.next
            current = current.next
        
        # Attach remaining nodes
        if list1:
            current.next = list1
        else:
            current.next = list2
        
        return dummy.next
            """,
                    "java": """
class Solution {
    public ListNode mergeTwoLists(ListNode list1, ListNode list2) {
        // Create a dummy node
        ListNode dummy = new ListNode(0);
        ListNode current = dummy;
        
        // Traverse both lists
        while (list1 != null && list2 != null) {
            if (list1.val <= list2.val) {
                current.next = list1;
                list1 = list1.next;
            } else {
                current.next = list2;
                list2 = list2.next;
            }
            current = current.next;
        }
        
        // Attach remaining nodes
        if (list1 != null) {
            current.next = list1;
        } else {
            current.next = list2;
        }
        
        return dummy.next;
    }
}
            """,
                    "cpp": """
class Solution {
public:
    ListNode* mergeTwoLists(ListNode* list1, ListNode* list2) {
        // Create a dummy node
        ListNode* dummy = new ListNode(0);
        ListNode* current = dummy;
        
        // Traverse both lists
        while (list1 != nullptr && list2 != nullptr) {
            if (list1->val <= list2->val) {
                current->next = list1;
                list1 = list1->next;
            } else {
                current->next = list2;
                list2 = list2->next;
            }
            current = current->next;
        }
        
        // Attach remaining nodes
        if (list1 != nullptr) {
            current->next = list1;
        } else {
            current->next = list2;
        }
        
        return dummy->next;
    }
};
            """
                }
            },
            {
                "id": "recursive",
                "title": "Approach 2: Recursive Solution",
                "explanation": """
The recursive approach elegantly solves the problem by breaking it down into smaller subproblems.

### Key Idea
At each step, we choose the smaller head and recursively merge the rest. The base cases handle when one or both lists are empty.

### Algorithm
1. Base cases:
   - If list1 is None, return list2
   - If list2 is None, return list1
2. Recursive case:
   - If list1.val <= list2.val:
     - Set list1.next = mergeTwoLists(list1.next, list2)
     - Return list1
   - Otherwise:
     - Set list2.next = mergeTwoLists(list1, list2.next)
     - Return list2

### How it works
Each recursive call selects the smaller head and merges it with the result of merging the remaining lists. The recursion naturally builds the merged list from smallest to largest.

### Example Trace: list1=[1,4], list2=[2,3]
- mergeTwoLists([1,4], [2,3])
  - 1 <= 2, so take 1
  - 1.next = mergeTwoLists([4], [2,3])
    - 4 > 2, so take 2
    - 2.next = mergeTwoLists([4], [3])
      - 4 > 3, so take 3
      - 3.next = mergeTwoLists([4], None)
        - Returns [4]
      - Returns [3,4]
    - Returns [2,3,4]
  - Returns [1,2,3,4]

### Complexity
- Time: O(n + m) - each node is visited once
- Space: O(n + m) - recursion call stack depth
            """,
                "code": {
                    "python": """
class Solution:
    def mergeTwoLists(self, list1, list2):
        # Base cases
        if not list1:
            return list2
        if not list2:
            return list1
        
        # Recursive case
        if list1.val <= list2.val:
            list1.next = self.mergeTwoLists(list1.next, list2)
            return list1
        else:
            list2.next = self.mergeTwoLists(list1, list2.next)
            return list2
            """,
                    "java": """
class Solution {
    public ListNode mergeTwoLists(ListNode list1, ListNode list2) {
        // Base cases
        if (list1 == null) {
            return list2;
        }
        if (list2 == null) {
            return list1;
        }
        
        // Recursive case
        if (list1.val <= list2.val) {
            list1.next = mergeTwoLists(list1.next, list2);
            return list1;
        } else {
            list2.next = mergeTwoLists(list1, list2.next);
            return list2;
        }
    }
}
            """,
                    "cpp": """
class Solution {
public:
    ListNode* mergeTwoLists(ListNode* list1, ListNode* list2) {
        // Base cases
        if (list1 == nullptr) {
            return list2;
        }
        if (list2 == nullptr) {
            return list1;
        }
        
        // Recursive case
        if (list1->val <= list2->val) {
            list1->next = mergeTwoLists(list1->next, list2);
            return list1;
        } else {
            list2->next = mergeTwoLists(list1, list2->next);
            return list2;
        }
    }
};
            """
                }
            }
        ],
        "videoUrl": "https://www.youtube.com/watch?v=XIdigk956u0"
    },
    "testcases": [
        {
            "input": "[1,2,4]\n[1,3,4]",
            "expectedOutput": "[1,1,2,3,4,4]",
            "isHidden": False,
            "order": 1,
            "explanation": "Both lists have common values and need proper interleaving."
        },
        {
            "input": "[]\n[]",
            "expectedOutput": "[]",
            "isHidden": False,
            "order": 2,
            "explanation": "Both lists are empty."
        },
        {
            "input": "[]\n[0]",
            "expectedOutput": "[0]",
            "isHidden": False,
            "order": 3,
            "explanation": "One list is empty, return the other."
        },
        {
            "input": "[1,2,3]\n[4,5,6]",
            "expectedOutput": "[1,2,3,4,5,6]",
            "isHidden": True,
            "order": 4,
            "explanation": "All elements of list1 come before all elements of list2."
        },
        {
            "input": "[5]\n[1,2,4]",
            "expectedOutput": "[1,2,4,5]",
            "isHidden": True,
            "order": 5,
            "explanation": "Single element list merged with multi-element list."
        },
        {
            "input": "[-9,-7,-3,-3,0,0,0,1]\n[-10,-6,-4,-1]",
            "expectedOutput": "[-10,-9,-7,-6,-4,-3,-3,-1,0,0,0,1]",
            "isHidden": True,
            "order": 6,
            "explanation": "Lists with negative numbers and duplicates."
        }
    ],
    "tags": [
        {
            "name": "Linked List",
            "category": "topic"
        },
        {
            "name": "Recursion",
            "category": "topic"
        },
        {
            "name": "Two Pointers",
            "category": "topic"
        },
        {
            "name": "Amazon",
            "category": "company"
        },
        {
            "name": "Microsoft",
            "category": "company"
        },
        {
            "name": "Apple",
            "category": "company"
        }
    ],
    "snippets": [
        {
            "code": "# Definition for singly-linked list.\n# class ListNode:\n#     def __init__(self, val=0, next=None):\n#         self.val = val\n#         self.next = next\nclass Solution:\n    def mergeTwoLists(self, list1, list2):\n        pass",
            "lang": "python",
            "compiler_language_id": 71
        },
        {
            "code": "/**\n * Definition for singly-linked list.\n * public class ListNode {\n *     int val;\n *     ListNode next;\n *     ListNode() {}\n *     ListNode(int val) { this.val = val; }\n *     ListNode(int val, ListNode next) { this.val = val; this.next = next; }\n * }\n */\nclass Solution {\n    public ListNode mergeTwoLists(ListNode list1, ListNode list2) {\n        return null;\n    }\n}",
            "lang": "java",
            "compiler_language_id": 62
        },
        {
            "code": "/**\n * Definition for singly-linked list.\n * struct ListNode {\n *     int val;\n *     ListNode *next;\n *     ListNode() : val(0), next(nullptr) {}\n *     ListNode(int x) : val(x), next(nullptr) {}\n *     ListNode(int x, ListNode *next) : val(x), next(next) {}\n * };\n */\nclass Solution {\npublic:\n    ListNode* mergeTwoLists(ListNode* list1, ListNode* list2) {\n        return nullptr;\n    }\n};",
            "lang": "cpp",
            "compiler_language_id": 54
        }
    ]
}








#############################################################################









problem_5 = {
    "title": "Best Time to Buy and Sell Stock",
    "description": "You are given an array prices where prices[i] is the price of a given stock on the ith day.\n\nYou want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock.\n\nReturn the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return 0.",
    "xpReward": 12,
    "difficulty": "Hard",
    "hints": [
        {
            "content": "Think about tracking the minimum price seen so far as you iterate through the array.",
            "order": 1
        },
        {
            "content": "For each price, calculate the profit if you sold at that price having bought at the minimum price.",
            "order": 2
        },
        {
            "content": "Keep track of the maximum profit seen so far.",
            "order": 3
        },
        {
            "content": "You can solve this in a single pass through the array with O(1) space.",
            "order": 4
        }
    ],
    "constraints": [
        {
            "description": "1 <= prices.length <= 10^5",
            "order": 1
        },
        {
            "description": "0 <= prices[i] <= 10^4",
            "order": 2
        }
    ],
    "editorial": {
        "title": "Best Time to Buy and Sell Stock",
        "overview": """
The **Best Time to Buy and Sell Stock** problem is a classic dynamic programming and greedy algorithm problem that teaches important concepts about optimization.

### Problem Essence:
We need to find the maximum difference between two elements in the array where the larger element comes after the smaller one. This represents buying at a low price and selling at a higher price later.

### Key Insights:
- We must buy before we sell (can't go back in time)
- We want to buy at the lowest price and sell at the highest price after that
- We need to track both the minimum price so far and the maximum profit

### Examples:
Input: [7,1,5,3,6,4]
- Buy on day 2 (price = 1), sell on day 5 (price = 6), profit = 6-1 = 5

Input: [7,6,4,3,1]
- No profitable transaction possible, return 0

### Approaches:
- Brute force checking all pairs
- One-pass greedy solution (optimal)
        """,
        "approaches": [
            {
                "id": "brute_force",
                "title": "Approach 1: Brute Force",
                "explanation": """
The straightforward approach is to try every possible buy-sell pair and find the maximum profit.

### Algorithm
1. Initialize maxProfit = 0
2. Use two nested loops:
   - Outer loop: iterate through each day i as the buy day
   - Inner loop: iterate through each day j > i as the sell day
   - Calculate profit = prices[j] - prices[i]
   - Update maxProfit if this profit is greater
3. Return maxProfit

### Why it works
By checking every possible combination, we're guaranteed to find the maximum profit if one exists.

### Example: [7,1,5,3,6,4]
- Buy at 7: sell at 1→-6, 5→-2, 3→-4, 6→-1, 4→-3
- Buy at 1: sell at 5→4, 3→2, 6→5, 4→3 (max so far: 5)
- Buy at 5: sell at 3→-2, 6→1, 4→-1
- Buy at 3: sell at 6→3, 4→1
- Buy at 6: sell at 4→-2
- Maximum profit: 5

### Complexity
- Time: O(n²) - nested loops checking all pairs
- Space: O(1) - only storing variables

### Note
This approach works but is inefficient for large inputs. It will likely exceed time limits on larger test cases.
            """,
                "code": {
                    "python": """
class Solution:
    def maxProfit(self, prices):
        max_profit = 0
        
        for i in range(len(prices)):
            for j in range(i + 1, len(prices)):
                profit = prices[j] - prices[i]
                max_profit = max(max_profit, profit)
        
        return max_profit
            """,
                    "java": """
class Solution {
    public int maxProfit(int[] prices) {
        int maxProfit = 0;
        
        for (int i = 0; i < prices.length; i++) {
            for (int j = i + 1; j < prices.length; j++) {
                int profit = prices[j] - prices[i];
                maxProfit = Math.max(maxProfit, profit);
            }
        }
        
        return maxProfit;
    }
}
            """,
                    "cpp": """
class Solution {
public:
    int maxProfit(vector<int>& prices) {
        int maxProfit = 0;
        
        for (int i = 0; i < prices.size(); i++) {
            for (int j = i + 1; j < prices.size(); j++) {
                int profit = prices[j] - prices[i];
                maxProfit = max(maxProfit, profit);
            }
        }
        
        return maxProfit;
    }
};
            """
                }
            },
            {
                "id": "one_pass_optimal",
                "title": "Approach 2: One Pass (Optimal)",
                "explanation": """
We can solve this problem optimally in a single pass by tracking the minimum price seen so far and calculating potential profit at each step.

### Key Idea
As we scan through prices:
- Keep track of the minimum price encountered so far (best buy price)
- For each price, calculate what profit we'd make if we sold at this price
- Update the maximum profit if this profit is better

### Algorithm
1. Initialize minPrice = infinity (or first price)
2. Initialize maxProfit = 0
3. For each price in prices:
   - If price < minPrice, update minPrice (found a better buy day)
   - Calculate currentProfit = price - minPrice
   - If currentProfit > maxProfit, update maxProfit
4. Return maxProfit

### Why it works
At each day, we know the best price to buy before that day (minPrice). We calculate the profit if we sold today and keep track of the best profit we've seen.

### Example Walkthrough: [7,1,5,3,6,4]
- Day 0 (price=7): minPrice=7, profit=0, maxProfit=0
- Day 1 (price=1): minPrice=1, profit=0, maxProfit=0
- Day 2 (price=5): minPrice=1, profit=4, maxProfit=4
- Day 3 (price=3): minPrice=1, profit=2, maxProfit=4
- Day 4 (price=6): minPrice=1, profit=5, maxProfit=5
- Day 5 (price=4): minPrice=1, profit=3, maxProfit=5
- Result: 5

### Visual Representation:
```
Prices: [7, 1, 5, 3, 6, 4]
         ↓  ↓           ↓
        Buy here    Sell here
         (min=1)    (profit=5)
```

### Complexity
- Time: O(n) - single pass through the array
- Space: O(1) - only using two variables
            """,
                "code": {
                    "python": """
class Solution:
    def maxProfit(self, prices):
        min_price = float('inf')
        max_profit = 0
        
        for price in prices:
            # Update minimum price if we found a lower one
            if price < min_price:
                min_price = price
            # Calculate profit if we sell at current price
            elif price - min_price > max_profit:
                max_profit = price - min_price
        
        return max_profit
            """,
                    "java": """
class Solution {
    public int maxProfit(int[] prices) {
        int minPrice = Integer.MAX_VALUE;
        int maxProfit = 0;
        
        for (int price : prices) {
            // Update minimum price if we found a lower one
            if (price < minPrice) {
                minPrice = price;
            } 
            // Calculate profit if we sell at current price
            else if (price - minPrice > maxProfit) {
                maxProfit = price - minPrice;
            }
        }
        
        return maxProfit;
    }
}
            """,
                    "cpp": """
class Solution {
public:
    int maxProfit(vector<int>& prices) {
        int minPrice = INT_MAX;
        int maxProfit = 0;
        
        for (int price : prices) {
            // Update minimum price if we found a lower one
            if (price < minPrice) {
                minPrice = price;
            } 
            // Calculate profit if we sell at current price
            else if (price - minPrice > maxProfit) {
                maxProfit = price - minPrice;
            }
        }
        
        return maxProfit;
    }
};
            """
                }
            }
        ],
        "videoUrl": "https://www.youtube.com/watch?v=1pkOgXD63yU"
    },
    "testcases": [
        {
            "input": "[7,1,5,3,6,4]",
            "expectedOutput": "5",
            "isHidden": False,
            "order": 1,
            "explanation": "Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6-1 = 5."
        },
        {
            "input": "[7,6,4,3,1]",
            "expectedOutput": "0",
            "isHidden": False,
            "order": 2,
            "explanation": "Prices only decrease, so no profit can be made."
        },
        {
            "input": "[2,4,1]",
            "expectedOutput": "2",
            "isHidden": False,
            "order": 3,
            "explanation": "Buy on day 1 (price = 2) and sell on day 2 (price = 4), profit = 2."
        },
        {
            "input": "[3,2,6,5,0,3]",
            "expectedOutput": "4",
            "isHidden": True,
            "order": 4,
            "explanation": "Buy on day 2 (price = 2) and sell on day 3 (price = 6), profit = 4."
        },
        {
            "input": "[1,2,3,4,5]",
            "expectedOutput": "4",
            "isHidden": True,
            "order": 5,
            "explanation": "Buy on day 1 (price = 1) and sell on day 5 (price = 5), profit = 4."
        },
        {
            "input": "[2,1,2,0,1]",
            "expectedOutput": "1",
            "isHidden": True,
            "order": 6,
            "explanation": "Multiple valid transactions, but max profit is 1 (buy at 0, sell at 1)."
        }
    ],
    "tags": [
        {
            "name": "Array",
            "category": "topic"
        },
        {
            "name": "Dynamic Programming",
            "category": "topic"
        },
        {
            "name": "Greedy",
            "category": "topic"
        },
        {
            "name": "Amazon",
            "category": "company"
        },
        {
            "name": "Facebook",
            "category": "company"
        },
        {
            "name": "Microsoft",
            "category": "company"
        },
        {
            "name": "Goldman Sachs",
            "category": "company"
        }
    ],
    "snippets": [
        {
            "code": "class Solution:\n    def maxProfit(self, prices):\n        pass",
            "lang": "python",
            "compiler_language_id": 71
        },
        {
            "code": "class Solution {\n    public int maxProfit(int[] prices) {\n        return 0;\n    }\n}",
            "lang": "java",
            "compiler_language_id": 62
        },
        {
            "code": "class Solution {\npublic:\n    int maxProfit(vector<int>& prices) {\n        return 0;\n    }\n};",
            "lang": "cpp",
            "compiler_language_id": 54
        }
    ]
}








###########################################################





problem_6 = {
    "title": "Maximum Subarray",
    "description": "Given an integer array nums, find the subarray with the largest sum, and return its sum.\n\nA subarray is a contiguous non-empty sequence of elements within an array.",
    "xpReward": 18,
    "difficulty": "Medium",
    "hints": [
        {
            "content": "Try using Kadane's Algorithm - it's specifically designed for this problem.",
            "order": 1
        },
        {
            "content": "At each position, decide whether to extend the current subarray or start a new one.",
            "order": 2
        },
        {
            "content": "Keep track of the current sum and the maximum sum seen so far.",
            "order": 3
        },
        {
            "content": "If the current sum becomes negative, it's better to start fresh from the next element.",
            "order": 4
        }
    ],
    "constraints": [
        {
            "description": "1 <= nums.length <= 10^5",
            "order": 1
        },
        {
            "description": "-10^4 <= nums[i] <= 10^4",
            "order": 2
        }
    ],
    "editorial": {
        "title": "Maximum Subarray",
        "overview": """
The **Maximum Subarray** problem, also known as the maximum subarray sum problem, is a classic problem in computer science that demonstrates the power of dynamic programming and greedy algorithms.

### Problem Essence:
Find a contiguous subarray within a one-dimensional array of numbers that has the largest sum.

### Key Insight:
At any position, we face a choice: either extend the existing subarray by including the current element, or start a new subarray from the current element. The decision depends on whether adding to the existing sum helps or hurts.

### Examples:
Input: [-2,1,-3,4,-1,2,1,-5,4]
- The subarray [4,-1,2,1] has the largest sum = 6

Input: [1]
- Only one element, so maximum sum = 1

Input: [5,4,-1,7,8]
- The entire array is the maximum subarray with sum = 23

### Approaches:
- Brute force checking all subarrays
- Kadane's Algorithm (optimal O(n) solution)
- Divide and Conquer approach
        """,
        "approaches": [
            {
                "id": "kadane_algorithm",
                "title": "Approach 1: Kadane's Algorithm (Optimal)",
                "explanation": """
Kadane's Algorithm is an elegant dynamic programming solution that solves this problem in linear time.

### Core Idea
At each position, we maintain:
- `current_sum`: maximum sum of subarray ending at current position
- `max_sum`: maximum sum found so far

The key decision at each element: should we extend the previous subarray or start fresh?

### Algorithm
1. Initialize current_sum = nums[0] and max_sum = nums[0]
2. For each element from index 1 to end:
   - Update current_sum = max(nums[i], current_sum + nums[i])
     - This decides: start new subarray OR extend existing one
   - Update max_sum = max(max_sum, current_sum)
3. Return max_sum

### Why it works
- If current_sum becomes negative, it will only decrease future sums
- Starting fresh from the next positive element is better
- We continuously track the best sum we've seen

### Example Walkthrough: [-2,1,-3,4,-1,2,1,-5,4]
```
Index:  0   1   2   3   4   5   6   7   8
Nums:  -2   1  -3   4  -1   2   1  -5   4
Curr:  -2   1  -2   4   3   5   6   1   5
Max:   -2   1   1   4   4   5   6   6   6
```

- i=0: curr=-2, max=-2
- i=1: curr=max(1, -2+1)=1, max=1
- i=2: curr=max(-3, 1-3)=-2, max=1
- i=3: curr=max(4, -2+4)=4, max=4
- i=4: curr=max(-1, 4-1)=3, max=4
- i=5: curr=max(2, 3+2)=5, max=5
- i=6: curr=max(1, 5+1)=6, max=6
- i=7: curr=max(-5, 6-5)=1, max=6
- i=8: curr=max(4, 1+4)=5, max=6

Result: 6 (subarray [4,-1,2,1])

### Complexity
- Time: O(n) - single pass through array
- Space: O(1) - only two variables
            """,
                "code": {
                    "python": """
class Solution:
    def maxSubArray(self, nums):
        current_sum = max_sum = nums[0]
        
        for i in range(1, len(nums)):
            # Either extend existing subarray or start new one
            current_sum = max(nums[i], current_sum + nums[i])
            # Update maximum sum found so far
            max_sum = max(max_sum, current_sum)
        
        return max_sum
            """,
                    "java": """
class Solution {
    public int maxSubArray(int[] nums) {
        int currentSum = nums[0];
        int maxSum = nums[0];
        
        for (int i = 1; i < nums.length; i++) {
            // Either extend existing subarray or start new one
            currentSum = Math.max(nums[i], currentSum + nums[i]);
            // Update maximum sum found so far
            maxSum = Math.max(maxSum, currentSum);
        }
        
        return maxSum;
    }
}
            """,
                    "cpp": """
class Solution {
public:
    int maxSubArray(vector<int>& nums) {
        int currentSum = nums[0];
        int maxSum = nums[0];
        
        for (int i = 1; i < nums.size(); i++) {
            // Either extend existing subarray or start new one
            currentSum = max(nums[i], currentSum + nums[i]);
            // Update maximum sum found so far
            maxSum = max(maxSum, currentSum);
        }
        
        return maxSum;
    }
};
            """
                }
            },
            {
                "id": "divide_conquer",
                "title": "Approach 2: Divide and Conquer",
                "explanation": """
The divide and conquer approach splits the array and considers three cases for the maximum subarray.

### Key Idea
The maximum subarray can be in three places:
1. Entirely in the left half
2. Entirely in the right half
3. Crosses the middle (spans both halves)

We recursively find the maximum for each case and return the largest.

### Algorithm
1. Base case: if array has one element, return it
2. Find the middle index
3. Recursively find max subarray in left half
4. Recursively find max subarray in right half
5. Find max subarray crossing the middle:
   - Find max sum extending left from middle
   - Find max sum extending right from middle
   - Sum them together
6. Return the maximum of the three values

### Finding Cross Sum
Starting from the middle:
- Extend left: keep track of best sum going left
- Extend right: keep track of best sum going right
- Total cross sum = left_sum + right_sum

### Example: [-2,1,-3,4,-1,2,1,-5,4]
- Split into [-2,1,-3,4] and [-1,2,1,-5,4]
- Continue splitting recursively
- At each level, compare left max, right max, and cross max
- Combine results back up

### Complexity
- Time: O(n log n) - dividing array takes log n levels, each level processes n elements
- Space: O(log n) - recursion stack depth
            """,
                "code": {
                    "python": """
class Solution:
    def maxSubArray(self, nums):
        return self.divideConquer(nums, 0, len(nums) - 1)
    
    def divideConquer(self, nums, left, right):
        if left == right:
            return nums[left]
        
        mid = (left + right) // 2
        
        # Maximum in left half
        left_max = self.divideConquer(nums, left, mid)
        # Maximum in right half
        right_max = self.divideConquer(nums, mid + 1, right)
        # Maximum crossing middle
        cross_max = self.crossSum(nums, left, right, mid)
        
        return max(left_max, right_max, cross_max)
    
    def crossSum(self, nums, left, right, mid):
        if left == right:
            return nums[left]
        
        # Max sum extending left from mid
        left_sum = float('-inf')
        current_sum = 0
        for i in range(mid, left - 1, -1):
            current_sum += nums[i]
            left_sum = max(left_sum, current_sum)
        
        # Max sum extending right from mid+1
        right_sum = float('-inf')
        current_sum = 0
        for i in range(mid + 1, right + 1):
            current_sum += nums[i]
            right_sum = max(right_sum, current_sum)
        
        return left_sum + right_sum
            """,
                    "java": """
class Solution {
    public int maxSubArray(int[] nums) {
        return divideConquer(nums, 0, nums.length - 1);
    }
    
    private int divideConquer(int[] nums, int left, int right) {
        if (left == right) {
            return nums[left];
        }
        
        int mid = (left + right) / 2;
        
        int leftMax = divideConquer(nums, left, mid);
        int rightMax = divideConquer(nums, mid + 1, right);
        int crossMax = crossSum(nums, left, right, mid);
        
        return Math.max(Math.max(leftMax, rightMax), crossMax);
    }
    
    private int crossSum(int[] nums, int left, int right, int mid) {
        if (left == right) {
            return nums[left];
        }
        
        int leftSum = Integer.MIN_VALUE;
        int currentSum = 0;
        for (int i = mid; i >= left; i--) {
            currentSum += nums[i];
            leftSum = Math.max(leftSum, currentSum);
        }
        
        int rightSum = Integer.MIN_VALUE;
        currentSum = 0;
        for (int i = mid + 1; i <= right; i++) {
            currentSum += nums[i];
            rightSum = Math.max(rightSum, currentSum);
        }
        
        return leftSum + rightSum;
    }
}
            """,
                    "cpp": """
class Solution {
public:
    int maxSubArray(vector<int>& nums) {
        return divideConquer(nums, 0, nums.size() - 1);
    }
    
private:
    int divideConquer(vector<int>& nums, int left, int right) {
        if (left == right) {
            return nums[left];
        }
        
        int mid = (left + right) / 2;
        
        int leftMax = divideConquer(nums, left, mid);
        int rightMax = divideConquer(nums, mid + 1, right);
        int crossMax = crossSum(nums, left, right, mid);
        
        return max({leftMax, rightMax, crossMax});
    }
    
    int crossSum(vector<int>& nums, int left, int right, int mid) {
        if (left == right) {
            return nums[left];
        }
        
        int leftSum = INT_MIN;
        int currentSum = 0;
        for (int i = mid; i >= left; i--) {
            currentSum += nums[i];
            leftSum = max(leftSum, currentSum);
        }
        
        int rightSum = INT_MIN;
        currentSum = 0;
        for (int i = mid + 1; i <= right; i++) {
            currentSum += nums[i];
            rightSum = max(rightSum, currentSum);
        }
        
        return leftSum + rightSum;
    }
};
            """
                }
            }
        ],
        "videoUrl": "https://www.youtube.com/watch?v=5WZl3MMT0Eg"
    },
    "testcases": [
        {
            "input": "[-2,1,-3,4,-1,2,1,-5,4]",
            "expectedOutput": "6",
            "isHidden": False,
            "order": 1,
            "explanation": "The subarray [4,-1,2,1] has the largest sum of 6."
        },
        {
            "input": "[1]",
            "expectedOutput": "1",
            "isHidden": False,
            "order": 2,
            "explanation": "Single element array, so the maximum sum is that element."
        },
        {
            "input": "[5,4,-1,7,8]",
            "expectedOutput": "23",
            "isHidden": False,
            "order": 3,
            "explanation": "The entire array is the maximum subarray with sum 23."
        },
        {
            "input": "[-1]",
            "expectedOutput": "-1",
            "isHidden": True,
            "order": 4,
            "explanation": "Single negative element, return it as the maximum."
        },
        {
            "input": "[-2,-1,-3,-4]",
            "expectedOutput": "-1",
            "isHidden": True,
            "order": 5,
            "explanation": "All negative numbers, pick the largest (least negative) one."
        },
        {
            "input": "[1,2,-1,-2,2,1,-2,1,4,-5,4]",
            "expectedOutput": "6",
            "isHidden": True,
            "order": 6,
            "explanation": "Complex array with mixed positive and negative values."
        }
    ],
    "tags": [
        {
            "name": "Array",
            "category": "topic"
        },
        {
            "name": "Dynamic Programming",
            "category": "topic"
        },
        {
            "name": "Divide and Conquer",
            "category": "topic"
        },
        {
            "name": "Amazon",
            "category": "company"
        },
        {
            "name": "Microsoft",
            "category": "company"
        },
        {
            "name": "LinkedIn",
            "category": "company"
        },
        {
            "name": "Bloomberg",
            "category": "company"
        }
    ],
    "snippets": [
        {
            "code": "class Solution:\n    def maxSubArray(self, nums):\n        pass",
            "lang": "python",
            "compiler_language_id": 71
        },
        {
            "code": "class Solution {\n    public int maxSubArray(int[] nums) {\n        return 0;\n    }\n}",
            "lang": "java",
            "compiler_language_id": 62
        },
        {
            "code": "class Solution {\npublic:\n    int maxSubArray(vector<int>& nums) {\n        return 0;\n    }\n};",
            "lang": "cpp",
            "compiler_language_id": 54
        }
    ]
}





#########################################################






problem_7 = {
    "title": "Climbing Stairs",
    "description": "You are climbing a staircase. It takes n steps to reach the top.\n\nEach time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?\n\nNote: Given n will be a positive integer.",
    "xpReward": 10,
    "difficulty": "Easy",
    "hints": [
        {
            "content": "To reach step n, you must have come from either step n-1 or step n-2.",
            "order": 1
        },
        {
            "content": "This is actually a Fibonacci sequence problem in disguise!",
            "order": 2
        },
        {
            "content": "Think about how many ways you can reach the first few steps: 1 step (1 way), 2 steps (2 ways), 3 steps (3 ways)...",
            "order": 3
        },
        {
            "content": "You can solve this using dynamic programming, starting from the base cases.",
            "order": 4
        }
    ],
    "constraints": [
        {
            "description": "1 <= n <= 45",
            "order": 1
        }
    ],
    "editorial": {
        "title": "Climbing Stairs",
        "overview": """
The **Climbing Stairs** problem is a fundamental dynamic programming problem that introduces the concept of breaking down problems into overlapping subproblems.

### Problem Essence:
Count the number of distinct ways to reach the top of a staircase with n steps, where you can climb 1 or 2 steps at a time.

### Key Insight:
To reach step n, you can arrive from:
- Step n-1 (by taking 1 step)
- Step n-2 (by taking 2 steps)

Therefore: ways(n) = ways(n-1) + ways(n-2)

This is the Fibonacci sequence!

### Examples:
n = 2: [1,1] and [2] → 2 ways
n = 3: [1,1,1], [1,2], [2,1] → 3 ways
n = 4: [1,1,1,1], [1,1,2], [1,2,1], [2,1,1], [2,2] → 5 ways

### Approaches:
- Recursive (with and without memoization)
- Dynamic Programming (bottom-up)
- Space-optimized DP (Fibonacci approach)
        """,
        "approaches": [
            {
                "id": "recursive_memoization",
                "title": "Approach 1: Recursion with Memoization",
                "explanation": """
The recursive approach directly models the problem definition, enhanced with memoization to avoid redundant calculations.

### Recursive Relation
- Base cases: ways(1) = 1, ways(2) = 2
- Recursive case: ways(n) = ways(n-1) + ways(n-2)

### Algorithm
1. Create a memoization dictionary/array to store computed results
2. Define a recursive function:
   - If n <= 2, return n
   - If result is already computed, return it from memo
   - Otherwise: result = recursive_call(n-1) + recursive_call(n-2)
   - Store result in memo and return it
3. Call the function with n

### Why Memoization?
Without memoization, we'd recalculate the same values many times:
```
climb(5)
├── climb(4)
│   ├── climb(3)
│   │   ├── climb(2)
│   │   └── climb(1)
│   └── climb(2)  ← recalculated
└── climb(3)      ← recalculated
    ├── climb(2)  ← recalculated
    └── climb(1)  ← recalculated
```

With memoization, each value is calculated only once.

### Example: n = 5
- climb(5) = climb(4) + climb(3)
- climb(4) = climb(3) + climb(2) = 3 + 2 = 5
- climb(3) = climb(2) + climb(1) = 2 + 1 = 3
- climb(2) = 2 (base case)
- climb(1) = 1 (base case)
- Result: 5 + 3 = 8

### Complexity
- Time: O(n) - each subproblem computed once
- Space: O(n) - recursion stack + memoization array
            """,
                "code": {
                    "python": """
class Solution:
    def climbStairs(self, n):
        memo = {}
        return self.climb(n, memo)
    
    def climb(self, n, memo):
        # Base cases
        if n <= 2:
            return n
        
        # Check if already computed
        if n in memo:
            return memo[n]
        
        # Compute and store in memo
        memo[n] = self.climb(n - 1, memo) + self.climb(n - 2, memo)
        return memo[n]
            """,
                    "java": """
class Solution {
    private Map<Integer, Integer> memo = new HashMap<>();
    
    public int climbStairs(int n) {
        return climb(n);
    }
    
    private int climb(int n) {
        // Base cases
        if (n <= 2) {
            return n;
        }
        
        // Check if already computed
        if (memo.containsKey(n)) {
            return memo.get(n);
        }
        
        // Compute and store in memo
        int result = climb(n - 1) + climb(n - 2);
        memo.put(n, result);
        return result;
    }
}
            """,
                    "cpp": """
class Solution {
public:
    int climbStairs(int n) {
        unordered_map<int, int> memo;
        return climb(n, memo);
    }
    
private:
    int climb(int n, unordered_map<int, int>& memo) {
        // Base cases
        if (n <= 2) {
            return n;
        }
        
        // Check if already computed
        if (memo.count(n)) {
            return memo[n];
        }
        
        // Compute and store in memo
        memo[n] = climb(n - 1, memo) + climb(n - 2, memo);
        return memo[n];
    }
};
            """
                }
            },
            {
                "id": "dp_bottom_up",
                "title": "Approach 2: Dynamic Programming (Bottom-Up)",
                "explanation": """
The bottom-up DP approach builds the solution iteratively from the base cases up to n.

### Key Idea
Instead of recursing from n down to base cases, we start from base cases and build up to n.

### Algorithm
1. Create a DP array of size n+1
2. Initialize base cases: dp[1] = 1, dp[2] = 2
3. For i from 3 to n:
   - dp[i] = dp[i-1] + dp[i-2]
4. Return dp[n]

### Why it works
We're computing each step's answer based on previously computed steps. By the time we reach step n, all necessary subproblems are already solved.

### Example: n = 5
```
dp[1] = 1
dp[2] = 2
dp[3] = dp[2] + dp[1] = 2 + 1 = 3
dp[4] = dp[3] + dp[2] = 3 + 2 = 5
dp[5] = dp[4] + dp[3] = 5 + 3 = 8
```

### Visualization:
```
Step:  1  2  3  4  5
Ways:  1  2  3  5  8
       ↑  ↑  ↑  ↑  ↑
       └──┴──┘  │  │
          └─────┴──┘
```

### Complexity
- Time: O(n) - single loop from 3 to n
- Space: O(n) - DP array of size n+1
            """,
                "code": {
                    "python": """
class Solution:
    def climbStairs(self, n):
        if n <= 2:
            return n
        
        # Create DP array
        dp = [0] * (n + 1)
        dp[1] = 1
        dp[2] = 2
        
        # Fill the DP array
        for i in range(3, n + 1):
            dp[i] = dp[i - 1] + dp[i - 2]
        
        return dp[n]
            """,
                    "java": """
class Solution {
    public int climbStairs(int n) {
        if (n <= 2) {
            return n;
        }
        
        // Create DP array
        int[] dp = new int[n + 1];
        dp[1] = 1;
        dp[2] = 2;
        
        // Fill the DP array
        for (int i = 3; i <= n; i++) {
            dp[i] = dp[i - 1] + dp[i - 2];
        }
        
        return dp[n];
    }
}
            """,
                    "cpp": """
class Solution {
public:
    int climbStairs(int n) {
        if (n <= 2) {
            return n;
        }
        
        // Create DP array
        vector<int> dp(n + 1);
        dp[1] = 1;
        dp[2] = 2;
        
        // Fill the DP array
        for (int i = 3; i <= n; i++) {
            dp[i] = dp[i - 1] + dp[i - 2];
        }
        
        return dp[n];
    }
};
            """
                }
            },
            {
                "id": "space_optimized",
                "title": "Approach 3: Space-Optimized DP",
                "explanation": """
Since we only need the previous two values to compute the current value, we can optimize space to O(1).

### Key Observation
At any point, we only need:
- The number of ways to reach the previous step (n-1)
- The number of ways to reach the step before that (n-2)

We don't need to store the entire array!

### Algorithm
1. Handle base cases: if n <= 2, return n
2. Initialize two variables: prev2 = 1 (for step 1), prev1 = 2 (for step 2)
3. For i from 3 to n:
   - current = prev1 + prev2
   - Update: prev2 = prev1, prev1 = current
4. Return prev1

### Example: n = 5
```
Initial: prev2=1, prev1=2
i=3: current=3, prev2=2, prev1=3
i=4: current=5, prev2=3, prev1=5
i=5: current=8, prev2=5, prev1=8
Result: 8
```

### Visual Representation:
```
Step:        1    2    3    4    5
            prev2 prev1
                 prev2 prev1
                      prev2 prev1
                           prev2 prev1
```

### Complexity
- Time: O(n) - single loop from 3 to n
- Space: O(1) - only using two variables
            """,
                "code": {
                    "python": """
class Solution:
    def climbStairs(self, n):
        if n <= 2:
            return n
        
        prev2 = 1  # Ways to reach step 1
        prev1 = 2  # Ways to reach step 2
        
        for i in range(3, n + 1):
            current = prev1 + prev2
            prev2 = prev1
            prev1 = current
        
        return prev1
            """,
                    "java": """
class Solution {
    public int climbStairs(int n) {
        if (n <= 2) {
            return n;
        }
        
        int prev2 = 1;  // Ways to reach step 1
        int prev1 = 2;  // Ways to reach step 2
        
        for (int i = 3; i <= n; i++) {
            int current = prev1 + prev2;
            prev2 = prev1;
            prev1 = current;
        }
        
        return prev1;
    }
}
            """,
                    "cpp": """
class Solution {
public:
    int climbStairs(int n) {
        if (n <= 2) {
            return n;
        }
        
        int prev2 = 1;  // Ways to reach step 1
        int prev1 = 2;  // Ways to reach step 2
        
        for (int i = 3; i <= n; i++) {
            int current = prev1 + prev2;
            prev2 = prev1;
            prev1 = current;
        }
        
        return prev1;
    }
};
            """
                }
            }
        ],
        "videoUrl": "https://www.youtube.com/watch?v=Y0lT9Fck7qI"
    },
    "testcases": [
        {
            "input": "2",
            "expectedOutput": "2",
            "isHidden": False,
            "order": 1,
            "explanation": "Two ways: [1,1] or [2]"
        },
        {
            "input": "3",
            "expectedOutput": "3",
            "isHidden": False,
            "order": 2,
            "explanation": "Three ways: [1,1,1], [1,2], or [2,1]"
        },
        {
            "input": "1",
            "expectedOutput": "1",
            "isHidden": False,
            "order": 3,
            "explanation": "Only one way: [1]"
        },
        {
            "input": "5",
            "expectedOutput": "8",
            "isHidden": True,
            "order": 4,
            "explanation": "Eight different ways to climb 5 steps."
        },
        {
            "input": "10",
            "expectedOutput": "89",
            "isHidden": True,
            "order": 5,
            "explanation": "89 different ways to climb 10 steps (10th Fibonacci number)."
        },
        {
            "input": "20",
            "expectedOutput": "10946",
            "isHidden": True,
            "order": 6,
            "explanation": "Testing larger input for efficiency."
        }
    ],
    "tags": [
        {
            "name": "Dynamic Programming",
            "category": "topic"
        },
        {
            "name": "Math",
            "category": "topic"
        },
        {
            "name": "Memoization",
            "category": "topic"
        },
        {
            "name": "Amazon",
            "category": "company"
        },
        {
            "name": "Adobe",
            "category": "company"
        },
        {
            "name": "Google",
            "category": "company"
        }
    ],
    "snippets": [
        {
            "code": "class Solution:\n    def climbStairs(self, n):\n        pass",
            "lang": "python",
            "compiler_language_id": 71
        },
        {
            "code": "class Solution {\n    public int climbStairs(int n) {\n        return 0;\n    }\n}",
            "lang": "java",
            "compiler_language_id": 63
        },
        {
            "code": "class Solution {\npublic:\n    int climbStairs(int n) {\n        return 0;\n    }\n};",
            "lang": "cpp",
            "compiler_language_id": 42
        }
    ]
}






#############################################







def get_data():
    return [problem_1, problem_2, problem_3, problem_4, problem_5, problem_6, problem_7]