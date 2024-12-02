REQUIRED_FIELDS = Set{"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}
VALID_EYE_COLORS = Set{"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}

def valid_field?(field, value)
    case field
    when "byr" then 1920 <= value.to_i <= 2002
    when "iyr" then 2010 <= value.to_i <= 2020
    when "eyr" then 2020 <= value.to_i <= 2030
    end
end

passports = File.read("../input").split("\n\n").map do |raw_passport|
    t = raw_passport.scan(/(\w+):(\S+)/)#.to_h
    puts t.to_h
    #t.to_h
end

# passports_with_required_fields = passports.select do |passport|
#     REQUIRED_FIELDS.all? { |field| 
#     passport.has_value?(field) }
# end

# required_and_valid_count = passports_with_required_fields.each do |passport|
#     passport.all? { |field, value| valid_field?(field, value) }
# end

# puts "Part 1:", passports_with_required_fields.size
# puts "Part 2:", required_and_valid_count
