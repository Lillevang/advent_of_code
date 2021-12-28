import { extent, line, scaleLinear } from 'd3';
import { createMemo } from 'solid-js';
import { now } from '../helpers/timers';
import input from './input.txt?raw';

export function Day2Viz() {
  const width = 200;
  const height = 200;
  const x = scaleLinear()
    .domain(extent(data, (d) => d.x) as [number, number])
    .range([0, width]);
  const y = scaleLinear()
    .domain(extent(data, (d) => d.y) as [number, number])
    .range([0, height]);
  const frame = createMemo(() => Math.floor(now() / 10));

  const dataToRender = createMemo(() => data.slice(0, frame() % data.length));
  const lineGenerator = line<Point>()
    .x((d) => x(d.x))
    .y((d) => y(d.y));

  const path = createMemo(() => lineGenerator(dataToRender()));

  return (
    <svg width={width} height={height}>
      <path stroke="black" d={path()!} fill="none" />
    </svg>
  );
}

const data: Point[] = [];
let aim = 0;
let x = 0;
let y = 0;
for (const line of input.split(`\n`).filter((x) => x.length > 0)) {
  const [command, amount] = line.split(' ');
  if (command === 'forward') {
    x += +amount;
    y += aim * +amount;
  }
  if (command === 'down') aim += +amount;
  if (command === 'up') aim -= +amount;
  data.push({ x, y, aim });
}
type Point = { x: number; y: number; aim: number };
