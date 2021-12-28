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

export function Day7Viz() {
  let canvas: HTMLCanvasElement = null as any;

  const crabs = sortBy(input.match(/(\d+)/g)!.map(Number));
  const crabPositionExtent = extent(crabs) as Vector;

  const part1Result = median(crabs)!;
  const part2Result = 473;
  const crabPositionRange = range(...crabPositionExtent);

  const colorScale = scaleSqrt(crabPositionExtent, [
    colors.pink,
    colors.darkBlue,
  ]);

  onMount(() => {
    const height = crabs.length;
    const width = crabPositionExtent[1];
    canvas.width = width;
    canvas.height = height;

    const x = scaleLinear().domain(crabPositionExtent).rangeRound([0, width]);
    const y = scaleLinear().domain([0, crabs.length]).rangeRound([0, height]);

    const ctx = canvas.getContext('2d')!;

    ctx.fillStyle = colors.pink;
    console.time('draw');
    crabs.forEach((position, index) => {
      crabPositionRange.forEach((possiblePosition) => {
        const error = Math.abs(possiblePosition - position);
        ctx.fillStyle = colorScale(error);
        ctx.fillRect(
          x(possiblePosition),
          y(index),
          scaledDist(x, 1),
          scaledDist(y, 1)
        );
      });
    });
    console.timeEnd('draw');

    ctx.fillStyle = 'white';
    const resultWidth = 4;
    ctx.fillRect(
      x(part1Result) - resultWidth / 2,
      y(0),
      scaledDist(x, resultWidth),
      height
    );
    ctx.fillRect(
      x(part2Result) - resultWidth / 2,
      y(0),
      scaledDist(x, resultWidth),
      height
    );
  });

  return <canvas ref={canvas} />;
}

function sumUntil(n: number) {
  return (n * (n + 1)) / 2;
}
