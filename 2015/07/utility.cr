# This script converts the input to a hash of name => expression mappings. This is copy pasted from terminal into the solution.

TRANSFORMS = {
"LSHIFT"         => "<<",
"RSHIFT"         => ">>",
"NOT"            => "~",
"AND"            => "&",
"OR"             => "|",
/\b(if|do|in)\b/ => "\\1_",
}

File.read_lines("input").each do |line|
    TRANSFORMS.each do |from, to|
        unless line.gsub(from, to) == line
          line = line.gsub(from, to)
        end
    end
    tmp = line.split(" -> ")
    puts "#{tmp[1]} => #{tmp[0]},"
end
