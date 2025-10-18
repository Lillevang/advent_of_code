defmodule Solution do
  @input File.read!("input")

  # Compass
  @n 0
  @s 180
  @e 90
  @w 270

  # ----- Parsing -----
  defp parse(input) do
    input
    |> String.trim()
    |> String.split()
    |> Enum.map(&String.split_at(&1, 1))
    |> Enum.map(fn {dir, val} -> {direction_to_degree(dir), String.to_integer(val)} end)
  end

  defp direction_to_degree("N"), do: @n
  defp direction_to_degree("S"), do: @s
  defp direction_to_degree("E"), do: @e
  defp direction_to_degree("W"), do: @w
  # "F", "L", "R"
  defp direction_to_degree(other), do: other

  # ----- Part 1 (ship heading) -----
  defp move_ship({dir, x, y}, {@n, v}), do: {dir, x, y + v}
  defp move_ship({dir, x, y}, {@s, v}), do: {dir, x, y - v}
  defp move_ship({dir, x, y}, {@e, v}), do: {dir, x + v, y}
  defp move_ship({dir, x, y}, {@w, v}), do: {dir, x - v, y}
  defp move_ship({@n, x, y}, {"F", v}), do: {@n, x, y + v}
  defp move_ship({@s, x, y}, {"F", v}), do: {@s, x, y - v}
  defp move_ship({@e, x, y}, {"F", v}), do: {@e, x + v, y}
  defp move_ship({@w, x, y}, {"F", v}), do: {@w, x - v, y}
  defp move_ship({dir, x, y}, {"R", deg}), do: {rem(dir + deg, 360), x, y}
  defp move_ship({dir, x, y}, {"L", deg}), do: {rem(dir - deg + 360, 360), x, y}

  defp manhattan_ship({_, x, y}), do: abs(x) + abs(y)

  def part1(input \\ @input) do
    input
    |> parse()
    |> Enum.reduce({@e, 0, 0}, &move_ship(&2, &1))
    |> manhattan_ship()
  end

  # ----- Part 2 (waypoint) -----
  # state: {dx, dy, ship_x, ship_y}
  defp move_waypoint({dx, dy, x, y}, {@n, v}), do: {dx, dy + v, x, y}
  defp move_waypoint({dx, dy, x, y}, {@s, v}), do: {dx, dy - v, x, y}
  defp move_waypoint({dx, dy, x, y}, {@e, v}), do: {dx + v, dy, x, y}
  defp move_waypoint({dx, dy, x, y}, {@w, v}), do: {dx - v, dy, x, y}
  defp move_waypoint({dx, dy, x, y}, {"F", v}), do: {dx, dy, x + dx * v, y + dy * v}
  defp move_waypoint({dx, dy, x, y}, {"R", 90}), do: {dy, -dx, x, y}
  defp move_waypoint({dx, dy, x, y}, {"R", 180}), do: {-dx, -dy, x, y}
  defp move_waypoint({dx, dy, x, y}, {"R", 270}), do: {-dy, dx, x, y}
  defp move_waypoint({dx, dy, x, y}, {"L", 90}), do: {-dy, dx, x, y}
  defp move_waypoint({dx, dy, x, y}, {"L", 180}), do: {-dx, -dy, x, y}
  defp move_waypoint({dx, dy, x, y}, {"L", 270}), do: {dy, -dx, x, y}

  defp manhattan_wp({_, _, x, y}), do: abs(x) + abs(y)

  def part2(input \\ @input) do
    input
    |> parse()
    |> Enum.reduce({10, 1, 0, 0}, &move_waypoint(&2, &1))
    |> manhattan_wp()
  end
end

IO.puts(Solution.part1())
IO.puts(Solution.part2())
