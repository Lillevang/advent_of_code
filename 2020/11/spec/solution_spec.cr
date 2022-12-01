require "spec"
require "../solution.cr"

def test_data
  ["L.LL.LL.LL",
  "LLLLLLL.LL",
  "L.L.L..L..",
  "LLLL.LL.LL",
  "L.LL.LL.LL",
  "L.LLLLL.LL",
  "..L.L.....",
  "LLLLLLLLLL",
  "L.LLLLLL.L",
  "L.LLLLL.LL"]
end

describe "solution" do

  it "can pad the grid correctly" do
    padded_grid = Solution.pad_grid(test_data)
    padded_grid.nil?.should be_falsey
    padded_grid[0].should eq(['.'] * 12)
    padded_grid[-1].should eq(['.'] * 12)
    padded_grid.each do |row|
      row[0].should eq('.')
      row[-1].should eq('.')
    end
  end

  it "can evolve the state correct once" do
    padded_grid = Solution.pad_grid(test_data)
    Solution.evolve_grid(padded_grid).should eq(Solution.pad_grid(["#.##.##.##",
    "#######.##",
    "#.#.#..#..",
    "####.##.##",
    "#.##.##.##",
    "#.#####.##",
    "..#.#.....",
    "##########",
    "#.######.#",
    "#.#####.##"]))
  end
end
