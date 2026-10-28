import { Download, FileText } from 'lucide';
import { fileUrl } from '../../api/client.js';
import { platformByName } from '../../data/platforms.js';
import { h, icon } from '../../lib/dom.js';
import { countForPlatform } from '../../lib/issues.js';

function downloadButton(href, label, disabled) {
  return h(
    'a',
    { class: 'btn btn-secondary btn-sm', href: disabled ? null : href, download: '', 'aria-disabled': disabled ? 'true' : null },
    icon(Download, { size: 14 }),
    label,
  );
}

function issueCell(groups, name) {
  const c = countForPlatform(groups, name);
  if (!c.ERROR && !c.CHECK) return h('span', { class: 'cell-muted' }, 'None');
  return h(
    'span',
    { class: 'pill-row' },
    c.ERROR ? h('span', { class: 'pill pill-bad' }, `${c.ERROR} to fix`) : null,
    c.CHECK ? h('span', { class: 'pill pill-warn' }, `${c.CHECK} to review`) : null,
  );
}

export function FilesTable(run, groups, expired) {
  const { job, platforms, report } = run.result;
  const rows = platforms.map((p) => {
    const meta = platformByName(p.name);
    const made = p.files.length > 0;
    return h(
      'tr',
      { class: made ? '' : 'is-skipped' },
      h(
        'td',
        {},
        h('span', { class: 'cell-platform' }, h('span', { class: 'swatch', style: { background: meta?.color } }), p.name),
      ),
      h(
        'td',
        { class: 'cell-file' },
        made
          ? p.files.map((f) => h('div', { class: 'mono file-name', title: f }, f))
          : h('div', {}, h('span', { class: 'cell-strong' }, 'Not created'), h('div', { class: 'cell-muted' }, 'No product has a price for this marketplace, or all were blocked by errors.')),
      ),
      h('td', { class: 'num cell-right' }, made ? p.products : '–'),
      h('td', { class: 'num cell-right' }, made ? p.rows : '–'),
      h('td', {}, issueCell(groups, p.name)),
      h(
        'td',
        { class: 'cell-actions' },
        made ? p.files.map((f, i) => downloadButton(fileUrl(job, f), p.files.length > 1 ? `Part ${i + 1}` : 'Download', expired)) : null,
      ),
    );
  });

  rows.push(
    h(
      'tr',
      { class: 'is-report' },
      h('td', {}, h('span', { class: 'cell-platform' }, icon(FileText, { size: 15, className: 'report-icon' }), 'Report')),
      h('td', { class: 'cell-file' }, h('div', { class: 'mono file-name', title: report }, report)),
      h('td', { class: 'cell-right cell-muted', colspan: '3' }, 'All issues, one line per product'),
      h('td', { class: 'cell-actions' }, downloadButton(fileUrl(job, report), 'Download', expired)),
    ),
  );

  return h(
    'div',
    { class: 'card table-wrap' },
    h(
      'table',
      { class: 'data-table files-table' },
      h(
        'thead',
        {},
        h(
          'tr',
          {},
          h('th', { scope: 'col' }, 'Marketplace'),
          h('th', { scope: 'col' }, 'File'),
          h('th', { scope: 'col', class: 'cell-right' }, 'Products'),
          h('th', { scope: 'col', class: 'cell-right' }, 'Rows'),
          h('th', { scope: 'col' }, 'Issues'),
          h('th', { scope: 'col' }, h('span', { class: 'sr-only' }, 'Download')),
        ),
      ),
      h('tbody', {}, rows),
    ),
  );
}
