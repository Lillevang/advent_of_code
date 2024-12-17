f = lambda s: f(s[:-1])*5 + '=-012'.find(s[-1])-2 if s else 0
g = lambda d: g((d+2)//5) + '=-012'[(d+2)%5] if d else ''

print(g(sum(map(f, map(str.strip, open('./input'))))))