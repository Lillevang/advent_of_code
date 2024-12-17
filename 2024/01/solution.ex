defmodule AOC2024.Day1 do
  # Parse input directly from a file or pre-split lines
  def parse_input(file_path) do
    File.read!(file_path)
    |> String.split("\n", trim: true)
    |> parse_lines()
  end

  def parse_lines(lines) do
    lines
    |> Enum.map(fn line ->
      Regex.split(~r/\s+/, line)
      |> Enum.map(&String.to_integer/1)
      |> List.to_tuple()
    end)
    |> Enum.unzip()
  end
end

defmodule AOC2024.Day1.Part1 do
  def sum_distance({left, right}) do
    left_sorted = Enum.sort(left)
    right_sorted = Enum.sort(right)

    Enum.zip(left_sorted, right_sorted)
    |> Enum.map(fn {a, b} -> abs(a - b) end)
    |> Enum.sum()
  end
end

defmodule AOC2024.Day1.Part2 do
  def similarity_score({left, right}) do
    frequencies = Enum.frequencies(right)

    Enum.reduce(left, 0, fn el, acc ->
      acc + el * Map.get(frequencies, el, 0)
    end)
  end
end

IO.puts(AOC2024.Day1.Part1.sum_distance(AOC2024.Day1.parse_input("./input")))
IO.puts(AOC2024.Day1.Part2.similarity_score(AOC2024.Day1.parse_input("./input")))