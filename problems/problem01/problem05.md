# Problem 6

You are given a directed graph with `n` nodes labeled from `0` to `n-1` and a list of edges, where each edge is `(u, v, w)` representing an edge from `u` to `v` with weight `w`.

Your task is to find the shortest distance from node `0` to all other nodes.  
If a node is unreachable, return `-1` for that node.

Example:
Input: `n = 5, edges = [(0,1,2),(0,2,5),(1,2,1),(1,3,3),(2,3,1),(3,4,2)]`
Output: `[0, 2, 3, 4, 6]`

Explanation:
- Distance to node 0 is 0
- Distance to node 1 is 2
- Distance to node 2 is 2+1=3 (via node 1)
- Distance to node 3 is 2+3=5 or 3+1=4 (take min 4)
- Distance to node 4 is 4+2=6

Constraints:
- `1 <= n <= 1000`
- `0 <= len(edges) <= 5000`
- `0 <= w <= 1000`

Boilerplate code:
```python
def shortest_paths(n, edges):
    ...