require "../../utility/crystal/grid_padder"

DATA = File.read("./example").strip().split("\n")
GRID = GridPadder.pad_grid(DATA, ".")
START = 1
END = GRID[0].size - 2

def print_layout(grid : Array(String))
  grid.each do |l|
    p l
  end
end

grid = GRID
stable = false
# TODO create state object to store each state in?

while !stable
  new_grid = [] of String

end
