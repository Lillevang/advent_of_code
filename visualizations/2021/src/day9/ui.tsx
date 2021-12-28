import { extent, format, median, scaleBand, scaleLinear, scaleSqrt } from 'd3';
import { createEffect, createMemo, For, onMount, untrack } from 'solid-js';
import { colors } from '../helpers/colors';
import { Vector } from '../helpers/types';
import input from './input.txt?raw';
import { transparentize } from 'polished';
import {
  chunk,
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
import './ui.css';
import { Index } from 'solid-js/web';
import { scaledDist } from '../helpers/dist';

export function Day9Viz() {
  const grid = input
    .trim()
    .split('\n')
    .map((line) => line.trim().split('').map(Number));

  const colorScale = scaleLinear([0, 9], [colors.darkBlue, colors.pink]);

  return (
    <svg
      viewBox="-5 -5 110 110"
      style={{
        'max-width': '100%',
        'max-height': '100%',
      }}
    >
      <Index each={grid}>
        {(row, y) => (
          <Index each={grid[y]}>
            {(cell, x) => (
              <rect
                x={x}
                y={y}
                width="1"
                height="1"
                stroke={colorScale(cell())}
                fill={colorScale(cell())}
              />
            )}
          </Index>
        )}
      </Index>
    </svg>
  );
}
