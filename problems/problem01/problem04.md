# Problem 5

You are given a list of items, each with a weight and a value: `items = [(w1, v1), (w2, v2), ...]`.  
You also have a knapsack with capacity `C`.  

Find the maximum total value you can carry without exceeding the capacity `C`.  

Example:
Input: `items = [(2,3), (3,4), (4,5)], C = 5`
Output: `7`

Explanation:  
Take items `(2,3)` and `(3,4)`. Total weight `2+3=5` ≤ 5, total value `3+4=7`.

Constraints:
- `1 <= len(items) <= 1000`
- `1 <= wi, vi <= 1000`
- `1 <= C <= 10000`

Boilerplate code:
```python
def knapsack_max_value(items, C):
    ...