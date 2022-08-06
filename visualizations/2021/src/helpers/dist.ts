import { ScaleLinear } from 'd3';

export function scaledDist(
  scale: ScaleLinear<number, number, any>,
  dist: number
) {
  const start = scale(0);
  const end = scale(0 + dist);
  return end - start;
}
