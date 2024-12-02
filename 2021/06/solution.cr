def fish_after(number_of_days)
    starting_state = File.read("./input").split(",").map{ |x| x.to_i }
    state = (0..8).map { |days| starting_state.count(days).to_i64 || 0.to_i64 }
    number_of_days.times do 
      state.rotate!
      state[6] += state.last
    end
  
    state.sum
end

p fish_after(80)
p fish_after(256)