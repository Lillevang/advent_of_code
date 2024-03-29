object solution:
  def bruteForce(left : Int, right: Int, bottom: Int, top: Int): Seq[Int] =
    def fire(speedX : Int, speedY: Int): Boolean = Iterator
      .iterate((0, 0, speedX, speedY))((x, y, dx, dy) => (x + dx, y + dy, (dx - 1).max(0), dy - 1))
      .takeWhile((x, y, dx, dy) => ((x < left && dx > 0) || (x >= left && x <= right)) && (y >= bottom))
      .exists((x, y, _, _) => x >= left && x <= right && y >= bottom && y <= top)

    for dx <- 1 to 1000; dy <- -1000 to 1000 if fire(dx, dy) yield (dy * (dy + 1)) - (dy * (dy + 1)) / 2
  end bruteForce

  def part1(input: (Int, Int, Int, Int)): Int = bruteForce.tupled(input).max

  def part2(input: (Int, Int, Int, Int)): Int = bruteForce.tupled(input).size

  def main(args: Array[String]): Unit =
    val data = (155, 215, -132, -72)
    println(part1(data))
    println(part2(data))
