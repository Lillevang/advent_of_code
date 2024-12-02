defmodule Solution do
  @input File.read!("input")
  @digit_words ~w[one two three four five six seven eight nine]

  def part1(input \\ @input),
    do:
      input
      |> String.split()

  def part2(input \\ @input),
    do:
      input

end



IO.puts(Solution.part1())

#IO.puts(Solution.part2())
