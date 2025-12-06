defmodule Solution do
  @input File.read!("input")

  @operations %{
    "*" => &Kernel.*/2,
    "+" => &Kernel.+/2
  }

  # Parsing
  # Token grid
  defp read_input_part1(input) do
    input
    |> String.split("\n", trim: true)
    |> Enum.map(&String.split/1)
  end

  # Char grid
  defp read_input_part2(input) do
    input
    |> String.split("\n", trim: true)
    |> Enum.map(fn line ->
      (line <> " ") |> String.graphemes()
    end)
  end

  # Parse a list of single-char strings into an int
  defp parse_digits(chars) do
    s = chars |> Enum.join() |> String.trim()
    if s == "", do: nil, else: String.to_integer(s)
  end

  defp columns(rows, fill \\ nil) do
    max_cols =
      rows
      |> Enum.map(&length/1)
      |> Enum.max(fn -> 0 end)

    for idx <- 0..(max_cols - 1) do
      Enum.map(rows, &Enum.at(&1, idx, fill))
    end
  end

  # Solutions
  def part1(input \\ @input) do
    rows = read_input_part1(input)

    rows
    |> columns()
    |> Enum.reduce(0, fn col, acc ->
      {nums, [op_symbol]} = Enum.split(col, -1)
      op = Map.fetch!(@operations, op_symbol)

      digits =
        nums
        |> Enum.reject(&is_nil/1)
        |> Enum.map(&String.to_integer/1)

      acc + Enum.reduce(digits, op)
    end)
  end

  def part2(input \\ @input) do
    rows = read_input_part2(input)

    {total, op, digits} =
      rows
      |> columns(" ")
      |> Enum.reduce({0, nil, []}, fn col, {total, op, digits} ->
        {data, [key]} = Enum.split(col, -1)

        op =
          case Map.get(@operations, key) do
            nil -> op
            fun -> fun
          end

        value = parse_digits(data)

        cond do
          value != nil ->
            {total, op, [value | digits]}

          digits != [] and op != nil ->
            result = digits |> Enum.reverse() |> Enum.reduce(op)
            {total + result, op, []}

          true ->
            {total, op, digits}
        end
      end)

    if digits != [] and op != nil do
      total + (digits |> Enum.reverse() |> Enum.reduce(op))
    else
      total
    end
  end
end

IO.puts(Solution.part1())
IO.puts(Solution.part2())
