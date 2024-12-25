defmodule AOC2024.Day24 do
  import Bitwise

  def run do
    input = File.read!("input") |> String.trim()

    case String.split(input, ~r/\n{2,}/) do
      [inps, gates] ->
        vals =
          inps
          |> String.split("\n")
          |> Enum.reduce(%{}, fn line, acc ->
            [gate, val] = String.split(line, ": ")
            Map.put(acc, gate, String.to_integer(val))
          end)

        gatez =
          gates
          |> String.split("\n")
          |> Enum.reduce(%{}, fn line, acc ->
            [expr, out] = String.split(line, " -> ")
            Map.put(acc, out, expr)
          end)

        outs =
          Map.keys(vals) ++ Map.keys(gatez)
          |> Enum.uniq()
          |> Enum.filter(&String.starts_with?(&1, "z"))

        outs
        |> Enum.sort()
        |> Enum.map(&evaluate(&1, vals, gatez))
        |> Enum.reverse()
        |> Integer.undigits(2)
        |> IO.puts()

      _ ->
        IO.puts("Input file format is invalid. Ensure it contains two sections separated by a blank line.")
    end
  end

  defp evaluate(g, vals, _gatez) when is_map_key(vals, g), do: vals[g]

  defp evaluate(g, vals, gatez) do
    [a, op, b] = String.split(gatez[g], " ")

    case op do
      "AND" -> evaluate(a, vals, gatez) &&& evaluate(b, vals, gatez)
      "OR" -> evaluate(a, vals, gatez) ||| evaluate(b, vals, gatez)
      "XOR" -> Bitwise.bxor(evaluate(a, vals, gatez), evaluate(b, vals, gatez))
    end
  end
end

AOC2024.Day24.run()
