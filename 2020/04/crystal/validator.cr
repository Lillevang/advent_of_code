module Passport_validator
    extend self
    
    @@task_1_valid = 0
    @@task_2_valid = 0

    def check_fields(info)
        required_fields = Set{"byr", "iyr", "eyr", "hgt", "ecl", "hcl", "pid"}
        required_fields.each { |field| return false if !info.includes?(field) }
        @@task_1_valid += 1
        return true
    end

    def run
        passports = File.read("../input").rstrip().split("\n\n")    
        passports.each {|passport| 
            info = passport.gsub("\n", " ")    
            flag = check_fields(info)
            if flag
                byr = /byr:(19[2-9][0-9]|200[0-2])/.match(info)
                iyr = /iyr:(201[0-9]|2020)/.match(info)
                eyr = /eyr:(20[2][0-9]|2030)/.match(info)
                hgt = /hgt:(1[5-8][0-9]cm|19[0-3]cm|59in|6[0-9]in|7[0-3]in)/.match(info)
                hcl = /hcl:#[0-9a-f]{6}/.match(info)
                ecl = /ecl:(amb|blu|brn|gry|grn|hzl|oth)/.match(info)
                pid = /pid:[0-9]{9}/.match(info)
                @@task_2_valid += 1 if byr && iyr && eyr && hgt && hcl && ecl && pid
            end
        }
        puts @@task_1_valid
        puts @@task_2_valid
    end
end
Passport_validator.run
