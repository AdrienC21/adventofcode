## --- Day 12: Hill Climbing Algorithm ---

"""
--- Day 12: Hill Climbing Algorithm ---
You try contacting the Elves using your handheld device, but the river you're following must be too low to get a decent signal.

You ask the device for a heightmap of the surrounding area (your puzzle input). The heightmap shows the local area from above broken into a grid; the elevation of each square of the grid is given by a single lowercase letter, where a is the lowest elevation, b is the next-lowest, and so on up to the highest elevation, z.

Also included on the heightmap are marks for your current position (S) and the location that should get the best signal (E). Your current position (S) has elevation a, and the location that should get the best signal (E) has elevation z.

You'd like to reach E, but to save energy, you should do it in as few steps as possible. During each step, you can move exactly one square up, down, left, or right. To avoid needing to get out your climbing gear, the elevation of the destination square can be at most one higher than the elevation of your current square; that is, if your current elevation is m, you could step to elevation n, but not to elevation o. (This also means that the elevation of the destination square can be much lower than the elevation of your current square.)

For example:

Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
Here, you start in the top-left corner; your goal is near the middle. You could start by moving down or right, but eventually you'll need to head toward the e at the bottom. From there, you can spiral around to the goal:

v..v<<<<
>v.vv<<^
.>vv>E^^
..v>>>^^
..>>>>>^
In the above diagram, the symbols indicate whether the path exits each square moving up (^), down (v), left (<), or right (>). The location that should get the best signal is still E, and . marks unvisited squares.

This path reaches the goal in 31 steps, the fewest possible.

What is the fewest steps required to move from your current position to the location that should get the best signal?
"""


with open("2022/day12.txt", "r") as f:
    input = f.read()


# First attempt failed
"""
from collections import defaultdict
import sys


def steps(input: str) -> int:
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    L = [list(l) for l in input.split("\n")]
    graph = defaultdict(list)
    m = len(L)
    n = len(L[0])
    start_pos = (0, 0)
    end_pos = (0, 0)
    for i in range(m):
        for j in range(n):
            if L[i][j] == "E":
                end_pos = (i, j)
            if L[i][j] == "S":
                start_pos = (i, j)
                for (k, l) in directions:
                    if (0 <= (i+k)) and ((i+k) < m) and (0 <= (j+l)) and ((j+l) < n):
                        graph[(i, j)].append((i+k, j+l))
                        graph[(i+k, j+l)].append((i, j))
            else:
                for (k, l) in directions:
                    if (0 <= (i+k)) and ((i+k) < m) and (0 <= (j+l)) and ((j+l) < n):
                        if (L[i][j] == "z") and (L[i+k][j+l] == "E"):
                            graph[(i, j)].append((i+k, j+l))
                            graph[(i+k, j+l)].append((i, j))
                        elif abs(ord(L[i][j]) - ord(L[i+k][j+l])) <= 1:
                            graph[(i, j)].append((i+k, j+l))

    dist = {(i, j): sys.maxsize for i in range(m) for j in range(n)}
    dist[start_pos] = 0
    to_visit = [(i, j) for i in range(m) for j in range(n)]
    prev = {(i, j): None for i in range(m) for j in range(n)}
    while to_visit:
        min_i = 0
        min_dist = dist[to_visit[0]]
        for i in range(1, len(to_visit)):
            if dist[to_visit[i]] < min_dist:
                min_i = i
                min_dist = dist[to_visit[i]]
        u = to_visit.pop(min_i)
        for v in graph[u]:
            if dist[v] > dist[u] + 1:
                dist[v] = dist[u] + 1
                prev[v] = u

    len_path = 0
    s = end_pos
    while s != start_pos:
        s = prev[s]
        len_path += 1
    return len_path
"""


from collections import deque


def steps(input : str) -> int:
    L = [list(l) for l in input.split("\n")]
    m = len(L)
    n = len(L[0])
    for i in range(m):
        for j in range(n):
            if L[i][j] == "S":
                start_pos = (i, j)
                L[i][j] = "a"
            if L[i][j] == "E":
                end_pos = (i, j)
                L[i][j] = "z"

    q = deque([(start_pos[0], start_pos[1], 0)])
    seen = set()

    while q:
        a, b, c = q.popleft()
        if (a, b) == end_pos:
            return c
        if (a, b) in seen:
            continue
        seen.add((a, b))
        for i in range(a-1, a+2):
            for j in range(b-1, b+2):
                if (0 <= i) and (i < m) and (0 <= j) and (j < n) and ((i == a) or (j == b)):
                    if (ord(L[i][j]) - ord(L[a][b])) <= 1:
                        q.append((i, j, c+1))


print(f"Result:\n{steps(input)}")

## --- Part Two ---

"""
--- Part Two ---
As you walk up the hill, you suspect that the Elves will want to turn this into a hiking trail. The beginning isn't very scenic, though; perhaps you can find a better starting point.

To maximize exercise while hiking, the trail should start as low as possible: elevation a. The goal is still the square marked E. However, the trail should still be direct, taking the fewest steps to reach its goal. So, you'll need to find the shortest path from any square at elevation a to the square marked E.

Again consider the example from above:

Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
Now, there are six choices for starting position (five marked a, plus the square marked S that counts as being at elevation a). If you start at the bottom-left square, you can reach the goal most quickly:

...v<<<<
...vv<<^
...v>E^^
.>v>>>^^
>^>>>>>^
This path reaches the goal in only 29 steps, the fewest possible.

What is the fewest steps required to move starting from any square with elevation a to the location that should get the best signal?
"""


def steps2(input: str) -> int:
    L = [list(l) for l in input.split("\n")]
    m = len(L)
    n = len(L[0])
    start_pos = []
    for i in range(m):
        for j in range(n):
            if (L[i][j] == "S") or (L[i][j] == "a"):
                start_pos.append((i, j))
                L[i][j] = "a"
            if L[i][j] == "E":
                end_pos = (i, j)
                L[i][j] = "z"

    q = deque()
    for s in start_pos:
        q.append((s[0], s[1], 0))
    seen = set()

    while q:
        a, b, c = q.popleft()
        if (a, b) == end_pos:
            return c
        if (a, b) in seen:
            continue
        seen.add((a, b))
        for i in range(a-1, a+2):
            for j in range(b-1, b+2):
                if (0 <= i) and (i < m) and (0 <= j) and (j < n) and ((i == a) or (j == b)):
                    if (ord(L[i][j]) - ord(L[a][b])) <= 1:
                        q.append((i, j, c+1))


print(f"Result:\n{steps2(input)}")
