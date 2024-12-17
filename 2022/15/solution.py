# TODO crystal refactor. Consider holding the Sensor/beacon coords as structs?

with open('./input', 'r') as file:
    lines = [_ for _ in file.read().strip().split("\n")]

S = set() # Sensors
B = set() # Beacons

sum_d = 0

for line in lines:
    words = line.split()
    sensor_x, sensor_y = int(words[2][2:-1]), int(words[3][2:-1])
    beacon_x, beacon_y = int(words[8][2:-1]), int(words[9][2:])
    d = abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y)
    sum_d += d
    S.add((sensor_x, sensor_y, d))
    B.add((beacon_x, beacon_y))

def valid(x,y, S):
    for (sx,sy,d) in S:
        dxy = abs(x-sx) + abs(y-sy)
        if dxy <= d:
            return False
    return True


p1 = 0
for x in range(-int(1e7), int(1e7)):
    y = int(2e6)
    if not valid(x, y, S) and (x,y) not in B:
        p1 += 1
print(p1)



n_checked = 0
found_p2 = False
for (sx, sy, d) in S:
    if found_p2:
        break
    for dx in range(d+2):
        if found_p2:
            break
        dy = (d+1)-dx
        for signx,signy in [(-1,-1), (-1,1), (1,-1), (1,1)]:
            if found_p2:
                break
            n_checked += 1
            x = sx + (dx*signx)
            y = sy + (dy*signy)
            if not (0<=x<=4000000 and 0<=y<=4000000):
                continue
            assert abs(x-sx) + abs(y-sy) == d+1
            if valid(x, y, S) and (not found_p2):
                print(x*4000000 + y)
                found_p2 = True
