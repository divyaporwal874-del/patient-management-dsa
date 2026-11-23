"""DSA-II algorithm practice (Units 3 and 4). Separate from the patient system."""
from itertools import permutations


def matrix_chain(dims):
    """Minimum multiplications for matrices where matrix i is dims[i] x dims[i+1]."""
    n = len(dims) - 1
    m = [[0] * n for _ in range(n)]
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            m[i][j] = float("inf")
            for k in range(i, j):
                cost = m[i][k] + m[k + 1][j] + dims[i] * dims[k + 1] * dims[j + 1]
                m[i][j] = min(m[i][j], cost)
    return m[0][n - 1]


def knapsack(weights, profits, capacity):
    """0/1 knapsack: returns (best profit, chosen item indexes)."""
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            dp[i][w] = dp[i - 1][w]
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i][w], profits[i - 1] + dp[i - 1][w - weights[i - 1]])
    chosen, w = [], capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            chosen.append(i - 1)
            w -= weights[i - 1]
    return dp[n][capacity], sorted(chosen)


def n_queens(n):
    """Backtracking: returns (number of solutions, first solution)."""
    cols, d1, d2, row_cols, found = set(), set(), set(), [], []

    def place(r):
        if r == n:
            found.append(list(row_cols))
            return
        for c in range(n):
            if c in cols or (r - c) in d1 or (r + c) in d2:
                continue
            cols.add(c); d1.add(r - c); d2.add(r + c); row_cols.append(c)
            place(r + 1)
            cols.remove(c); d1.remove(r - c); d2.remove(r + c); row_cols.pop()

    place(0)
    return len(found), (found[0] if found else None)


def hamiltonian_cycle(graph):
    """Backtracking on an adjacency matrix: returns a cycle (list) or None."""
    n = len(graph)
    path = [0]

    def extend():
        if len(path) == n:
            return graph[path[-1]][0] == 1
        for v in range(1, n):
            if graph[path[-1]][v] == 1 and v not in path:
                path.append(v)
                if extend():
                    return True
                path.pop()
        return False

    return path + [0] if extend() else None


def tsp_branch_and_bound(cost):
    """Branch and bound: returns the minimum tour cost starting from city 0."""
    n = len(cost)
    best = [float("inf")]

    def bound(cur, visited, so_far):
        rest = [v for v in range(n) if v not in visited]
        total = so_far
        for u in [cur] + rest:
            targets = [v for v in rest + [0] if v != u]
            total += min(cost[u][v] for v in targets)
        return total

    def explore(cur, visited, so_far):
        if len(visited) == n:
            best[0] = min(best[0], so_far + cost[cur][0])
            return
        if bound(cur, visited, so_far) >= best[0]:
            return  # prune
        for v in range(n):
            if v not in visited:
                explore(v, visited | {v}, so_far + cost[cur][v])

    explore(0, {0}, 0)
    return best[0]


def tsp_brute_force(cost):
    n = len(cost)
    return min(sum(cost[a][b] for a, b in zip((0,) + p, p + (0,))) for p in permutations(range(1, n)))