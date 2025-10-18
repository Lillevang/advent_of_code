// Run with: ts-node solution.ts [1|2]  (or compile with tsc and run with node)
import * as fs from "fs";

function readInput(): string[] {
  const data = fs.readFileSync("./input", "utf8");
  // Keep empty lines if you prefer: remove the filter(Boolean) below
  return data.split(/\r?\n/);
}

function partOne(lines: string[]): string {
  // TODO: implement
  return `part 1 not implemented (${lines.length} lines)`;
}

function partTwo(lines: string[]): string {
  // TODO: implement
  return `part 2 not implemented (${lines.length} lines)`;
}

function main() {
  const lines = readInput();
  const arg = process.argv[2];
  if (arg === "1") {
    console.log(partOne(lines));
  } else if (arg === "2") {
    console.log(partTwo(lines));
  } else {
    console.log(partOne(lines));
    console.log(partTwo(lines));
  }
}

main();
