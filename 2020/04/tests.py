import passport_validator_part_1 as pv1
import passport_validator_part_2 as pv2

def test_validate_passport_part_1():
    l = [
        ("iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884 hcl:#cfa07d byr:1929", False),
        ("ecl:gry pid:860033327 eyr:2020 hcl:#fffffd byr:1937 iyr:2017 cid:147 hgt:183cm", True),
        ("hcl:#ae17e1 iyr:2013 eyr:2024 ecl:brn pid:760753108 byr:1931 hgt:179cm", True),
        ("hcl:#cfa07d eyr:2025 pid:166559648 iyr:2011 ecl:brn hgt:59in", False)
    ]
    for t in l:
        try:
            assert(pv1.validate_passport(t[0]) == t[1])
        except AssertionError:
            print(t)


def test_byr_validation():
    assert(pv2.validate_byr('001') == False)
    assert(pv2.validate_byr('123456') == False)
    assert(pv2.validate_byr('1919') == False)
    assert(pv2.validate_byr('1920') == True)
    assert(pv2.validate_byr('2002') == True)
    assert(pv2.validate_byr('2003') == False)


def test_iyr_validation():
    assert(pv2.validate_iyr('001') == False)
    assert(pv2.validate_iyr('123456') == False)
    assert(pv2.validate_iyr('1919') == False)
    assert(pv2.validate_iyr('1920') == False)
    assert(pv2.validate_iyr('2002') == False)
    assert(pv2.validate_iyr('2003') == False)
    assert(pv2.validate_iyr('2010') == True)
    assert(pv2.validate_iyr('2020') == True)
    assert(pv2.validate_iyr('2021') == False)


def test_eyr_validation():
    assert(pv2.validate_eyr('001') == False)
    assert(pv2.validate_eyr('123456') == False)
    assert(pv2.validate_eyr('1919') == False)
    assert(pv2.validate_eyr('1920') == False)
    assert(pv2.validate_eyr('2002') == False)
    assert(pv2.validate_eyr('2003') == False)
    assert(pv2.validate_eyr('2010') == False)
    assert(pv2.validate_eyr('2020') == True)
    assert(pv2.validate_eyr('2021') == True)
    assert(pv2.validate_eyr('2030') == True)  
    assert(pv2.validate_eyr('2031') == False)  


def test_hgt_validation():
    assert(pv2.validate_hgt('60in') == True)
    assert(pv2.validate_hgt('190cm') == True)
    assert(pv2.validate_hgt('190in') == False)
    assert(pv2.validate_hgt('190') == False)


def test_hcl_validation():
    assert(pv2.validate_hcl('#123abc') == True)
    assert(pv2.validate_hcl('#a231bc') == True)
    assert(pv2.validate_hcl('#123abz') == False)
    assert(pv2.validate_hcl('123abc') == False)


def test_ecl_validation():
    assert(pv2.validate_ecl('brn') == True)
    assert(pv2.validate_ecl('wat') == False)


def test_pid_validation():
    assert(pv2.validate_pid('087499704') == True)
    assert(pv2.validate_pid('0087499704') == False) 
    assert(pv2.validate_pid('02157') == False) 
    assert(pv2.validate_pid('012533040') == True)
    

def test_validate_passport_part_2():
    test_byr_validation()
    test_iyr_validation()
    test_eyr_validation()
    test_hgt_validation()
    test_hcl_validation()
    test_ecl_validation()
    test_pid_validation()
    assert(pv2.validate_passport("hcl:#ae17e1 iyr:2013 eyr:2024 ecl:brn pid:760753108 byr:1931 hgt:179cm") == True)
    assert(pv2.validate_passport("eyr:1972 cid:100 hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926") == False)
    assert(pv2.validate_passport("iyr:2019 hcl:#602927 eyr:1967 hgt:170cm ecl:grn pid:012533040 byr:1946") == False)
    assert(pv2.validate_passport("hcl:dab227 iyr:2012 ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277") == False)
    assert(pv2.validate_passport("hgt:59cm ecl:zzz eyr:2038 hcl:74454a iyr:2023 pid:3556412378 byr:2007") == False)
    assert(pv2.validate_passport("pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980 hcl:#623a2f") == True)
    assert(pv2.validate_passport("eyr:2029 ecl:blu cid:129 byr:1989 iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm") == True)
    assert(pv2.validate_passport("hcl:#888785 hgt:164cm byr:2001 iyr:2015 cid:88 pid:545766238 ecl:hzl eyr:2022") == True)
    assert(pv2.validate_passport("iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719") == True)

    
if __name__ == "__main__":
    test_validate_passport_part_1()
    test_validate_passport_part_2()