defmodule Solution do
  @dirs [{1, 1}, {1, 0}, {1, -1}, {0, 1}, {0, -1}, {-1, 1}, {-1, 0}, {-1, -1}]

  def run do
    {rows, cols, seats, occupied} = parse("input")
    adj = neighbors(seats, rows, cols, :adjacent)
    vis = neighbors(seats, rows, cols, :visible)

    p1 = solve(occupied, adj, 4)
    p2 = solve(occupied, vis, 5)

    IO.puts("""
    Part 1: #{p1}

    Part 2: #{p2}
    """)
  end

  # parsing

  defp parse(path) do
    lines = path |> File.read!() |> String.split("\n", trim: true)
    rows = length(lines)
    cols = lines |> hd() |> String.length()

    {seats, occupied} =
      lines
      |> Enum.with_index()
      |> Enum.reduce({Map.new(), Map.new()}, fn {line, r}, {seats_acc, occ_acc} ->
        line
        |> :binary.bin_to_list()
        |> Enum.with_index()
        |> Enum.reduce({seats_acc, occ_acc}, fn {ch, c}, {sacc, oacc} ->
          i = r * cols + c

          case ch do
            # floor not stored
            ?. -> {sacc, oacc}
            # empty seat
            ?L -> {Map.put(sacc, i, ?L), oacc}
            # occupied
            ?# -> {Map.put(sacc, i, ?#), Map.put(oacc, i, true)}
          end
        end)
      end)

    {rows, cols, seats, occupied}
  end

  # neighbor precomputation

  defp neighbors(seats, rows, cols, :adjacent) do
    for {i, _} <- seats, into: %{} do
      {r, c} = {div(i, cols), rem(i, cols)}

      ns =
        for {dr, dc} <- @dirs,
            nr = r + dr,
            nc = c + dc,
            nr >= 0 and nr < rows and nc >= 0 and nc < cols,
            j = nr * cols + nc,
            # only seats
            Map.has_key?(seats, j),
            do: j

      {i, ns}
    end
  end

  defp neighbors(seats, rows, cols, :visible) do
    seat_index? = &Map.has_key?(seats, &1)

    for {i, _} <- seats, into: %{} do
      {r, c} = {div(i, cols), rem(i, cols)}

      ns =
        for {dr, dc} <- @dirs do
          find_first_seat(r + dr, c + dc, dr, dc, rows, cols, seat_index?)
        end
        |> Enum.filter(& &1)

      {i, ns}
    end
  end

  defp find_first_seat(r, c, dr, dc, rows, cols, seat_index?) do
    cond do
      r < 0 or r >= rows or c < 0 or c >= cols ->
        nil

      true ->
        j = r * cols + c

        if seat_index?.(j),
          do: j,
          else: find_first_seat(r + dr, c + dc, dr, dc, rows, cols, seat_index?)
    end
  end

  # simulation 

  defp solve(occupied, neighbor_map, tolerance) do
    step(occupied, neighbor_map, tolerance)
    |> case do
      {:fixed, occ} -> map_size(occ)
      {:next, occ} -> solve(occ, neighbor_map, tolerance)
    end
  end

  defp step(occupied, neighbor_map, tolerance) do
    {next_occ, changes} =
      Enum.reduce(neighbor_map, {%{}, 0}, fn {i, ns}, {acc, ch} ->
        occ_neighbors =
          Enum.reduce(ns, 0, fn j, cnt -> cnt + if Map.has_key?(occupied, j), do: 1, else: 0 end)

        is_occupied = Map.has_key?(occupied, i)

        cond do
          is_occupied and occ_neighbors >= tolerance ->
            # becomes empty, so don't put in next_occ
            {acc, ch + 1}

          not is_occupied and occ_neighbors == 0 ->
            # becomes occupied
            {Map.put(acc, i, true), ch + 1}

          true ->
            {if(is_occupied, do: Map.put(acc, i, true), else: acc), ch}
        end
      end)

    if changes == 0, do: {:fixed, occupied}, else: {:next, next_occ}
  end
end

Solution.run()
