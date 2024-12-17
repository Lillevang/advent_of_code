package main

import (
	"fmt"
	"os"
	"strings"
)

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: go run main.go <input_file>")
		return
	}

	// path := "input_sample"
	path := "input"

	data, err := os.ReadFile(path)
	if err != nil {
		fmt.Printf("Error reading file: %v\n", err)
		return
	}

	input := strings.TrimSpace(string(data))
	matrix, start := parseInput(input)
	fmt.Println(part1(matrix, start))
	fmt.Println(part2(matrix, start))
}

// vec represents a 2D vector.
type vec [2]int

// add adds two vectors and returns the result.
func (u vec) add(v vec) vec {
	return vec{u[0] + v[0], u[1] + v[1]}
}

// rotate rotates the vector 90 degrees clockwise, `n` times.
func (u vec) rotate(n int) vec {
	x, y := u[0], u[1]
	for i := 0; i < n%4; i++ {
		x, y = -y, x
	}
	return vec{x, y}
}

// state represents the current position and direction.
type state struct {
	pos vec
	dir vec
}

// part1 calculates the length of the path for the first task.
func part1(matrix [][]byte, start vec) int {
	_, path := findLoop(matrix, start, vec{-1, -1})
	return len(path)
}

// part2 calculates the number of loops for the second task.
func part2(matrix [][]byte, start vec) int {
	_, originalPath := findLoop(matrix, start, vec{-1, -1})
	loopChannel := make(chan bool)

	for position := range originalPath {
		if position == start {
			continue
		}
		go func(obstruction vec) {
			foundLoop, _ := findLoop(matrix, start, obstruction)
			loopChannel <- foundLoop
		}(position)
	}

	loopCount := 0
	for i := 0; i < len(originalPath)-1; i++ {
		if <-loopChannel {
			loopCount++
		}
	}

	return loopCount
}

// parseInput parses the input string into a matrix and determines the start position.
func parseInput(input string) ([][]byte, vec) {
	matrix := readMatrix(input, func(b byte) byte { return b })

	var start vec
	rows, cols := len(matrix), len(matrix[0])

	for r := 0; r < rows; r++ {
		for c := 0; c < cols; c++ {
			if matrix[r][c] == '^' {
				start = vec{r, c}
				break
			}
		}
	}

	return matrix, start
}

// findLoop checks for loops in the matrix starting from the given position and direction.
func findLoop(matrix [][]byte, start, obstruction vec) (bool, map[vec]bool) {
	visitedPoints := make(map[vec]bool)
	visitedStates := make(map[state]bool)

	current := start
	direction := vec{-1, 0}

	for {
		currentState := state{current, direction}

		// Check if we revisit the same state
		if visitedStates[currentState] {
			return true, nil
		}

		visitedPoints[current] = true
		visitedStates[currentState] = true

		next := current.add(direction)
		row, col := next[0], next[1]

		// Check boundaries
		if row < 0 || row >= len(matrix) || col < 0 || col >= len(matrix[0]) {
			return false, visitedPoints
		}

		// Handle obstacles and redirection
		if matrix[row][col] == '#' || next == obstruction {
			direction = direction.rotate(3)
		} else {
			current = next
		}
	}
}

// readMatrix reads a string representation of a matrix and applies a transformation to each byte.
func readMatrix[T any](s string, transform func(byte) T) [][]T {
	rows := strings.Split(s, "\n")
	matrix := make([][]T, len(rows))

	for i, row := range rows {
		matrix[i] = make([]T, len(row))
		for j := range row {
			matrix[i][j] = transform(row[j])
		}
	}
	return matrix
}
