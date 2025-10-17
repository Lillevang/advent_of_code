require "collections"

edges = File.read_lines("input")
graph = Collections::Graph(String).new

edges.each do |edge|
  v1, v2 = edge.split("-")
  graph.add_edge(v1, v2)
end

# Part 1: Subgraphs of size 3
filtered_subgraphs = graph.find_subgraphs(3).select do |subgraph|
  subgraph.any? { |node| node.starts_with?("t") }
end
puts "Part 1: #{filtered_subgraphs.size}"

# Part 2: Largest clique
largest_clique_result = graph.largest_clique
puts largest_clique_result.join(",")