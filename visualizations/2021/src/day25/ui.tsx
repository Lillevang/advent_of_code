import { extent, format, median, scaleBand, scaleLinear, scaleSqrt } from 'd3';
import {
  createEffect,
  createMemo,
  For,
  onMount,
  untrack,
  Show,
  on,
  createSignal,
  Accessor,
  batch,
} from 'solid-js';
import { colors } from '../helpers/colors';
import { Vector } from '../helpers/types';
import input from './input.txt?raw';
import { transparentize } from 'polished';
import {
  chunk,
  differenceBy,
  floor,
  max,
  random,
  range,
  round,
  shuffle,
  sortBy,
  sum,
  sumBy,
} from 'lodash';
import { now } from '../helpers/timers';
import { createMutable } from 'solid-js/store';
import { Index } from 'solid-js/web';
import { scaledDist } from '../helpers/dist';

export function Day25Viz() {
  function* animationSteps() {
    let moved = new Set<Cucumber>();
    yield;
    yield;
    do {
      moved.clear();

      for (const c of horizontal) c.canMove() && moved.add(c);
      for (const c of moved) c.move();

      yield;

      for (const c of vertical) c.canMove() && moved.add(c);
      for (const c of moved) !c.isHorizontal() && c.move();

      yield;
    } while (moved.size > 0);
  }

  const tickLength = 16 * 50;
  const tick = createMemo(() => round(now() / tickLength));

  const steps = animationSteps();

  createEffect(
    on(tick, () => {
      batch(() => {
        steps.next();
      });
    })
  );

  const colorByCucumber = {
    '>': colors.pink,
    v: colors.blue,
  };

  return (
    <svg
      viewBox="-10 -10 160 160"
      style={{
        'max-width': '100%',
        'max-height': '100%',
      }}
    >
      <For each={cucumbers}>
        {(c) => (
          <circle
            cx={c.getPos()[0]}
            cy={c.getPos()[1]}
            r="0.4"
            fill={colorByCucumber[c.toString()]}
          />
        )}
      </For>
    </svg>
  );
}

let lines = input
  .trim()
  .split('\n')
  .map((line) => line.split(''));
let grid: (Cucumber | null)[][] = [];
class Cucumber {
  getPos: Accessor<[number, number]>;
  private setPos: (newPos: [number, number]) => void;

  constructor(public pos: [number, number], private dir: [number, number]) {
    const signal = createSignal(pos);
    this.getPos = signal[0];
    this.setPos = signal[1];
  }

  nextPos(): [number, number] {
    const x = (this.pos[0] + this.dir[0]) % grid[0].length;
    const y = (this.pos[1] + this.dir[1]) % grid.length;
    return [x, y];
  }

  canMove() {
    const [x, y] = this.nextPos();
    return !grid[y][x];
  }

  move() {
    const [x, y] = this.nextPos();
    grid[y][x] = this;
    grid[this.pos[1]][this.pos[0]] = null;
    this.pos[0] = x;
    this.pos[1] = y;
    this.setPos([x, y]);
  }

  isHorizontal() {
    return this.dir[0] === 1;
  }

  toString() {
    if (this.isHorizontal()) return '>';
    return 'v';
  }
}

lines.map((line, y) =>
  line.forEach((cell, x) => {
    if (!grid[y]) grid[y] = [];
    if (cell === '.') grid[y][x] = null;
    if (cell === '>') grid[y][x] = new Cucumber([x, y], [1, 0]);
    if (cell === 'v') grid[y][x] = new Cucumber([x, y], [0, 1]);
  })
);
const cucumbers = grid.flat().filter((x): x is Cucumber => !!x);
const horizontal = cucumbers.filter((c) => c.isHorizontal());
const vertical = cucumbers.filter((c) => !c.isHorizontal());
