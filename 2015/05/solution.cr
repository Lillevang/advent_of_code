input_data = File.read("./input").split("\n")

# Part one
DOUBLE_LETTERS = /([a-z])\1/
ILLEGAL_LETTERS = /ab|cd|pq|xy/

p "Part One: #{input_data.count { |w|  w.count("aeiou") >= 3 && DOUBLE_LETTERS.match(w) && ILLEGAL_LETTERS.match(w).nil? }}"


# Part two
input_data.select! do |w|
    w.chars.each_cons(3).any? { |a| a[0] == a[2] }
end

input_data.select! do |w|
    (w.size - 3).times.any? do |idx|
        pair = w[idx, 2]
        w[(idx + 2)..-1].chars
            .each_cons(2)
            .map(&.join)
            .any? { |pair2| pair2 == pair }
    end
end

p "Part Two: #{input_data.size}"