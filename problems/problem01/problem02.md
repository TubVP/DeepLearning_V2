# Problem 2

Given a square matrix `grid` of size `n x n`, find the maximum sum of numbers along a path from the top-left corner `(0,0)` to the bottom-right corner `(n-1,n-1)`.  
You can only move **right** or **down** at each step.

Example:
Input: `grid = [ [5, 3, 2], [1, 4, 1], [1, 5, 1] ]`
Output: `18`

Explanation: 
One of the paths that produces the maximum sum is: 5 → 3 → 4 → 5 → 1. The sum = 18.

Constraints:
- `1 <= n <= 100`
- `0 <= grid[i][j] <= 1000`

Boilerplate code:
```python
def max_path_sum(grid):
    ...
