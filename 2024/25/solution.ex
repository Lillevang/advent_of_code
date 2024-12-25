defmodule AOC2024.Day25 do
  def run() do
    data = File.read!("input") |> String.trim()
    shapes = String.split(data, "\n\n", trim: true)

    # Separate shapes into keys and locks
    {keys, locks} =
      Enum.reduce(shapes, {[], []}, fn shape, {keys_acc, locks_acc} ->
        lines = String.split(shape, "\n", trim: true)

        grid = Enum.map(lines, &String.graphemes/1)

        # A shape is a "key" if the top row contains no '#'
        top_row = hd(grid)
        is_key = Enum.all?(top_row, &(&1 != "#"))

        if is_key do
          {[shape | keys_acc], locks_acc}
        else
          {keys_acc, [shape | locks_acc]}
        end
      end)

    # Reverse so keys and locks are in the original order
    keys = Enum.reverse(keys)
    locks = Enum.reverse(locks)

    # Count how many key-lock pairs fit
    answer =
      Enum.reduce(keys, 0, fn key, acc ->
        acc +
          Enum.count(locks, fn lock -> fits?(key, lock) end)
      end)

    IO.puts(answer)
  end

  # Converts a multi-line shape string into a list-of-lists of characters
  defp parse_shape(shape) do
    shape
    |> String.split("\n", trim: true)
    |> Enum.map(&String.graphemes/1)
  end

  # Checks if key fits into lock (returns true or false)
  defp fits?(key_str, lock_str) do
    key = parse_shape(key_str)
    lock = parse_shape(lock_str)

    if length(key) != length(lock),
      do: raise("Key and lock row counts differ.")

    if length(hd(key)) != length(hd(lock)),
      do: raise("Key and lock column counts differ.")

    # If any corresponding position in both key and lock is '#', they do not fit
    Enum.with_index(key)
    |> Enum.all?(fn {row_k, r} ->
      row_l = Enum.at(lock, r)

      Enum.with_index(row_k)
      |> Enum.all?(fn {char_k, c} ->
        char_l = Enum.at(row_l, c)
        not (char_k == "#" and char_l == "#")
      end)
    end)
  end
end

AOC2024.Day25.run()
