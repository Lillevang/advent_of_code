import { extent } from 'd3';
import { For } from 'solid-js';
import { colors } from '../helpers/colors';
import { Vector } from '../helpers/types';
import input from './input.txt?raw';
import { transparentize } from 'polished';

import './ui.css';
import { chunk, random, shuffle } from 'lodash';
import { now } from '../helpers/timers';

export function Day5Viz() {
  const allNums = data.flat(2);
  const padding = 50;
  const [totalMin, totalMax] = extent(allNums);
  const viewBow = [
    totalMin! - padding,
    totalMin! - padding,
    totalMax! + 2 * padding,
    totalMax! + 2 * padding,
  ].join(' ');

  const d = () => data.slice(0, now() / 50);

  return (
    <svg
      viewBox={viewBow}
      style={{
        'max-width': '100%',
        'max-height': '100%',
      }}
    >
      <For each={d()}>
        {([[x1, y1], [x2, y2]]) => (
          <line
            {...{ x1, x2, y1, y2 }}
            stroke={transparentize(0.25, colors.pink)}
          />
        )}
      </For>
    </svg>
  );
}

function parseInstruction(s: string): [Vector, Vector] {
  const match = s.match(/(\d+),(\d+) -> (\d+),(\d+)/);
  if (!match) throw new Error(`Input ${s} does not match d,d -> d,d`);
  const [, x1, y1, x2, y2] = match.map(Number);
  return [
    [x1, y1],
    [x2, y2],
  ];
}

const charMap: { [key: string]: { to: Vector; from?: Vector }[] } = {
  A: [
    { from: [0, 0], to: [0, 3] },
    { to: [1, 4] },
    { to: [2, 4] },
    { to: [2, 0] },
    { from: [0, 2], to: [2, 2] },
  ],
  B: [
    { from: [0, 0], to: [0, 4] },
    { to: [1, 4] },
    { to: [2, 3] },
    { to: [1, 2] },
    { to: [0, 2] },
    { from: [1, 2], to: [2, 1] },
    { to: [1, 0] },
    { to: [0, 0] },
  ],
  C: [
    { from: [2, 3], to: [1, 4] },
    { to: [0, 3] },
    { to: [0, 2] },
    { to: [0, 1] },
    { to: [1, 0] },
    { to: [2, 1] },
  ],
  D: [
    { from: [0, 0], to: [0, 4] },
    { to: [1, 4] },
    { to: [2, 3] },
    { to: [2, 1] },
    { to: [1, 0] },
    { to: [0, 0] },
  ],
  E: [
    { from: [0, 0], to: [0, 4] },
    { from: [0, 4], to: [2, 4] },
    { from: [0, 2], to: [1, 2] },
    { from: [0, 0], to: [2, 0] },
  ],
  F: [
    { from: [0, 0], to: [0, 4] },
    { from: [0, 4], to: [2, 4] },
    { from: [0, 2], to: [1, 2] },
  ],
  G: [
    { from: [2, 3], to: [1, 4] },
    { to: [0, 3] },
    { to: [0, 2] },
    { to: [0, 1] },
    { to: [1, 0] },
    { to: [2, 1] },
    { to: [2, 2] },
    { to: [1, 2] },
    { to: [0, 1] },
  ],
  H: [
    { from: [0, 0], to: [0, 4] },
    { from: [0, 2], to: [2, 2] },
    { from: [2, 0], to: [2, 4] },
  ],
  I: [{ from: [1, 0], to: [1, 4] }],
  J: [{ from: [2, 4], to: [2, 1] }, { to: [1, 0] }, { to: [0, 1] }],
  K: [
    { from: [0, 0], to: [0, 4] },
    { from: [2, 4], to: [0, 2] },
    { to: [2, 0] },
  ],
  L: [
    { from: [0, 0], to: [0, 4] },
    { from: [0, 0], to: [2, 0] },
  ],
  M: [
    { from: [0, 0], to: [0, 4] },
    { to: [1, 3] },
    { to: [2, 4] },
    { to: [2, 0] },
  ],
  N: [
    { from: [0, 0], to: [0, 4] },
    { to: [1, 3] },
    { to: [1, 1] },
    { to: [2, 0] },
    { to: [2, 4] },
  ],
  O: [
    { from: [2, 3], to: [1, 4] },
    { to: [0, 3] },
    { to: [0, 2] },
    { to: [0, 1] },
    { to: [1, 0] },
    { to: [2, 1] },
    { to: [2, 3] },
  ],
  P: [
    { from: [0, 0], to: [0, 4] },
    { to: [1, 4] },
    { to: [2, 3] },
    { to: [1, 2] },
    { to: [0, 2] },
  ],
  Q: [
    { from: [2, 3], to: [1, 4] },
    { to: [0, 3] },
    { to: [0, 2] },
    { to: [0, 1] },
    { to: [1, 0] },
    { to: [2, 1] },
    { to: [2, 3] },
    { from: [1, 1], to: [2, 0] },
  ],
  R: [
    { from: [0, 0], to: [0, 4] },
    { to: [1, 4] },
    { to: [2, 3] },
    { to: [1, 2] },
    { to: [0, 2] },
    { to: [2, 0] },
  ],
  S: [
    { from: [0, 4], to: [1, 4] },
    { to: [2, 3] },
    { to: [2, 2] },
    { to: [0, 2] },
    { to: [0, 1] },
    { to: [1, 0] },
    { to: [2, 0] },
  ],
  T: [
    { from: [1, 0], to: [1, 4] },
    { from: [0, 4], to: [2, 4] },
  ],
  U: [{ from: [0, 4], to: [0, 0] }, { to: [2, 0] }, { to: [2, 4] }],
  V: [
    { from: [0, 4], to: [0, 2] },
    { to: [0, 1] },
    { to: [1, 0] },
    { to: [2, 1] },
    { to: [2, 4] },
  ],
  W: [
    { from: [0, 4], to: [0, 0] },
    { to: [1, 0] },
    { to: [1, 2] },
    { to: [1, 0] },
    { to: [2, 0] },
    { to: [2, 4] },
  ],
  X: [
    { from: [0, 0], to: [0, 1] },
    { to: [2, 3] },
    { to: [2, 4] },
    { from: [0, 4], to: [0, 3] },
    { to: [2, 1] },
    { to: [2, 0] },
  ],
  Y: [
    { from: [1, 0], to: [1, 2] },
    { from: [0, 4], to: [0, 3] },
    { to: [1, 2] },
    { to: [2, 3] },
    { to: [2, 4] },
  ],
  Z: [
    { from: [0, 4], to: [2, 4] },
    { to: [2, 3] },
    { to: [0, 1] },
    { to: [0, 0] },
    { to: [2, 0] },
  ],
  ',': [{ from: [0, 0.5], to: [0, -0.5] }],
  '.': [{ from: [-0.2, 0], to: [0.2, 0] }],
  '!': [
    { from: [1, 4], to: [1, 1.5] },
    { from: [1, 0.5], to: [1, 0] },
  ],
  ' ': [],
};

const xPadding = 20;
const yPadding = 20;
const squareSize = 50;
const charHeight = 5;
const charWidth = 3;
const randomLinesPerLine = 8;
const randomLineCountDeviation = 2;
const randomLineXDeviation = 15;
const randomLineYDeviation = 20;

function toInstruction(text: string) {
  let instructions: string[] = [];

  const vectorToTargetVector = (
    v: Vector,
    charIndex: number,
    lineIndex: number
  ): Vector => [
    v[0] * squareSize +
      charIndex * (squareSize * 1.5) * (charWidth - 1) +
      xPadding,
    (charHeight - v[1] - 1) * squareSize +
      lineIndex * charHeight * squareSize +
      yPadding,
  ];
  const lines = text.split('\n');

  lines.forEach((line, lineIndex) =>
    [...line].forEach((char, charIndex) => {
      const path = charMap[char].map((x, i, segments) => ({
        to: vectorToTargetVector(x.to, charIndex, lineIndex),
        from: vectorToTargetVector(
          x.from ?? segments[i - 1].to,
          charIndex,
          lineIndex
        ),
      }));
      for (const { to, from } of path) {
        instructions.push(`${from[0]},${from[1]} -> ${to[0]},${to[1]}`);

        const lineCount = random(
          randomLinesPerLine - randomLineCountDeviation,
          randomLinesPerLine + randomLineCountDeviation
        );
        for (let i = 0; i < lineCount; i++) {
          const dx = random(-1 * randomLineXDeviation, randomLineXDeviation);
          const dy = random(-1 * randomLineYDeviation, randomLineYDeviation);
          instructions.push(
            `${from[0] + dx},${from[1] + dy} -> ${to[0] + dx},${to[1] + dy}`
          );
        }
      }

      charIndex++;
    })
  );

  return shuffle(instructions);
}

const testInput = toInstruction(
  `THE SQUID
 CHEATED
AT BINGO!`.toUpperCase()
).join('\n');
console.log(testInput);
const data = input
  .trim()
  .split('\n')
  .map((line) => parseInstruction(line));
