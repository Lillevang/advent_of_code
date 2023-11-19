
LINES = File.read("./input").strip().split("\n")

GRAPH = LINES.map(&.chars)
ROW_LENGTH = GRAPH.size
COL_LENGTH = GRAPH[0].size
EDGES = Array.new(ROW_LENGTH) { Array.new(COL_LENGTH, 0)  }

DIRS = [{-1,0},{0,1},{1,0},{0,-1}]
(0...ROW_LENGTH).each do |r|
  (0...COL_LENGTH).each do |c|
    if GRAPH[r][c] == 'S'
      EDGES[r][c] = 1
    else
      EDGES[r][c] = GRAPH[r][c].ord - 'a'.ord + 1
    end
  end
end

def bfs(part)
  q = Deque(Tuple(Tuple(Int32, Int32), Int32)).new
  (0...ROW_LENGTH).each do |r|
    (0...COL_LENGTH).each do |c|
      if (part == 1 && GRAPH[r][c] == 'S') || (part == 2 && EDGES [r][c] == 1)
        t = {r,c}
        q << {t, 0}
      end
    end
  end

  s = Set(Tuple(Int32, Int32)).new

  while !q.empty?
    x, d = q.shift
    next if s.includes?(x)
    s << x
    r, c = x
    if GRAPH[r][c] == 'E'
      return d
    end
    DIRS.each do |dr, dc|
      rr = r + dr
      cc = c + dc
      if (0 <= rr < ROW_LENGTH) && (0 <= cc < COL_LENGTH) && (EDGES[rr][cc] <= 1 + EDGES[r][c])
        t = {rr, cc}
        q << {t, d + 1}
      end
    end
  end
end

puts bfs(1)
puts bfs(2)
