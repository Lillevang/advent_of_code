from typing import List

d = [int(f.strip()) for f in open('input').readlines()]
PREAMBLE_START = 0
PREAMBLE_END = 25
PREAMBLE = d[PREAMBLE_START:PREAMBLE_END]

def two_sum(preamble: List[int], num: int) -> bool:
    return True


for i in range(25, len(d)):    
    if not two_sum(PREAMBLE, d[i]):
        print(d[i])
        break
    else:
        PREAMBLE_START+=1
        PREAMBLE_END+=1
        PREAMBLE = d[PREAMBLE_START:PREAMBLE_END]