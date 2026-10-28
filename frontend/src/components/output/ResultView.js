import { Archive, CircleCheck, CircleX, Clock, FileText, Plus, TriangleAlert } from 'lucide';
import { fileUrl, zipUrl } from '../../api/client.js';
import { h, icon } from '../../lib/dom.js';
import { ago, clock, plural } from '../../lib/format.js';
import { countByLevel, groupIssues } from '../../lib/issues.js';
import { isExpired, keepMs, startNewRun } from '../../state/actions.js';
import { FilesTable } from './FilesTable.js';
import { IssuesPanel } from './IssuesPanel.js';

function verdict(counts, fileCount) {
  if (!fileCount) {
    return { tone: 'bad', icon: CircleX, badge: 'No files created', text: 'No marketplace file could be made. Fix the problems below in the master sheet and generate again.' };
  }
  if (counts.ERROR) {
    return {
      tone: 'bad',
      icon: CircleX,
      badge: `${plural(counts.ERROR, 'problem')} to fix`,
      text: 'Fix these in the master sheet and generate again before uploading. Affected products may be missing from the files.',
    };
  }
  if (counts.CHECK) {
    return {
      tone: 'warn',
      icon: TriangleAlert,
      badge: `${plural(counts.CHECK, 'point')} to review`,
      text: 'The files are ready. Read the points under “Review” before you upload.',
    };
  }
  return { tone: 'ok', icon: CircleCheck, badge: 'Ready to upload', text: 'No problems found. Upload each file in its seller panel.' };
}

function Stat(label, value, tone, onClick) {
  return h(
    'button',
    { class: `stat${value && tone ? ` stat-${tone}` : ''}`, type: 'button', onClick, disabled: !onClick },
    h('span', { class: 'stat-label' }, label),
    h('span', { class: 'stat-value num' }, value),
  );
}

export function ResultView(run) {
  const groups = groupIssues(run.result.issues);
  const counts = countByLevel(groups);
  const fileCount = run.result.platforms.reduce((n, p) => n + p.files.length, 0);
  const expired = isExpired(run);
  const v = verdict(counts, fileCount);
  const issues = IssuesPanel(groups);
  const openIssues = (level) => () => {
    issues.show(level);
    issues.el.scrollIntoView({ behavior: 'smooth', block: 'start' });
  };

  return [
    h(
      'div',
      { class: 'result-head' },
      h(
        'div',
        { class: 'output-inner result-head-inner' },
        h(
          'div',
          { class: 'result-title' },
          h('p', { class: 'eyebrow' }, `Run at ${clock(run.at)}  ·  ${ago(run.at)}`),
          h('h1', { class: 'truncate', title: run.fileName }, run.fileName),
        ),
        h(
          'div',
          { class: 'result-actions' },
          h(
            'a',
            {
              class: 'btn btn-primary',
              href: expired || !fileCount ? null : zipUrl(run.id),
              download: '',
              'aria-disabled': expired || !fileCount ? 'true' : null,
            },
            icon(Archive, { size: 16 }),
            'Download all (.zip)',
          ),
          h(
            'a',
            { class: 'btn btn-secondary', href: expired ? null : fileUrl(run.id, run.result.report), download: '', 'aria-disabled': expired ? 'true' : null },
            icon(FileText, { size: 16 }),
            'Report',
          ),
          h('button', { class: 'btn btn-ghost', type: 'button', onClick: startNewRun }, icon(Plus, { size: 16 }), 'New run'),
        ),
      ),
    ),
    h(
      'div',
      { class: 'output-inner result-body' },
      expired
        ? h(
            'div',
            { class: 'alert alert-warn' },
            icon(Clock, { size: 15 }),
            h('span', {}, 'These files were deleted from the main PC 2 hours after they were made. Upload the master sheet again to get new ones.'),
          )
        : null,
      h(
        'div',
        { class: `verdict verdict-${v.tone}` },
        h('span', { class: `badge badge-${v.tone}` }, icon(v.icon, { size: 15 }), v.badge),
        h('p', {}, v.text),
        !expired ? h('span', { class: 'verdict-keep' }, `Files kept until ${clock(run.at + keepMs())}`) : null,
      ),
      h(
        'div',
        { class: 'stats' },
        Stat('Files created', fileCount + 1, null, null),
        Stat('Must fix', counts.ERROR, 'bad', openIssues('ERROR')),
        Stat('To review', counts.CHECK, 'warn', openIssues('CHECK')),
        Stat('Fixed automatically', counts.INFO, 'ok', openIssues('INFO')),
      ),
      h(
        'section',
        { class: 'section', 'aria-labelledby': 'files-title' },
        h('div', { class: 'section-head' }, h('h2', { id: 'files-title' }, 'Files'), h('p', {}, 'Upload each file in its marketplace’s seller panel. The zip holds all of them and the report.')),
        FilesTable(run, groups, expired),
      ),
      issues.el,
    ),
  ];
}
