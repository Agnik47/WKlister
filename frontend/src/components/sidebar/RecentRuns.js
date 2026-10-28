import { h } from '../../lib/dom.js';
import { clock, plural } from '../../lib/format.js';
import { countByLevel, groupIssues } from '../../lib/issues.js';
import { isExpired, openRun } from '../../state/actions.js';
import { reactive } from '../../state/store.js';

export function runStatus(run) {
  const counts = countByLevel(groupIssues(run.result.issues));
  if (counts.ERROR) return { tone: 'bad', text: `${counts.ERROR} to fix` };
  if (counts.CHECK) return { tone: 'warn', text: `${counts.CHECK} to review` };
  return { tone: 'ok', text: 'Ready' };
}

function RunItem(run, active) {
  const files = run.result.platforms.reduce((n, p) => n + p.files.length, 0);
  const expired = isExpired(run);
  const status = runStatus(run);
  return h(
    'li',
    {},
    h(
      'button',
      {
        class: `run-item${active ? ' is-active' : ''}`,
        type: 'button',
        'aria-current': active ? 'true' : null,
        onClick: () => openRun(run.id),
      },
      h('span', { class: `run-dot tone-${expired ? 'muted' : status.tone}` }),
      h(
        'span',
        { class: 'run-text' },
        h('span', { class: 'run-name', title: run.fileName }, run.fileName),
        h('span', { class: 'run-meta' }, `${clock(run.at)}  ·  ${plural(files, 'file')}  ·  ${expired ? 'expired' : status.text}`),
      ),
    ),
  );
}

export function RecentRuns() {
  return h(
    'section',
    { class: 'side-section', 'aria-labelledby': 'runs-title' },
    h('h3', { class: 'eyebrow', id: 'runs-title' }, 'Recent runs'),
    reactive(
      (s) => [s.runs, s.activeRunId],
      (s) =>
        s.runs.length
          ? h('ul', { class: 'run-list' }, s.runs.map((r) => RunItem(r, r.id === s.activeRunId)))
          : h('p', { class: 'side-empty' }, 'Runs from this browser show here for 2 hours, while their files are kept.'),
    ),
  );
}
