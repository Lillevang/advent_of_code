defmodule AOC2024.Day13 do
  def run do
    input = File.read!("input")
    groups = String.split(input, "\n\n")

    # Run for part 1 with offset 0.0
    IO.puts(process_groups(groups, 0.0))

    # Run for part 2 with offset 10_000_000_000_000.0
    IO.puts(process_groups(groups, 10_000_000_000_000.0))
  end

  defp process_groups(groups, offset) do
    Enum.reduce(groups, 0, fn group, total ->
      lines = String.split(group, "\n")

      # Extract coordinates for Button A and Button B
      {button_a_x, button_a_y} = extract_coordinates(Enum.at(lines, 0))
      {button_b_x, button_b_y} = extract_coordinates(Enum.at(lines, 1))

      # Extract and adjust coordinates for the prize
      {prize_x, prize_y} =
        extract_coordinates(Enum.at(lines, 2))
        |> apply_offset(offset)

      # Calculate coefficient_b based on prize and button coordinates
      coefficient_b = (prize_x * button_a_y - prize_y * button_a_x) / (button_a_y * button_b_x - button_a_x * button_b_y)

      # Calculate coefficient_a based on coefficient_b and prize coordinates
      coefficient_a = (prize_y - coefficient_b * button_b_y) / button_a_y

      # Validate the combination and update the total points
      if valid_combination?(coefficient_a, coefficient_b, button_a_x, button_a_y, button_b_x, button_b_y, prize_x, prize_y, offset == 0.0) do
        total + round(coefficient_a) * 3 + round(coefficient_b)
      else
        total
      end
    end)
  end

  # Extract coordinates from a line using regex
  defp extract_coordinates(line) do
    [_, x_str, y_str] = Regex.run(~r/X[+=]?(\d+(?:\.\d+)?), Y[+=]?(\d+(?:\.\d+)?)/, line)
    {x, _} = Float.parse(x_str)
    {y, _} = Float.parse(y_str)
    {x, y}
  end

  # Apply an offset to a pair of coordinates
  defp apply_offset({x, y}, offset), do: {x + offset, y + offset}

  # Validate the calculated coefficients against prize coordinates
  defp valid_combination?(coefficient_a, coefficient_b, button_a_x, button_a_y, button_b_x, button_b_y, prize_x, prize_y, is_part1) do
    rounded_a = round(coefficient_a)
    rounded_b = round(coefficient_b)

    rounded_a * button_a_x + rounded_b * button_b_x == prize_x and
      rounded_a * button_a_y + rounded_b * button_b_y == prize_y and
      (not is_part1 or (coefficient_a <= 100.0 and coefficient_b <= 100.0))
  end
end

AOC2024.Day13.run()
