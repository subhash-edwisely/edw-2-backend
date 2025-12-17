from dotenv import load_dotenv
load_dotenv()

import os
import json
from openai import OpenAI

API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=API_KEY)

SYSTEM_PROMPT = """
You are an expert competitive programmer specializing in algorithmic complexity analysis.

Analyze the given code and determine its time and space complexity in Big-O notation.

IMPORTANT RULES:
1. Identify the input size variable(s) from the code:
   - For arrays/lists: use 'n' for length
   - For strings: use 'n' for length
   - For matrices: use 'm × n' or 'm * n' for dimensions
   - For trees: use 'n' for number of nodes
   - For graphs: use 'n' for vertices, 'm' for edges
   - For multiple independent inputs: use distinct variables (n, m, k, etc.)

2. Express complexity in terms of these variables:
   - Use standard notation: O(n), O(n log n), O(n^2), O(m * n), O(n + m), etc.
   - For constants or small fixed operations: use O(1)
   - For recursive calls: account for call stack depth

3. Determine WORST-CASE complexity:
   - Consider all loops, recursive calls, and built-in operations
   - Account for hidden complexity in library functions
   - Common operations: sort is O(n log n), set/dict lookup is O(1) average

4. Space complexity includes:
   - Auxiliary space (extra data structures created)
   - Recursive call stack space
   - Do NOT count input space unless explicitly modified

Return ONLY valid JSON with no additional text:
{
  "time_complexity": "O(...)",
  "space_complexity": "O(...)"
}
"""

DOS = """
MUST DO:
1. Identify what 'n' represents from the function parameters
2. Express complexity using the identified variables
3. Return ONLY the JSON object, nothing else
4. Use proper Big-O notation syntax
"""

DONTS = """
NEVER:
- Add explanations outside the JSON
- Include markdown formatting or code blocks
- Ask clarifying questions
- Return multiple options or ranges
- Add comments in the JSON
"""

def identify_time_and_space_complexity(code):
    try:
        input_data = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": code + "\n\n" + DOS + "\n\n" + DONTS
            }
        ]

        response = client.responses.create(
            model="gpt-4.1-nano",
            input=input_data,
            text={"format": {"type": "json_object"}}
        )
        
        
        json_text = response.output_text

        
        result = json.loads(json_text)

        print("openai: ", result)

        return result

    except Exception as e:
        print("Error:", str(e))
        return None
