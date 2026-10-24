def max_path_sum(grid):
    ...
def max_path_sum(grid):
    n = len(grid)
    max_sum = float('-inf')
    for i in range(n):
        for j in range(n):
            max_sum = max(max_sum, dfs(grid, i, j, n))
    return max_sum

def dfs(grid, i, j, n):
    if i < 0 or i >= n or j < 0 or j >= n:
        return 0
    if i == n - 1 and j == n - 1:
        return grid[i][j]
    return grid[i][j] + max(dfs(grid, i + 1, j, n), dfs(grid, i, j + 1, n))