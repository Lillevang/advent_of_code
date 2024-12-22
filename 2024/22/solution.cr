def mix(x, y)
  x ^ y
end

def prune(x)
  x % 16777216
end

def prices(x : Int64) : Array(Int64)
  answers = [x]
  (0...2000).each do |i|
    x = prune(mix(x, 64 * x))
    x = prune(mix(x, x // 32))
    x = prune(mix(x, x * 2048))
    answers << x
  end
  answers
end

def changes(prices : Array(Int64))
  output = Array(Int64).new
  (0...prices.size-1).each do |i|
    output << prices[i+1]-prices[i]
  end
  output
end

def get_scores(prices : Array(Int64), changes : Array(Int64)) : Hash(Tuple(Int64,Int64,Int64,Int64), Int64)
  output = Hash(Tuple(Int64,Int64,Int64,Int64), Int64).new
  (0...changes.size-3).each do |i|
    pattern = {changes[i], changes[i+1], changes[i+2], changes[i+3]}
    unless output.has_key?(pattern)
      output[pattern] = prices[i+4]
    end
  end
  output
end

DATA = File.read_lines("input")
p1 = 0.to_i64
SCORE = Hash(Tuple(Int64,Int64,Int64,Int64), Int64).new

DATA.each do |line|
  p = prices(line.to_i64)
  p1 += p.last
  prices = p.map { |x| x % 10 }
  c = changes(prices)
  s = get_scores(prices, c)
  s.each do |k, v|
    if !SCORE.has_key?(k)
      SCORE[k] = v
    else
      SCORE[k] += v
    end
  end
end

puts p1
puts SCORE.values.max
