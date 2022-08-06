import { scaleLinear } from 'd3';
import {
  batch,
  createEffect,
  createMemo,
  createSignal,
  on,
  onMount,
} from 'solid-js';
import { colors } from '../helpers/colors';
import { random } from 'lodash';
import { now } from '../helpers/timers';
import { createMutable, Store } from 'solid-js/store';
import './ui.css';
import { Index } from 'solid-js/web';

export function Day11Viz() {
  let largeGrid: number[][] = [];

  for (let x = 0; x < 50; x++) {
    for (let y = 0; y < 50; y++) {
      if (!largeGrid[y]) largeGrid[y] = [];
      largeGrid[y][x] = random(0, 9);
    }
  }

  const inputString = largeGrid.map((row) => row.join('')).join('\n');

  const tickLength = 100;
  const data = createMutable({
    grid: inputString
      .trim()
      .split('\n')
      .map((line) => line.trim().split('').map(Number)),
    step: 0,
    flashes: 0,
  });

  const iterator = steps(data);

  const tick = createMemo(() => Math.floor(now() / tickLength));

  createEffect(
    on(tick, () => {
      batch(() => {
        iterator.next();
      });
    })
  );

  const colorScale = scaleLinear([0, 9], [colors.pink, colors.darkBlue]).clamp(
    true
  );
  return (
    <svg
      viewBox={`-1 -1 ${data.grid.length + 2} ${data.grid.length + 2}`}
      style={{
        'max-width': '100%',
        'max-height': '100%',
        overflow: 'visible',
      }}
    >
      <text
        font-size={5 * (data.grid.length / 100) + ''}
        x={101 * (data.grid.length / 100) + ''}
        y={45 * (data.grid.length / 100) + ''}
        fill="white"
        font-family="Klavika"
        alignment-baseline="middle"
      >
        Step {data.step}
      </text>
      <text
        font-size={5 * (data.grid.length / 100) + ''}
        x={101 * (data.grid.length / 100) + ''}
        y={55 * (data.grid.length / 100) + ''}
        fill="white"
        font-family="Klavika"
        alignment-baseline="middle"
      >
        Flashes: {data.flashes}
      </text>
      <Index each={data.grid}>
        {(row, y) => (
          <Index each={data.grid[y]}>
            {(cell, x) => (
              <circle
                style={{
                  transition: 'all 1s',
                  'transition-duration': tickLength + 'ms',
                }}
                cx={x + 0.5}
                cy={y + 0.5}
                r="0.3"
                stroke="none"
                fill={colorScale(cell())}
              />
            )}
          </Index>
        )}
      </Index>
    </svg>
  );
}

function* steps(
  store: Store<{
    grid: number[][];
    step: number;
    flashes: number;
  }>
) {
  while (true) {
    store.step++;
    for (let y = 0; y < store.grid.length; y++) {
      for (let x = 0; x < store.grid[0].length; x++) {
        store.grid[y][x]++;
      }
    }

    yield;

    let flashed = true;
    while (flashed) {
      flashed = false;
      for (let y = 0; y < store.grid.length; y++) {
        for (let x = 0; x < store.grid[0].length; x++) {
          if (store.grid[y][x] > 9) {
            store.grid[y][x] = -10000;
            store.flashes++;
            flashed = true;

            for (let dx = -1; dx <= 1; dx++) {
              for (let dy = -1; dy <= 1; dy++) {
                if (dx === 0 && dy === 0) continue;
                const neighbour = store.grid[y + dy]?.[x + dx];
                if (neighbour === undefined) continue;
                store.grid[y + dy][x + dx]++;
              }
            }
          }
        }
      }
    }
    yield;

    for (let y = 0; y < store.grid.length; y++) {
      for (let x = 0; x < store.grid[0].length; x++) {
        if (store.grid[y][x] < 0) store.grid[y][x] = 0;
      }
    }
  }
}
