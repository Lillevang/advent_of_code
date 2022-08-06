import { extent, format, scaleBand, scaleLinear } from 'd3';
import { createEffect, createMemo, For, untrack } from 'solid-js';
import { colors } from '../helpers/colors';
import { Vector } from '../helpers/types';
import input from './input.txt?raw';
import { transparentize } from 'polished';
import { chunk, max, random, range, round, shuffle, sum } from 'lodash';
import { now } from '../helpers/timers';
import { createMutable } from 'solid-js/store';
import './ui.css';
import { Index } from 'solid-js/web';

export function Day6Viz() {
  const animationDuration = 500;
  const height = 100;
  const width = 100;

  const store = createMutable({ fishes: [] as number[], generation: 0 });
  for (let i = 0; i <= 8; i++) store.fishes[i] = 0;

  for (const fish of input.match(/-?\d+/g)!.map(Number)) {
    store.fishes[fish]++;
  }

  const maxFish = createMemo(() => max(store.fishes)!);

  const x = scaleLinear([-1, 9], [10, width - 10]);
  const y = () => scaleLinear([0, maxFish()], [height - 5, 5]);
  const colorScale = scaleLinear([0, 8], [colors.pink, colors.blue]);

  const numRange = range(0, 9);

  const tick = createMemo(() => round(now() / animationDuration));

  const yTickFormatter = createMemo(() => y().tickFormat(2, 's'));
  const yTicks = createMemo(() => y().ticks(2));

  let i = 0;
  createEffect(() => {
    tick();
    i++;
    if (i < 5) return;
    untrack(() => {
      store.generation = store.generation + 1;
      let toAdd = 0;
      for (let i = 0; i <= 8; i++) {
        if (i === 0) toAdd = store.fishes[i];
        if (i > 0) store.fishes[i - 1] = store.fishes[i];
      }
      store.fishes[6] += toAdd;
      store.fishes[8] = toAdd;
    });
  });

  return (
    <svg
      class="day6-svg"
      viewBox={`0 0 ${width} ${height}`}
      style={{ 'max-width': '100%', 'max-height': '100%' }}
    >
      <For each={numRange}>
        {(i) => {
          const oi = () => (i - (store.generation % 8) + 8) % 8;

          return (
            <rect
              class="day6-rect"
              style={{ 'transition-duration': animationDuration + 'ms' }}
              x={x(oi())}
              y={y()(store.fishes[oi()])}
              width={x(oi() + 0.8) - x(oi())}
              height={y()(0) - y()(store.fishes[oi()])}
              stroke="none"
              fill={colorScale(oi())}
            />
          );
        }}
      </For>
      <text x={x(0)} y="10" font-size="2.5" fill="white" font-family="Arial">
        Generation: {store.generation} Population:{' '}
        {format(',')(sum(store.fishes))}
      </text>
      <line
        x1={x(-0.5)}
        x2={x(-0.5)}
        y1={y()(0)}
        y2={y().range()[1]}
        stroke="white"
        stroke-width="0.25"
      />
      <Index each={yTicks()}>
        {(item) => (
          <>
            <line
              style={{
                transition: 'all 1s',
                'transition-duration': animationDuration + 'ms',
              }}
              x1={x(-0.75)}
              x2={x(-0.5)}
              y1={0}
              y2={0}
              transform={`translate(0, ${y()(item())})`}
              stroke="white"
              stroke-width="0.25"
            />
            <text
              x={x(-0.8)}
              text-anchor="end"
              y={0}
              transform={`translate(0, ${y()(item())})`}
              font-size="3"
              fill="white"
              font-family="arial"
              alignment-baseline="middle"
              style={{
                transition: 'all 1s',
                'transition-duration': animationDuration + 'ms',
              }}
            >
              {yTickFormatter()(item())}
            </text>
          </>
        )}
      </Index>
    </svg>
  );
}
