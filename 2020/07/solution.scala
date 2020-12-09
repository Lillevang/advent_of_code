// Inspiration from: https://github.com/bbstilson/adventofcode/blob/main/adventofcode/src/bbstilson/aoc2020/Day7.scala
import scala.io.Source

object solution {
    val RootRegex = raw"(.+) bags contain (.+)".r
    val ContainsRegex = raw"(\d+) ([a-z ]+) bags?".r
    val SHINY = "shiny gold"

    def run(input: List[String]): Unit = {
        implicit val rules: Map[String, Map[String, Int]] = input.map { case RootRegex(root, rest) => 
            root -> ContainsRegex
                .findAllMatchIn(rest)
                .toList
                .flatMap(_.subgroups)
                .sliding(2,2)
                .collect { case List(number, color) => color -> number.toInt}
                .toMap
            }.toMap

            println(rules.keys.filter(holdsShiny).size)
            println(sumBagCount(SHINY))
    }

    def holdsShiny(color: String)(implicit rules: Map[String, Map[String, Int]]): Boolean = {
        val ruleMap = rules(color)
        ruleMap.contains(SHINY) || ruleMap.keys.find(holdsShiny).nonEmpty
    }

    def sumBagCount(color: String)(implicit rules: Map[String, Map[String, Int]]): Int = {
        rules(color).map { case (c, n) =>
            n + List.fill(n)(sumBagCount(c)).sum
        }.sum
    }
    
    def main(args: Array[String]) = {
        val lines = Source.fromFile("input").getLines.toList
        solution.run(lines)
    }
}
