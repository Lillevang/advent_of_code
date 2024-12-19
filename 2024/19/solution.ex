defmodule AOC2024.Day19 do
  def run do
    {:ok, content} = File.read("input")
    [prefix_line, targets_block] = String.split(content, "\n\n", trim: true)
    prefixes = String.split(prefix_line, ", ")
    targets = String.split(targets_block, "\n", trim: true)

    {p1, p2} = Enum.reduce(targets, {0, 0}, fn target, {acc_p1, acc_p2} ->
      target_ways = composable_count(target, prefixes)
      new_p1 = if target_ways > 0, do: acc_p1 + 1, else: acc_p1
      {new_p1, acc_p2 + target_ways}
    end)

    IO.puts(p1)
    IO.puts(p2)
  end

  defp memoize(fun) do
    cache = :persistent_term.get(:cache, nil)

    if cache == nil do
      :persistent_term.put(:cache, :ets.new(:cache, [:named_table, :public, {:read_concurrency, true}]))
    end

    fn key ->
      case :ets.lookup(:persistent_term.get(:cache), key) do
        [{^key, value}] ->
          value

        [] ->
          value = fun.(key)
          :ets.insert(:persistent_term.get(:cache), {key, value})
          value
      end
    end
  end

  def composable_count(s, ws) when is_binary(s) and is_list(ws) do
    memoized_fun = memoize(fn {s, ws} -> composable_count_inner(s, ws) end)
    memoized_fun.({s, ws})
  end

  defp composable_count_inner(s, _ws) when s == "", do: 1


  defp composable_count_inner(s, ws) do
    Enum.reduce(ws, 0, fn word, acc ->
      if String.starts_with?(s, word) do
        acc + composable_count(String.slice(s, String.length(word)..-1//1), ws)
      else
        acc
      end
    end)
  end
end

AOC2024.Day19.run()
