defmodule AOC2024.Day12 do
  def transform(counts) do
    Enum.reduce(counts, %{}, fn {s, cnt}, acc ->
      cond do
        s == "0" ->
          Map.update(acc, "1", cnt, &(&1 + cnt))

        rem(String.length(s), 2) == 0 ->
          # Even number of digits => split
          digits = String.length(s)
          half = div(digits, 2)
          {left_part, right_part} = String.split_at(s, half)

          acc
          |> Map.update(String.to_integer(left_part) |> Integer.to_string(), cnt, &(&1 + cnt))
          |> Map.update(String.to_integer(right_part) |> Integer.to_string(), cnt, &(&1 + cnt))

        true ->
          # Odd number of digits => multiply by 2024
          val = String.to_integer(s) * 2024
          Map.update(acc, Integer.to_string(val), cnt, &(&1 + cnt))
      end
    end)
  end

  def run do
    counts = 
      File.read!("input")
      |> String.trim()
      |> String.split()
      |> Enum.frequencies()

    # Apply 75 transformations
    apply_transformations(counts, 75, 1)
  end

  defp apply_transformations(counts, 0, _current_iteration), do: counts

  defp apply_transformations(counts, remaining_iterations, current_iteration) do
    updated_counts = transform(counts)

    if current_iteration == 25 do
      IO.puts("Part 1: #{Enum.reduce(updated_counts, 0, fn {_key, val}, acc -> acc + val end)}")
    end

    if remaining_iterations == 1 do
      IO.puts("Part 2: #{Enum.reduce(updated_counts, 0, fn {_key, val}, acc -> acc + val end)}")
    end

    apply_transformations(updated_counts, remaining_iterations - 1, current_iteration + 1)
  end
end

AOC2024.Day12.run()