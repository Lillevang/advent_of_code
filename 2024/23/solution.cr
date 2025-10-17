require "collections"

edges = File.read_lines("input")
graph = Collections::Graph(String).new

edges.each do |edge|
  v1, v2 = edge.split("-")
  graph.add_edge(v1, v2)
end


def fully_connected?(graph : Collections::Graph(String), nodes : Array(String)) : Bool
  nodes.each_with_index do |node1, i|
    ((i + 1)...nodes.size).each do |j|
      node2 = nodes[j]
      neighbors = graph.neighbors(node1) || [] of Collections::Node(String)
      return false unless neighbors.any? { |neighbor| neighbor.value == node2 }
    end
  end
  true
end

# Optimized method to find subgraphs of size 3
def find_filtered_subgraphs(graph : Collections::Graph(String)) : Array(Array(String))
  subgraphs = Set(Array(String)).new

  # Focus only on nodes starting with "t"
  target_nodes = graph.adjacency_list.keys.select { |node| node.value.starts_with?("t") }

  target_nodes.each do |node|
    # Explore all combinations of 2 neighbors with the node itself
    neighbors = graph.neighbors(node.value) || [] of Collections::Node(String)
    neighbors.combinations(2).each do |combination|
      subgraph = ([node.value] + combination.map(&.value)).sort
      if fully_connected?(graph, subgraph) && subgraphs.add?(subgraph)
        # Add unique subgraph to the set
        subgraphs << subgraph
      end
    end
  end

  subgraphs.to_a
end

# Find the largest clique in the graph
def largest_clique(graph : Collections::Graph(String)) : Array(String)
  nodes = graph.adjacency_list.keys.map(&.value) # Get all node values
  nodes = nodes.sort_by { |node| -(graph.neighbors(node) || [] of String).size } # Sort by degree (descending)
  max_clique = [] of String

  backtrack(graph, [] of String, nodes, max_clique) # Call the backtracking function
  max_clique.sort
end

# Backtracking to find the largest clique
def backtrack(graph : Collections::Graph(String), current_clique : Array(String), candidates : Array(String), max_clique : Array(String))
  if candidates.empty?
    if current_clique.size > max_clique.size
      max_clique.clear
      max_clique.concat(current_clique)
    end
    return
  end

  candidates.each_with_index do |candidate, i|
    # Extend the current clique
    new_clique = current_clique + [candidate]
    # Filter candidates to keep only neighbors of the current candidate
    new_candidates = candidates[(i + 1)..-1].select do |other|
      neighbors = graph.neighbors(candidate) || [] of Collections::Node(String)
      neighbors.any? { |neighbor| neighbor.value == other }
    end
    # Recurse
    backtrack(graph, new_clique, new_candidates, max_clique)
  end
end

# Part 1
filtered_subgraphs = find_filtered_subgraphs(graph)
puts "Part 1: #{filtered_subgraphs.size}"

# Part 2
largest_clique_result = largest_clique(graph)
puts largest_clique_result.join(",")
