File.read_lines("input")
    .map(&.split(" = "))
    .each do |a|
        n1, n2 = a[0].split(" to ")
        e = a[1].to_i
        puts [n1, n2, e]
    end

# DefaultHash {name => id}
# Give create graph with input: n1, n2, w
# Call mst method on graph