def read_input
    content = File.read("./input").split("\n")
    tpl = content[0]
    r = content[2..].map { |r| r.split(" -> ") }.transpose
    rules = Hash(String, String).zip(r[0], r[1])
    return tpl, rules
end

def get_pairs_counter(tpl : String)
    pairs = {} of String => Int64
    (0..(tpl.size() - 2)).each { |i|
        s = tpl[i..i+1]
        pairs[s] = 1
    } 
    pairs
end

def get_chars_counter(tpl : String)
    chars = {} of String => Int64
    tpl.each_char do |c|
        s = c.to_s
        if chars.has_key?(s)
            chars[s] += 1
        else
            chars[s] = 1
        end
    end
    chars
end

def update_hash(pairs : Hash(String, Int64), keys : Array(String))
    keys.each { |key|
        if !pairs.has_key?(key)
            pairs[key]  = 0
        end
    }    
end

def solve(steps : Int64, pairs : Hash(String, Int64), chars : Hash(String, Int64), rules : Hash(String, String))
    (0..steps).each { |i|
        pairs.clone.each do | k, v|
            a,b = k
            x = rules[k]
            update_hash(pairs, [a+x.to_s, x+b.to_s])
            update_hash(chars, [x])
            pairs[k] -= v
            pairs[a+x.to_s] += v
            pairs[x+b.to_s] += v
            chars[x] += v
      	end
    }
end

def part_one(tpl : String, rules : Hash(String, String))
    pairs = get_pairs_counter(tpl)
    chars = get_chars_counter(tpl)
    solve(9, pairs, chars, rules)
    chars.values.max - chars.values.min
end

def part_two(tpl : String, rules : Hash(String, String))
    pairs = get_pairs_counter(tpl)
    chars = get_chars_counter(tpl)
    solve(39, pairs, chars, rules)
    chars.values.max - chars.values.min
end

tpl, rules = read_input
p part_one(tpl, rules)
p part_two(tpl, rules)
