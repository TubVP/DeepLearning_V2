def knapsack_max_value(items, C):
    ...
def knapsack_max_value(items, C):
    max_value = 0
    for i in range(len(items)):
        for j in range(i+1, len(items)):
            if items[i][0] + items[j][0] <= C:
                max_value = max(max_value, items[i][1] + items[j][1])
    return max_value