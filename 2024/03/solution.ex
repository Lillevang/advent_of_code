defmodule AOC2024.Day3 do
  @input_file "input"
  @mul_func ~r/mul\((\d+),(\d+)\)/
  @dont_do ~r/don't\(\).*?(?:do\(\)|$)/

  def run(filename \\ @input_file) do
    input = read_input(filename)

    part1_result = input
    |> multiply()
    
    part2_result = input
    |> ignore_donts()
    |> multiply()

    IO.inspect(part1_result, label: "Part 1")
    IO.inspect(part2_result, label: "Part 2")
  end

  def read_input(file_path) do
    File.read!(file_path)
    |> String.trim()
    |> String.split("\n")
    |> Enum.join("")
  end

  defp multiply(input) do
    Regex.scan(@mul_func, input)
    |> Enum.map(fn [_ | numbers] ->
      numbers
      |> Enum.map(&String.to_integer/1)
      |> Enum.product()
    end)
    |> Enum.sum()
  end

  defp ignore_donts(input) do
    Regex.replace(@dont_do, input, "")
  end
end

AOC2024.Day3.run()
