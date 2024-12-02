defmodule AOC2024Day1 do
  def read_input(file_path) do
      File.read!(file_path)
      |> String.split("\n", trim: true)
      |> Enum.map(fn line ->
        case String.split(line, "   ") do
            [left, right] -> {String.to_integer(left), String.to_integer(right)}
        end
      end)
      |> Enum.unzip()
  end

  # Part 1: Calculate the sum of absolute differences
  def part1({left_list, right_list}) do
    left_list
    |> Enum.sort()
    |> Enum.zip(Enum.sort(right_list))
    |> Enum.map(fn {left, right} -> abs(left - right) end)
    |> Enum.sum()
  end

  # Part 2: Calculate the weighted sum based on frequency in right list
  def part2({left_list, right_list}) do
    freqs_right = Enum.frequencies(right_list)
    left_list
    |> Enum.reduce(0, fn num, acc -> 
        acc + num * Map.get(freqs_right, num, 0)
    end)
  end

  # Run both parts
  def solve(file_path) do
    {left_list, right_list} = read_input(file_path)
    part1_score = part1({left_list, right_list})
    part2_score = part2({left_list, right_list})

    IO.puts("Part 1: #{part1_score}")
    IO.puts("Part 2: #{part2_score}")
  end
end

AOC2024Day1.solve("./input")