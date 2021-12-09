def fish_after(number_of_days)
    starting_state = File.read("./input").split(",").map{ |x| x.to_i }
    fish_at_each_stage = (0..8).map { |days| starting_state.count(days).to_i64 || 0.to_i64 }
    number_of_days.times do 
      fish_at_each_stage.rotate!
      fish_at_each_stage[6] += fish_at_each_stage.last
    end
  
    fish_at_each_stage.sum
end

p fish_after(80)
p fish_after(256)