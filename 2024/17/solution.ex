import Bitwise
defmodule AOC2024.Day17 do
  # Load and parse the input file
  def load_input(file) do
    {:ok, data} = File.read(file)
    Regex.scan(~r/\d+/, data)
    |> Enum.map(fn [x] -> String.to_integer(x) end)
  end

  # The run function processes the program instructions
  def run(prog, a) do
    process(prog, a, 0, 0, 0, [])
  end

  defp process(prog, _a, _b, _c, ip, out) when ip < 0 or ip >= length(prog), do: out
  # Process instructions with a state machine
  defp process(prog, a, b, c, ip, out) do
    table = [0, 1, 2, 3, a, b, c, 99_999]
    operand = Enum.at(prog, ip + 1, 0)
    combo = Enum.at(table, operand, 0)

    case Enum.at(prog, ip) do
      0 -> process(prog, a >>> combo, b, c, ip + 2, out)
      1 -> process(prog, a, Bitwise.bxor(b, operand), c, ip + 2, out)
      2 -> process(prog, a, rem(combo, 8), c, ip + 2, out)
      3 -> process(prog, a, b, c, if(a == 0, do: ip + 2, else: operand), out)
      4 -> process(prog, a, Bitwise.bxor(b, c), c, ip + 2, out)
      5 -> process(prog, a, b, c, ip + 2, List.insert_at(out, -1, rem(combo, 8)))
      6 -> process(prog, a, a >>> combo, c, ip + 2, out)
      7 -> process(prog, a, b, a >>> combo, ip + 2, out)
      _ -> out
    end
  end

  # Part 2 - Recursive search for finding A
  def find_a(prog, target) do
    search_a(prog, target, 0, 0)
  end

  defp search_a(_prog, target, a, depth) when depth == length(target), do: a

  defp search_a(prog, target, a, depth) do
    Enum.reduce_while(0..7, 0, fn i, _acc ->
      output = run(prog, a * 8 + i)
      if output != [] and hd(output) == Enum.at(target, depth) do
        case search_a(prog, target, a * 8 + i, depth + 1) do
          0 -> {:cont, 0}
          result -> {:halt, result}
        end
      else
        {:cont, 0}
      end
    end)
  end

  # Main function to solve Part 1 and Part 2
  def solve(file) do
    [a, _b, _c | prog] = load_input(file)

    IO.puts("Part 1:")
    part1 = run(prog, a)
    IO.puts(Enum.join(part1, ","))

    IO.puts("Part 2:")
    target = Enum.reverse(prog)
    result = find_a(prog, target)
    IO.puts(result)
  end
end

# Run the solution
AOC2024.Day17.solve("input")
