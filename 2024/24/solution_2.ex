defmodule Wire do
  defstruct name: ""
end

defmodule Gate do
  defstruct inputs: [], output: %Wire{}, op: ""
end

defmodule AOC2024.Day24 do
  def run do
    # Read all lines from "input" file
    lines = File.read!("./input")
            |> String.split("\n", trim: true)

    # Parse all wires and gates
    {wires, gates} =
      Enum.reduce(lines, {%{}, []}, fn line, {acc_wires, acc_gates} ->
        if String.contains?(line, "->") do
          elements = String.split(line, " ")
          # elements[0] => first wire, elements[2] => second wire, elements[4] => output wire
          # elements[1] => gate operation

          acc_wires = add_wire(acc_wires, Enum.at(elements, 0))
          acc_wires = add_wire(acc_wires, Enum.at(elements, 2))
          acc_wires = add_wire(acc_wires, Enum.at(elements, 4))

          new_gate = %Gate{
            inputs: [
              acc_wires[Enum.at(elements, 0)],
              acc_wires[Enum.at(elements, 2)]
            ],
            output: acc_wires[Enum.at(elements, 4)],
            op: Enum.at(elements, 1)
          }

          {acc_wires, [new_gate | acc_gates]}
        else
          {acc_wires, acc_gates}
        end
      end)

    # Identify wires that start with 'z'
    output_wires =
      wires
      |> Map.values()
      |> Enum.filter(fn wire -> String.starts_with?(wire.name, "z") end)

    # Check suspicious gates
    suspicious_gates =
      gates
      |> Enum.reduce([], fn gate, suspicious ->
        # Condition 1
        suspicious =
          if condition_one?(gate, gates) do
            [gate | suspicious]
          else
            suspicious
          end

        # Condition 2
        suspicious =
          if condition_two?(gate) do
            [gate | suspicious]
          else
            suspicious
          end

        # Condition 3
        suspicious =
          if condition_three?(gate, output_wires) do
            [gate | suspicious]
          else
            suspicious
          end

        suspicious
      end)

    # Sort suspicious gates by their output wire name and build the final string
    answer =
      suspicious_gates
      |> Enum.uniq()                 # remove duplicates if condition_one & two, etc. triggered more than once
      |> Enum.sort_by(& &1.output.name)
      |> Enum.map(& &1.output.name)
      |> Enum.join(",")

    IO.puts(answer)
  end

  # Create a wire struct only if it doesn't already exist
  defp add_wire(wires, wire_name) do
    Map.put_new(wires, wire_name, %Wire{name: wire_name})
  end

  defp condition_one?(gate, all_gates) do
    if (starts_with_any?(gate.inputs, "x") and
        starts_with_any?(gate.inputs, "y") and
        not contains_any?(gate.inputs, "00")) do

      # Now see if there's a second gate that takes gate.output as input
      Enum.any?(all_gates, fn second_gate ->
        gate.output in second_gate.inputs and
          (
            (gate.op == "AND" and second_gate.op == "AND") or
            (gate.op == "XOR" and second_gate.op == "OR")
          )
      end)
    else
      false
    end
  end

  defp condition_two?(gate) do
    # gates in the middle should not have XOR
    # if (!input starts with x/y && !output starts with z && op == "XOR")
    (not starts_with_any?(gate.inputs, "x") and
     not starts_with_any?(gate.inputs, "y") and
     !String.starts_with?(gate.output.name, "z") and
     gate.op == "XOR")
  end

  defp condition_three?(gate, output_wires) do
    # gates at the end should always have XOR operators,
    # except for the very last gate
    if (gate.output in output_wires and
       gate.output.name != "z#{length(output_wires) - 1}" and
       gate.op != "XOR") do
      true
    else
      false
    end
  end

  # Helper: check if any input wire name starts with a given prefix
  defp starts_with_any?(inputs, prefix) do
    Enum.any?(inputs, fn wire -> String.starts_with?(wire.name, prefix) end)
  end

  # Helper: check if any input wire name contains a given substring
  defp contains_any?(inputs, substring) do
    Enum.any?(inputs, fn wire -> String.contains?(wire.name, substring) end)
  end
end

AOC2024.Day24.run()
