require "digest"

input_data = File.read("./input").strip

def find_md5_hash(input : String, prefix : String)
    i = 1
    md5_hash_found = false
    while(!md5_hash_found)
        md5_hash_found = Digest::MD5.hexdigest("#{input}#{i}").starts_with?(prefix) ? true : false
        i = i + 1 unless md5_hash_found
    end
    i
end

# Part 1
p find_md5_hash(input_data, "00000")

# Part 2
p find_md5_hash(input_data, "000000")
