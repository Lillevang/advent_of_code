import { extent, format, median, scaleBand, scaleLinear, scaleSqrt } from 'd3';
import {
  createEffect,
  createMemo,
  For,
  onMount,
  untrack,
  Show,
  on,
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

export function Day23Viz() {
  const rooms = `
#############
#           #
### # # # ###
  # # # # #
  # # # # #
  # # # # #
  #########
`
    .trim()
    .split('\n')
    .flatMap((row, y) => row.split('').map((c, x) => ({ x, y, c })));

  type Room = typeof rooms[number];
  const initialEntities = [] as Room[];
  for (const [c, coordinates] of Object.entries(states[0].state)) {
    for (const [x, y] of coordinates) {
      initialEntities.push({ x, y, c });
    }
  }
  const store = createMutable({ entities: initialEntities });
  const letterColors = {
    A: colors.yellow,
    B: colors.blue,
    C: colors.darkGreen,
    D: colors.pink,
  };

  function* animationSteps() {
    yield;
    yield;
    for (const state of states.slice(1)) {
      const { from, to } = state.changed;
      const toChange = store.entities.find(
        ({ x, y }) => x === from[0] && y === from[1]
      );
      if (!toChange) {
        throw new Error('Should not happen');
      }
      const dx = to[0] - from[0];
      const dy = to[1] - from[1];
      if (dy < 0) {
        if (dy) {
          toChange.y = to[1];
          yield;
        }
        if (dx) {
          toChange.x = to[0];
          yield;
        }
      } else {
        if (dx) {
          toChange.x = to[0];
          yield;
        }
        if (dy) {
          toChange.y = to[1];
          yield;
        }
      }
    }
  }

  const tickLength = 500;
  const tick = createMemo(() => round(now() / tickLength));

  const steps = animationSteps();

  createEffect(
    on(tick, () => {
      steps.next();
    })
  );

  return (
    <svg
      viewBox="-1 -1 15 9"
      style={{
        'max-width': '100%',
        'max-height': '100%',
      }}
    >
      <For each={rooms}>
        {(room) => (
          <Show when={room.c === '#'}>
            <rect
              x={room.x}
              y={room.y}
              width={0.8}
              height={0.8}
              fill="white"
              shape-rendering="crispEdges"
            />
          </Show>
        )}
      </For>
      <For each={store.entities}>
        {(entity) => (
          <rect
            x={entity.x}
            y={entity.y}
            width={0.8}
            height={0.8}
            fill={letterColors[entity.c as keyof typeof letterColors]}
            shape-rendering="crispEdges"
            style={{ transition: `all ${tickLength}ms` }}
          />
        )}
      </For>
    </svg>
  );
}

const statesString = `
#############
#...........#
###B#C#A#D###
  #D#C#B#A#
  #D#B#A#C#
  #B#C#D#A#
  #########

#############
#A..........#
###B#C#.#D###
  #D#C#B#A#
  #D#B#A#C#
  #B#C#D#A#
  #########

#############
#A........B.#
###B#C#.#D###
  #D#C#.#A#
  #D#B#A#C#
  #B#C#D#A#
  #########

#############
#AA.......B.#
###B#C#.#D###
  #D#C#.#A#
  #D#B#.#C#
  #B#C#D#A#
  #########

#############
#AA.D.....B.#
###B#C#.#D###
  #D#C#.#A#
  #D#B#.#C#
  #B#C#.#A#
  #########

#############
#AA.D.C...B.#
###B#.#.#D###
  #D#C#.#A#
  #D#B#.#C#
  #B#C#.#A#
  #########

#############
#AA.D.....B.#
###B#.#.#D###
  #D#C#.#A#
  #D#B#.#C#
  #B#C#C#A#
  #########

#############
#AA.D.C...B.#
###B#.#.#D###
  #D#.#.#A#
  #D#B#.#C#
  #B#C#C#A#
  #########

#############
#AA.D.....B.#
###B#.#.#D###
  #D#.#.#A#
  #D#B#C#C#
  #B#C#C#A#
  #########

#############
#AA.D...B.B.#
###B#.#.#D###
  #D#.#.#A#
  #D#.#C#C#
  #B#C#C#A#
  #########

#############
#AA.D.C.B.B.#
###B#.#.#D###
  #D#.#.#A#
  #D#.#C#C#
  #B#.#C#A#
  #########

#############
#AA.D...B.B.#
###B#.#.#D###
  #D#.#C#A#
  #D#.#C#C#
  #B#.#C#A#
  #########

#############
#AA.D.....B.#
###B#.#.#D###
  #D#.#C#A#
  #D#.#C#C#
  #B#B#C#A#
  #########

#############
#AA.D.......#
###B#.#.#D###
  #D#.#C#A#
  #D#B#C#C#
  #B#B#C#A#
  #########

#############
#AA.D.D.....#
###B#.#.#.###
  #D#.#C#A#
  #D#B#C#C#
  #B#B#C#A#
  #########

#############
#AA.D.D....A#
###B#.#.#.###
  #D#.#C#.#
  #D#B#C#C#
  #B#B#C#A#
  #########

#############
#AA.D.D.C..A#
###B#.#.#.###
  #D#.#C#.#
  #D#B#C#.#
  #B#B#C#A#
  #########

#############
#AA.D.D.C.AA#
###B#.#.#.###
  #D#.#C#.#
  #D#B#C#.#
  #B#B#C#.#
  #########

#############
#AA.D.D...AA#
###B#.#C#.###
  #D#.#C#.#
  #D#B#C#.#
  #B#B#C#.#
  #########

#############
#AA.D.....AA#
###B#.#C#.###
  #D#.#C#.#
  #D#B#C#.#
  #B#B#C#D#
  #########

#############
#AA.......AA#
###B#.#C#.###
  #D#.#C#.#
  #D#B#C#D#
  #B#B#C#D#
  #########

#############
#AA.B.....AA#
###.#.#C#.###
  #D#.#C#.#
  #D#B#C#D#
  #B#B#C#D#
  #########

#############
#AA.......AA#
###.#.#C#.###
  #D#B#C#.#
  #D#B#C#D#
  #B#B#C#D#
  #########

#############
#AA.....D.AA#
###.#.#C#.###
  #.#B#C#.#
  #D#B#C#D#
  #B#B#C#D#
  #########

#############
#AA...D.D.AA#
###.#.#C#.###
  #.#B#C#.#
  #.#B#C#D#
  #B#B#C#D#
  #########

#############
#AA.B.D.D.AA#
###.#.#C#.###
  #.#B#C#.#
  #.#B#C#D#
  #.#B#C#D#
  #########

#############
#A..B.D.D.AA#
###.#.#C#.###
  #.#B#C#.#
  #.#B#C#D#
  #A#B#C#D#
  #########

#############
#...B.D.D.AA#
###.#.#C#.###
  #.#B#C#.#
  #A#B#C#D#
  #A#B#C#D#
  #########

#############
#.....D.D.AA#
###.#B#C#.###
  #.#B#C#.#
  #A#B#C#D#
  #A#B#C#D#
  #########

#############
#.....D...AA#
###.#B#C#.###
  #.#B#C#D#
  #A#B#C#D#
  #A#B#C#D#
  #########

#############
#.........AA#
###.#B#C#D###
  #.#B#C#D#
  #A#B#C#D#
  #A#B#C#D#
  #########

#############
#..........A#
###.#B#C#D###
  #A#B#C#D#
  #A#B#C#D#
  #A#B#C#D#
  #########

#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #A#B#C#D#
  #A#B#C#D#
  #########
`;

const states = statesString
  .trim()
  .split('\n\n')
  .map((x) => x.split('\n').map((r) => r.split('')))
  .map((grid) => {
    const coords = {
      A: [] as [number, number][],
      B: [] as [number, number][],
      C: [] as [number, number][],
      D: [] as [number, number][],
    };
    grid.forEach((row, y) =>
      row.forEach((c, x) => {
        if (c === '.' || c === '#' || c === ' ') return;
        coords[c as keyof typeof coords].push([x, y]);
      })
    );
    return coords;
  })
  .map((state, index, states) => {
    const prev = states[index - 1];
    if (!prev) {
      return { state, changed: { from: state.A[0], to: state.A[0] } };
    }
    for (const c of ['A', 'B', 'C', 'D'] as const) {
      let to = differenceBy(state[c], prev[c], JSON.stringify)[0];
      let from = differenceBy(prev[c], state[c], JSON.stringify)[0];
      if (!from || !to) continue;
      return { state, changed: { from, to } };
    }
    throw new Error('Should never happen');
  });
