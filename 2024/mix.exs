defmodule AOC2024.MixProject do
 use Mix.Project

 def project do
  [
   app: :aoc_2024,
   version: "0.1.0",
   elixir: "~> 1.17",
   start_permanent: Mix.env() == :prod,
   deps: deps()
   elixirc_paths: elixirc_paths(Mix.env())
  ]
  end

  defp elixirc_paths(:test), do: ["lib", "test"]
  defp elixirc_paths(_), do: elixir_solution_paths()

  defp elixir_solution_paths do
   days = 1..25
   |> Enum.map(&Integer.to_string/1)
   |> Enum.map(&Path.join(&1))

   days
   |> Enum.filter(&File.dir?/1)
   |> Enum.filter(fn dir ->
    dir
    |> File.ls!()
    |> Enum.any?(&String.ends_with?(&1, ".ex"))
   end)
end

defp application do
 [
  extra_applications: [:logger]
 ]
end

defp deps do
 [
  
 ]
 end
end
