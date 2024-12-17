from collections import deque

with open('./example', 'r') as file:
    lines = file.readlines()

graph = [line for line in lines]
row_length = len(graph)
col_length = len(graph[0])

edges = [[0 for _ in range(col_length)] for _ in range(row_length)]
for r in range(row_length):
    for c in range(col_length):
        if graph[r][c]=='S':
            edges[r][c] = 1
        elif graph[r][c] == 'edges':
            edges[r][c] = 26
        else:
            edges[r][c] = ord(graph[r][c])-ord('a')+1

def bfs(part):
    Q = deque()
    for r in range(row_length):
        for c in range(col_length):
            if (part==1 and graph[r][c]=='S') or (part==2 and edges[r][c] == 1):
                Q.append(((r,c), 0))

    S = set()
    while Q:
        (r,c),d = Q.popleft()
        if (r,c) in S:
            continue
        S.add((r,c))
        if graph[r][c]=='E':
            return d
        for dr,dc in [(-1,0),(0,1),(1,0),(0,-1)]:
            rr = r+dr
            cc = c+dc
            if 0<=rr<row_length and 0<=cc<col_length and edges[rr][cc]<=1+edges[r][c]:
                Q.append(((rr,cc),d+1))
print(bfs(1))
print(bfs(2))
