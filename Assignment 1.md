Assignment 1:

Your task is to fine tune an LLM to compete in programming contests. 
The LLM receives a problem description in natural language and it must output the Python code solution to the problem. 
The Python code will be run on some test cases and its score will be measured by the percentage of correct test cases. 
For example, there are 20 test cases and the programm correctly solves 17 of them, then its score is 0.85. 

Competition rules:
- The dataset contains 50 programming problems.
- The problems have different difficulty levels: easy, medium, hard.
- The solutions must be written in Python and must not use any non-standard libraries.
- The solutions must use less than 100MB of memory.
- The solutions must run in less than 10 seconds.
- The LLM must produce the code in less than 120 seconds on a single RTX 1080 GPU.
- The base LLM must be no bigger than 5B parameters.
- The LLM cannot use the internet.
- Your code must be written in a single file named "uet_coder.py".
- You must submit the "uet_coder.py" file and the model weights.


Evaluation:
- The LLM will be run using the following command:
```bash
python uet_coder.py --problem <problem_file> --output <source_code_file>
```
- The problem_file is the file containing the problem description in Markdown format. See examples below.
- The source_code_file is the file containing the solution code. 
- The source_code_file will be run on the test cases and the score will be measured by the percentage of correct test cases.

Examples:
1. Run the following command to get the problem description and the solution code:
```bash
python uet_coder.py --problem Problem1.md --output Solution1.py
```
2. Run the following command to get the score:
```bash
python uet_marker.py --source_code_file Solution1.py --test_cases TestCases1.txt
```

Problem1.md:
```markdown
# Problem 1

Given a list of integers `nums` of size `n`, return the sum of the two largest integers.

Example:
Input: `nums = [1, 2, 3, 4, 5]`
Output: `9`

Explanation:
The two largest integers are 4 and 5, so the sum is 9.

Constraints:
- `n < 10000`


Boilerplate code:
```python
def sum_of_two_largest(nums):
    ...
```
```

Solution1.py: 
```python
def sum_of_two_largest(nums):
    return sorted(nums)[-2:]
```
