require "benchmark"

module Solution
  extend self

  class Node

    include Comparable(Node)

    @connections = [] of Node

    getter value
    getter connections

    def initialize(@value : Int32)
    end

    def set_connections(nodes : Array(Node))
      @connections = nodes.select do |n|
        n.value == @value + 3 || n.value == @value + 2 || n.value == @value + 1
      end
    end

    def <=>(other : Node)
      return -1 if @value < other.value
      return 0 if @value == other.value
      return 1 if @value > other.value
    end
  end

  class Graph

    @nodes = [] of Node

    # Part two specific (DFS)
    @starting_node : Node | Nil
    @exit_node : Node | Nil
    @visited = Hash(Int32, Bool).new
    @current_path = [] of Node
    @simple_paths = [] of Array(Node)

    # Part two specific (DP)
    @dp_dict = Hash(Int64, Int64).new

    getter nodes
    getter starting_node
    getter exit_node
    getter simple_paths

    def initialize(nums : Array(Int32))
      @nodes = nums.map do |n|
        Node.new(n)
      end
      @nodes.each(&.set_connections(@nodes))
    end

    def add_start_node
      @starting_node = Node.new(0)
      @starting_node.not_nil!.set_connections(@nodes)
      @nodes << @starting_node.not_nil!
    end

    def add_exit_node
      cur_max_node = @nodes.max
      @exit_node = Node.new(cur_max_node.value + 3)
      @nodes << @exit_node.not_nil!
      cur_max_node.set_connections(@nodes)
    end

    # Solution works, but is not scalable
    def dfs(start : Node, target : Node)
      return if @visited.has_key?(start.value) && @visited[start.value]
      @visited[start.value] = true
      @current_path << start
      if start == target
        @simple_paths << @current_path
        @visited[start.value] = false
        @current_path.pop
        return
      end
      start.connections.each do |n|
        dfs(n, target)
      end
      @current_path.pop
      @visited[start.value] = false
    end

    def dp(i : Int32)
      # Assumes that the nodes array is sorted
      return 1 if i == @nodes.size - 1
      return @dp_dict[i] if @dp_dict.keys.includes?(i)
      ans = 0.to_i64
      ((i+1)...@nodes.size).each do |j|
        if @nodes[j].value - @nodes[i].value <= 3
          ans += dp(j)
        end
      end
      @dp_dict[i] = ans
      ans
    end

    def sort_nodes
      @nodes = @nodes.sort
    end

  end

  # Solution

  def create_adapter_sequence(graph : Graph)
    ones =  0
    threes = 0
    graph.nodes.each do |n|
      unless n.connections.empty?
        ones += 1 if n.connections.min.value - n.value == 1
        threes += 1 if n.connections.min.value - n.value == 3
      end
    end
    ones * threes
  end

  def read_input
    File.read("./input").split("\n").select{|n| n != ""}.map(&.to_i)
  end

  def create_graph
    graph = Graph.new(read_input)
    graph.add_start_node
    graph.add_exit_node
    graph.sort_nodes
    graph
  end

  def part_one
    p create_adapter_sequence(create_graph)
  end

  def part_two
    p create_graph.dp(0)
  end
end


# Benchmarking
# Dynamic programming is far, far superior:
# DFS  75.51  ( 13.24ms) (±25.66%)  948kB/op  37903.11× slower
#  DP   2.86M (349.42ns) (±20.58%)   304B/op           fastest

#def example_input
#  [28, 33, 18, 42, 31, 14, 46, 20, 48, 47, 24, 23, 49, 45, 19, 38, 39, 11, 1, 32, 25, 35, 8, 17, 7, 9, 4, 2, 34, 10, 3]
#end

#graph = Solution::Graph.new(example_input)
#graph.add_start_node
#graph.add_exit_node
#graph.sort_nodes

#Benchmark.ips do |x|
#  x.report("DFS") {graph.dfs(graph.starting_node.not_nil!, graph.exit_node.not_nil!)}
#  x.report("DP") {graph.dp(0)}
#end

