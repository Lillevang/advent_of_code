rocks, i = ((0,1,2,3),(1,0+1j,2+1j,1+2j),(0,1,2,2+1j,2+2j),(0,0+1j,0+2j,0+3j),(0,1,0+1j,1+1j)), 0
jets,  j = [ord(x)-61 for x in open('./input').read()], 0
tower, cache, h = set(), dict(), 0

empty = lambda p: p.real in range(7) and p.imag>0 and p not in tower
check = lambda p, d, rock: all(empty(p+d+r) for r in rock)

for n in range(int(1e12)):
    p = complex(2, h+4)                     # set start pos
    if n==2022: print(h)

    key = i, j                              # check for cycle
    if key in cache:
        N, H = cache[key]
        d, m = divmod(1e12-n, N-n)
        if not m: print(h + (H-h)*d); break
    else: cache[key] = n, h

    rock = rocks[i]                         # get next rock
    i = (i+1) % len(rocks)                  # and inc index

    while True:                                          
        jet = jets[j]                       # get next jet
        j = (j+1) % len(jets)               # and inc index

        if check(p, jet, rock): p += jet    # maybe move side
        if check(p, -1j, rock): p += -1j    # maybe move down
        else: break                         # can't move down

    tower |= {p+r for r in rock}            # add rock to tower
    h = max(h, p.imag+[1,0,2,2,3][i])       # compute new height
