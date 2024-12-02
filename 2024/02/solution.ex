defmodule AOC2024.Day2 do
  def run do
    data = File.read!("./input") |> String.trim() |> String.split("\n")

    {part_1, part_2} =
      Enum.reduce(data, {0, 0}, fn line, {count_1, count_2} ->
        report = parse_report(line)

        part_1_increment = if valid_report?(report), do: 1, else: 0
        part_2_increment = if single_removal_valid?(report), do: 1, else: 0

        {count_1 + part_1_increment, count_2 + part_2_increment}
      end)

    IO.puts("Part 1: #{part_1}")
    IO.puts("Part 2: #{part_2}")
  end

  # Parse a line into a list of integers
  defp parse_report(line), do: line |> String.split() |> Enum.map(&String.to_integer/1)

  # Check if the report is valid 
  defp valid_report?(report) do
    sorted? = report == Enum.sort(report) or report == Enum.sort(report, :desc)

    valid_differences? =
      report
      |> Enum.chunk_every(2, 1, :discard)
      |> Enum.all?(fn [a, b] -> abs(a - b) in 1..3 end)

    sorted? and valid_differences?
  end

  # Check if removing one element can make the report valid
  defp single_removal_valid?(report) do
    report
    |> Enum.with_index()
    |> Enum.any?(fn {_, idx} -> valid_report?(List.delete_at(report, idx)) end)
  end
end

AOC2024.Day2.run()
