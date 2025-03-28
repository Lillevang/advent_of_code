defmodule AoC2023.Day02 do
  @red_limit 12
  @green_limit 13
  @blue_limit 14

  def run do
    # Parse the file contents once
    puzzle_data =
      File.read!("./input")
      |> parse_input()

    # Now we can run both parts without re-parsing
    IO.puts(part1(puzzle_data))
    IO.puts(part2(puzzle_data))
  end

  # Part 1: Filter out any game whose sets exceed the R/G/B limits.
  #         Then sum all such game IDs.
  def part1(games) do
    games
    |> Enum.filter(fn {_id, sets} ->
      Enum.all?(sets, fn set ->
        Map.get(set, "red", 0)   <= @red_limit and
        Map.get(set, "green", 0) <= @green_limit and
        Map.get(set, "blue", 0)  <= @blue_limit
      end)
    end)
    |> Enum.map(fn {id, _sets} -> id end)
    |> Enum.sum()
  end

  # Part 2: For each game, merge its sets so that for each color
  #         we take the maximum usage across all sets. Multiply
  #         the red/green/blue usage, then sum over all games.
  def part2(games) do
    games
    |> Enum.map(fn {_id, sets} ->
      Enum.reduce(sets, %{}, fn set, acc ->
        Map.merge(acc, set, fn _color, v1, v2 -> max(v1, v2) end)
      end)
    end)
    |> Enum.map(fn usage_map ->
      (usage_map["red"]   || 0) *
      (usage_map["green"] || 0) *
      (usage_map["blue"]  || 0)
    end)
    |> Enum.sum()
  end

  defp parse_input(puzzle_input) do
    puzzle_input
    |> String.split("\n", trim: true)
    |> Enum.map(&parse_line/1)
  end

  defp parse_line(line) do
    [id_part | sets_part] = String.split(line, ~r/[:;]/, trim: true)

    [id_string] = Regex.run(~r/\d+/, id_part)
    id = String.to_integer(id_string)

    sets =
      sets_part
      |> Enum.map(&parse_set/1)

    {id, sets}
  end

  defp parse_set(string) do
    ~r/(\d+) (\w+)/
    |> Regex.scan(string, capture: :all_but_first)
    |> Map.new(fn [count, color] ->
      {color, String.to_integer(count)}
    end)
  end
end

AoC2023.Day02.run()
