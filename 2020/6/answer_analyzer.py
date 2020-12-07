from operator import and_
from functools import reduce

print(sum([len(set(x)) for x in [_.replace('\n', '') for _ in open('input').read().split('\n\n')]])) 

nums = []
for ag in [a for a in [g.split('\n') for g in [_ for _ in open('input').read().split('\n\n')]]]:
    nums.append(len(reduce(and_, [set(_a) for _a in ag])))

print(sum(nums))
