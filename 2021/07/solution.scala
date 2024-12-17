import scala.io.Source

object solution {

    def parseData(filename: String): Array[Int] = {
        val bufferedSource = Source.fromFile(filename)
        val numbers = bufferedSource.getLines().next()
        bufferedSource.close
        numbers.split(",").map(_.trim.toInt)
    }

    object PartOne {
        def optimizeForFuel(positions: Array[Int]) : Int = {
            val median = positions.sorted.apply(positions.length / 2)
            positions.foldLeft(0)((acc, cur) => acc + Math.abs(cur - median))
        }
    }

    object PartTwo {

        def naturalSum(n: Int): Int = {
            (n to 0 by -1).sum
        }

        def optimizeForFuel(positions: Array[Int]) : Int = {
            val avg = Math.floor(positions.sum.toDouble / positions.length.toDouble).toInt
            positions.foldLeft(0)((acc, cur) => {acc + naturalSum(Math.abs(cur - avg))})
        }
    }

    def main(args: Array[String]): Unit = {
        val data = parseData("./input")
        println(PartOne.optimizeForFuel(data))
        println(PartTwo.optimizeForFuel(data))
    }
}
