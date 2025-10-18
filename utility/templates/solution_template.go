package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
)

func readInput() []string {
	f, err := os.Open("input")
	if err != nil {
		log.Fatalf("open input: %v", err)
	}
	defer f.Close()

	var lines []string
	sc := bufio.NewScanner(f)
	for sc.Scan() {
		lines = append(lines, sc.Text())
	}
	if err := sc.Err(); err != nil {
		log.Fatalf("scan input: %v", err)
	}
	return lines
}

func partOne(lines []string) string {
	// TODO: implement
	return fmt.Sprintf("part 1 not implemented (%d lines)", len(lines))
}

func partTwo(lines []string) string {
	// TODO: implement
	return fmt.Sprintf("part 2 not implemented (%d lines)", len(lines))
}

func main() {
	lines := readInput()
	if len(os.Args) > 1 {
		if os.Args[1] == "1" {
			fmt.Println(partOne(lines))
			return
		}
		if os.Args[1] == "2" {
			fmt.Println(partTwo(lines))
			return
		}
	}
	fmt.Println(partOne(lines))
	fmt.Println(partTwo(lines))
}
