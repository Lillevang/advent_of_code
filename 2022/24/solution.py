W = set()
B = set()

with open('./input', 'r') as file:
    lines = file.read().strip().split('\n')

for y, line in enumerate(lines):
    for x, c in enumerate(line):
        if c == '#': W.add((x-1, y-1))
        elif c == '>': B.add((x-1,y-1, +1,0))
        elif c == '<': B.add((x-1, y-1, -1,0))
        elif c == '^': B.add((x-1, y-1, 0,-1))
        elif c == 'v': B.add((x-1, y-1, 0,+1))
        else : raise ValueError("UNKNOWN SYMBOL!")

X = max(x for x, _ in W)
Y = max(y for _, y in W)

print(f'Maze size: {X}x{Y}, {len(W)} walls, {len(B)} blizzards')

W |= { (x, -2) for x in range(-1, 3) }
W |= { (x, Y + 1) for x in range(X-3, X+2) }
start = (0, -1)
exit = (X-1, Y)

t = 0
q = {start}
goals = [exit, start, exit]
while goals:
    t += 1
    b = { ((px+t*dx)%X, (py))}