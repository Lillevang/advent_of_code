module GridPadder
  extend self

  # TODO Could probably be generalized more?
  def pad_grid(grid : Array(String), token : String) : Array(String)
    padded_grid = Array(String).new
    padded_grid << token * (grid[0].size + 2)
    grid.each do |row|
      padded_grid << "#{token}#{row}#{token}"
    end
    padded_grid << token * (grid[0].size + 2)
    padded_grid
  end
end
