# TODO: Review if we prefer this over last years approach?
defmodule Day01 do
  @dial_size 100
  @start_pos 50

  @type direction :: :left | :right
  @type move :: {direction(), non_neg_integer()}

  # Entry point
  # TODO: Extract into helper in template?
  def main(file \\ "input") do
    moves = file |> File.read!() |> parse_moves()

    IO.puts("Part 1: #{compute_password(moves)}")
    IO.puts("Part 2: #{compute_password_method_click(moves)}")
  end

  ## Parsing

  # Trying the elixir type hinting thing...
  @spec parse_moves(String.t()) :: [move()]
  def parse_moves(raw) do
    raw
    |> String.split("\n", trim: true)
    |> Enum.map(&parse_move/1)
  end

  @spec parse_move(String.t()) :: move()
  defp parse_move(<<"L", rest::binary>>), do: {:left, String.to_integer(rest)}
  defp parse_move(<<"R", rest::binary>>), do: {:right, String.to_integer(rest)}

  defp parse_move(<<dir, _::binary>>) do
    raise "Invalid direction: #{<<dir>>}"
  end

  ## Part 1

  @spec compute_password([move()]) :: non_neg_integer()
  def compute_password(moves) do
    {_pos, hits} =
      Enum.reduce(moves, {@start_pos, 0}, fn {dir, dist}, {pos, hits} ->
        pos = move(pos, dir, dist)
        hits = if pos == 0, do: hits + 1, else: hits
        {pos, hits}
      end)

    hits
  end

  ## Part 2

  @spec compute_password_method_click([move()]) :: non_neg_integer()
  def compute_password_method_click(moves) do
    {_pos, hits} =
      Enum.reduce(moves, {@start_pos, 0}, fn {dir, dist}, {pos, hits} ->
        hits = hits + count_zero_hits_during_rotation(pos, dir, dist)
        pos = move(pos, dir, dist)
        {pos, hits}
      end)

    hits
  end

  @spec count_zero_hits_during_rotation(non_neg_integer(), direction(), integer()) ::
          non_neg_integer()
  def count_zero_hits_during_rotation(_pos, _dir, distance) when distance <= 0, do: 0

  def count_zero_hits_during_rotation(pos, :right, distance) do
    first_step = Integer.mod(@dial_size - pos, @dial_size)
    zero_hits(first_step, distance)
  end

  def count_zero_hits_during_rotation(pos, :left, distance) do
    first_step = Integer.mod(pos, @dial_size)
    zero_hits(first_step, distance)
  end

  defp zero_hits(first_step, distance) do
    step = if first_step == 0, do: @dial_size, else: first_step

    if distance < step do
      0
    else
      1 + div(distance - step, @dial_size)
    end
  end

  ## Shared helpers

  @spec move(non_neg_integer(), direction(), integer()) :: non_neg_integer()
  defp move(pos, :right, distance),
    do: Integer.mod(pos + distance, @dial_size)

  defp move(pos, :left, distance),
    do: Integer.mod(pos - distance, @dial_size)
end

Day01.main("input")
