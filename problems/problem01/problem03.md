# Problem 3

You are given a weighted 2D grid `grid` of size `n x m` where each cell contains a non-negative integer cost. 
Your task is to find the minimum cost path from the top-left corner `(0,0)` to the bottom-right corner `(n-1,m-1)`. 
You can only move **right** or **down** at each step.

Example:
Input: `grid = [ [1, 3, 1], [1, 5, 1], [4, 2, 1] ]`
Output: `7`

Explanation:  
The path with minimum cost is `1 → 3 → 1 → 1 → 1`, total cost = 7.

Constraints:
- `1 <= n, m <= 100`
- `0 <= grid[i][j] <= 1000`

Boilerplate code:
```python
def min_cost_path(grid):
    ...