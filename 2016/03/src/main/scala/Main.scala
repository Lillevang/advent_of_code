import scala.io.Source

val inputPath = "./input"
val lines = Source.fromFile(inputPath).getLines.toList


def isValidTriangle(v: Array[Int]) : Boolean =
    v(0) + v(1) > v(2) && v(0) + v(2) > v(1) && v(1) + v(2) > v(0)

def partOne: Int =
    return lines
            .map(line => line.trim.split("\\s+").map(_ .toInt))
            .count(isValidTriangle)

def partTwo: Int =
    return lines
            .map(line => line.trim.split("\\s+").map(_ .toInt))
            .grouped(3).map(_ .transpose).flatten
            .count(v => isValidTriangle(v.toArray))


@main def solution: Unit =
    println(partOne)
    println(partTwo)
