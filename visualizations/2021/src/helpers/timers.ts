import { createSignal, createMemo } from 'solid-js';

const [now, setNow] = createSignal(0);

export const createFrame = () => createMemo(() => Math.floor(now() / 16));

export { now };

function update(ms: number) {
  setNow(ms);
  requestAnimationFrame(update);
}
requestAnimationFrame(update);
