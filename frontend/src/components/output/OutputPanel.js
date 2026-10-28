import { activeRun, reactive } from '../../state/store.js';
import { EmptyState } from './EmptyState.js';
import { ResultView } from './ResultView.js';
import { RunningState } from './RunningState.js';
import './output.css';

export function OutputPanel() {
  return reactive(
    (s) => [s.phase, s.activeRunId, s.runs, s.info],
    (s) => {
      if (s.phase === 'running') return RunningState(s);
      const run = activeRun(s);
      return run ? ResultView(run) : EmptyState(s.info);
    },
    { class: 'output-view' },
  );
}
