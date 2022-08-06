import { render } from 'solid-js/web';
import { Day11Viz } from './day11/ui';
import { Day2Viz } from './day2/ui';
import { Day23Viz } from './day23/ui';
import { Day25Viz } from './day25/ui';
import { Day5Viz } from './day5/ui';
import { Day6Viz } from './day6/ui';
import { Day7Viz } from './day7/ui';
import { Day9Viz } from './day9/ui';
import './index.css';

//render(() => <Day25Viz />, document.getElementById('app')!);
render(() => <Day23Viz />, document.getElementById('app')!);
