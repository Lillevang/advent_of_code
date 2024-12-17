require "spec"
require  "../solution.cr"

def example_input
    [28, 33, 18, 42, 31, 14, 46, 20, 48, 47, 24, 23, 49, 45, 19, 38, 39, 11, 1, 32, 25, 35, 8, 17, 7, 9, 4, 2, 34, 10, 3]
end

def create_graph
  graph = Solution:: Graph.new(example_input)
  graph.add_start_node
  graph.add_exit_node
  graph.sort_nodes
  graph
end

describe "solution" do

    it "creates a graph" do
        Solution::Graph.new(example_input).nil?.should be_falsey
    end

    it "should create a node for each number" do
        Solution::Graph.new(example_input).nodes.size.should eq(example_input.size)
    end

    it "should create the starting node" do
        graph = Solution::Graph.new(example_input)
        graph = graph.add_start_node
        graph[-1].value.should eq(0)
        graph[-1].connections.empty?.should be_falsey
    end

    it "should be able to sort the graph" do
        graph = Solution::Graph.new(example_input)
        graph = graph.add_start_node
        x = graph.sort
        x[0].value.should eq(0)
        x[1].value.should eq(1)
        x[2].value.should eq(2)
        x[-1].value.should eq(49)
    end

    it "should be able to create the exit node" do
        graph = create_graph
        graph.nodes[0].value.should eq(0)
        graph.nodes[1].value.should eq(1)
        graph.nodes[2].value.should eq(2)
        graph.nodes[-1].value.should eq(52)
    end

    it "should be able to create an adapter sequence" do
        graph = create_graph
        Solution.create_adapter_sequence(graph).should eq(22 * 10)
    end

    it "solves part one" do
        Solution.part_one
    end

    it "solves part two with DFS and test data" do
      graph = create_graph
      graph.dfs(graph.starting_node.not_nil!, graph.exit_node.not_nil!)
      graph.simple_paths.size.should eq(19208)
    end

    it "solves part two with dynamic programming and test data" do
      graph = create_graph
      graph.dp(0).should eq(19208)
    end

    it "solves part two with real data" do
      Solution.part_two
    end

end
