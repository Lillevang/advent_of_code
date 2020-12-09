import re

def check_fields(passport_info):
    f = True
    necessary_fields = ('byr', 'iyr', 'eyr', 'hgt', 'ecl', \
                        'hcl', 'pid')
    for field in necessary_fields:
        if field not in passport_info:
            f = False
            break
    return f

fhand = open('input',encoding='utf-8')
info = fhand.read()
persons = info.rstrip().split('\n\n')
count = 0

for person in persons:
    info = person.replace('\n', ' ')
    flag = check_fields(info)
    if flag:
        byr = re.search(r'byr:(19[2-9][0-9]|200[0-2])', info)
        iyr = re.search(r'iyr:(201[0-9]|2020)', info)
        eyr = re.search(r'eyr:(20[2][0-9]|2030)', info)
        hgt = re.search(r'hgt:(1[5-8][0-9]cm|19[0-3]cm|59in|6[0-9]in|7[0-3]in)', info)
        hcl = re.search(r'hcl:#[0-9a-f]{6}', info)
        ecl = re.search(r'ecl:(amb|blu|brn|gry|grn|hzl|oth)', info)
        pid = re.search(r'pid:[0-9]{9}', info)
        if byr and iyr and eyr and hgt and hcl and ecl and pid:
            count += 1

print(count)