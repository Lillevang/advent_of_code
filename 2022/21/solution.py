import re, z3

for name in 'root', 'humn':
    s = z3.Optimize()
    for line in open('./input'):
        for m in re.findall(r'[a-z]{4}', line):
            exec(f'{m} = z3.Int("{m}")')
        if name=='humn': # part 2
            if line[:4]=='humn':
                continue
            if line[:4]=='root':
                line = line[6:].replace('+', '==')
        exec(f's.add({line.replace(":", "==")})')

    s.check()
    print(s.model()[z3.Int(name)])