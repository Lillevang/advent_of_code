# TODO translate Ruby below into Crystal
p read.split("\n\n").map{|x|x.split.join.chars.uniq.size}.sum
p read.split("\n\n").map{|x|x.lines.map{|x|x.chomp.chars}.reduce(:&).size}.sum