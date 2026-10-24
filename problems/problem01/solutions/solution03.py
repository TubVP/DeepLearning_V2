def min_cost_path(grid):
    ...
def min_cost_path(grid):
    n, m = len(grid), len(grid[0])
    dp = [[0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            if i == 0 and j == 0:
                dp[i][j] = grid[i][j]
            elif i == 0:
                dp[i][j] = dp[i][j - 1] + grid[i][j]
            elif j == 0:
                dp[i][j] = dp[i - 1][j] + grid[i][j]
            else:
                dp[i][j] = min(dp[i - 1][j], dp[i][j - 1]) + grid[i][j]
    return dp[-1][-1]