distances = Hash(Tuple(String, String), Int32).new
cities = Set(String).new

File.read_lines("input")
    .each do |line|
        parts = line.split(" to ")
        city1 = parts[0]
        rest = parts[1].split(" = ")
        city2 = rest[0]
        distance = rest[1].to_i
        city_pair = city1 < city2 ? {city1, city2} : {city2, city1}
        distances[city_pair] = distance
        cities << city1
        cities << city2
    end

shortest_distance = Int32::MAX
longest_distance = 0
shortest_path = [] of String
longest_path = [] of String

cities.to_a.permutations.each do |perm|
    total_distance = 0
    valid_path = true
    (0...perm.size - 1).each do |i|
        city_pair = perm[i] < perm[i + 1] ? {perm[i], perm[i + 1]} : {perm[i + 1], perm[i]}
        if distances.has_key?(city_pair)
            total_distance += distances[city_pair]
        else
            valid_path = false
            break
        end
    end
    if valid_path && total_distance < shortest_distance
        shortest_distance = total_distance
        shortest_path = perm
    elsif valid_path && total_distance > longest_distance
        longest_distance = total_distance
        longest_path = perm
    end
end
shortest_path_string = shortest_path.join(" -> ")
longest_path_string = longest_path.join(" -> ")
puts "Shortest path: #{shortest_path_string}"
puts "Distance: #{shortest_distance}"
puts ""
puts "Longest path: #{longest_path_string}"
puts "Distance: #{longest_distance}"

            
