# Count lines:
lines=$(wc -l input | sed 's/[^0-9]//g')
# 300, meaning 600 quotes

# Count total characters:
char_count=$(wc -c input | sed 's/[^0-9]//g') 
# 6789

# Count characters after un-escaping:
unescaped_chars_count=$(sed 's/\\"/@/g' input | sed 's/\\x[a-f0-9][a-f0-9]/~/g' | sed 's/\\\\/\\/g' | wc -c)
tmp=$(expr $char_count - $unescaped_chars_count)
double_lines=$(expr $lines + $lines)
total=$(expr $tmp + $double_lines)

# Solution: 
echo PART ONE SOLUTION:
echo "$char_count - $unescaped_chars_count = $tmp"
echo "$tmp + $lines * 2 = $total"
echo
echo PART TWO SOLUTION
encoded=$(sed 's/"/~~/g' input | sed 's/\\/@@/g' | wc -c)
tmp=$(expr $encoded + $double_lines)
result=$(expr $tmp - $char_count)
echo "$result"