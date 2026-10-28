import { Search } from 'lucide';
import { sourceColor } from '../../data/platforms.js';
import { h, icon } from '../../lib/dom.js';
import { fieldLabel } from '../../lib/format.js';
import { LEVELS, countByLevel, filterIssues } from '../../lib/issues.js';

function skuText(skus) {
  if (!skus.length) return null;
  if (skus.length > 2) return `${skus.length} sizes`;
  return skus.join(', ');
}

function IssueRow(g) {
  return h(
    'tr',
    {},
    h('td', {}, h('span', { class: 'cell-platform' }, h('span', { class: 'swatch', style: { background: sourceColor(g.platform) } }), g.platform)),
    h(
      'td',
      { class: 'cell-product' },
      g.style ? h('div', { class: 'mono' }, g.style) : h('span', { class: 'cell-muted' }, 'Whole sheet'),
      skuText(g.skus) && h('div', { class: 'cell-muted mono-sm', title: g.skus.join('\n') }, skuText(g.skus)),
    ),
    h('td', { class: 'cell-field' }, fieldLabel(g.field)),
    // the tab already says these were fixed automatically
    h('td', { class: 'cell-msg' }, g.level === 'INFO' ? g.msg.replace(/^Auto-fixed:?\s*/i, '') : g.msg),
  );
}

/** Returns { el, show(levelKey) } so the summary numbers can open a tab. */
export function IssuesPanel(groups) {
  const counts = countByLevel(groups);
  const view = {
    level: (LEVELS.find((l) => counts[l.key]) || LEVELS[0]).key,
    platform: '',
    query: '',
  };

  const sources = [...new Set(groups.map((g) => g.platform))];
  const list = h('div', { class: 'issues-list', id: 'issues-list', role: 'tabpanel' });

  const tabs = LEVELS.map((l) =>
    h(
      'button',
      {
        class: 'tab',
        type: 'button',
        role: 'tab',
        id: `tab-${l.id}`,
        'aria-controls': 'issues-list',
        onClick: () => show(l.key),
      },
      l.label,
      h('span', { class: `pill ${counts[l.key] ? { ERROR: 'pill-bad', CHECK: 'pill-warn', INFO: 'pill-ok' }[l.key] : 'pill-muted'}` }, counts[l.key]),
    ),
  );

  const platformSelect = h(
    'select',
    {
      'aria-label': 'Filter by source',
      onChange: (e) => {
        view.platform = e.target.value;
        renderList();
      },
    },
    h('option', { value: '' }, 'All sources'),
    sources.map((s) => h('option', { value: s }, s)),
  );

  const search = h('input', {
    type: 'search',
    placeholder: 'Search style code, SKU or text',
    'aria-label': 'Search issues',
    onInput: (e) => {
      view.query = e.target.value;
      renderList();
    },
  });

  function renderList() {
    tabs.forEach((t, i) => t.setAttribute('aria-selected', String(LEVELS[i].key === view.level)));
    list.setAttribute('aria-labelledby', `tab-${LEVELS.find((l) => l.key === view.level).id}`);
    const rows = filterIssues(groups, view);
    if (!rows.length) {
      const filtered = view.platform || view.query;
      list.replaceChildren(
        h(
          'div',
          { class: 'issues-empty' },
          filtered ? 'No issues match these filters.' : LEVELS.find((l) => l.key === view.level).empty,
          filtered &&
            h(
              'button',
              {
                class: 'btn btn-ghost btn-sm',
                type: 'button',
                onClick: () => {
                  view.platform = '';
                  view.query = '';
                  platformSelect.value = '';
                  search.value = '';
                  renderList();
                },
              },
              'Clear filters',
            ),
        ),
      );
      return;
    }
    list.replaceChildren(
      h(
        'div',
        { class: 'table-wrap' },
        h(
          'table',
          { class: 'data-table issues-table' },
          h(
            'thead',
            {},
            h('tr', {}, h('th', { scope: 'col' }, 'Source'), h('th', { scope: 'col' }, 'Product'), h('th', { scope: 'col' }, 'Field'), h('th', { scope: 'col' }, 'What to do')),
          ),
          h('tbody', {}, rows.map(IssueRow)),
        ),
      ),
    );
  }

  function show(levelKey) {
    view.level = levelKey;
    renderList();
  }

  renderList();

  const el = h(
    'section',
    { class: 'section', id: 'issues', 'aria-labelledby': 'issues-title' },
    h(
      'div',
      { class: 'section-head' },
      h('h2', { id: 'issues-title' }, 'Issues'),
      h('p', {}, 'Grouped per product. The same list is in the Excel report.'),
    ),
    h(
      'div',
      { class: 'card issues-card' },
      h(
        'div',
        { class: 'issues-toolbar' },
        h('div', { class: 'tabs', role: 'tablist', 'aria-label': 'Issue type' }, tabs),
        h(
          'div',
          { class: 'issues-filters' },
          h('label', { class: 'field field-select' }, platformSelect),
          h('label', { class: 'field field-search' }, icon(Search, { size: 15 }), search),
        ),
      ),
      list,
    ),
  );

  return { el, show };
}
