# Explanation

Source: /u/pileOfSchist - [Link](https://www.reddit.com/r/adventofcode/comments/k8xw8h/2020_day_08_solutions/gf16m0u/)

```python
print(
# Define recursive lambda function executes a line of the program and calls itself with the next line number, accumulator, and list of visited lines
(execute := lambda program, line, acc, visited:
    # Once a previously-visited line is hit, return the accumulator value
    acc if line in visited else (
        # If the line is a nop, run the next line with the same acc and add this line to visited
        execute(program, line + 1, acc, visited + [line]) if program[line].startswith('nop') else (
            # If the line is an acc operation, run the next line with the operand added to the accumulator
            execute(program, line + 1, acc + int(program[line][4:]), visited + [line]) if program[line].startswith('acc') else (
                # Otherwise the line must be a jmp operation, so run the line given by the current line + the operand.
                execute(program, line + int(program[line][4:]), acc, visited + [line])
            )
        )
    )
 )(open('input.txt').read().splitlines(), 0, 0, []))  # Call execute with the input from the file, and initialize line and acc to 0
```

```python
print(
    list(filter(
        lambda out: out is not None,
        map(
            # Define recursive lambda function executes a line of the program and calls itself with the next line number, accumulator, and list of visited lines
            execute := lambda program, line=0, acc=0, visited=[]:
                # Once a previously-visited line is hit, return the accumulator value
                acc if line >= len(program) else (
                    None if line in visited else (
                        # If the line is a nop, run the next line with the same acc and add this line to visited
                        execute(program, line + 1, acc, visited + [line]) if program[line].startswith('nop') else (
                            # If the line is an acc operation, run the next line with the operand added to the accumulator
                            execute(program, line + 1, acc + int(program[line][4:]), visited + [line]) if program[line].startswith('acc') else (
                                # Otherwise the line must be a jmp operation, so run the line given by the current line + the operand.
                                execute(program, line + int(program[line][4:]), acc, visited + [line])
                            )
                        )
                    )
                ),
            # Define a lambda that takes the input and returns a copy for each line with that line changed from nop to jmp and vice versa
            (lambda in_lines:
                [
                    [  # Replace the idx'th line only
                        new_line.replace('jmp', 'n').replace('nop', 'jmp').replace('n', 'nop') if new_idx == idx else new_line
                        for new_idx, new_line in enumerate(in_lines.copy())
                    ]
                    # Loop through and create a copy of the input for each line
                    for idx, line in enumerate(in_lines)
                ]
             )(open('input.txt').read().splitlines())
        )
    ))[0]
)
```