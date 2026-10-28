import { ArrowLeft, FileText } from 'lucide';
import { PLATFORMS } from '../../data/platforms.js';
import { h, icon } from '../../lib/dom.js';
import { day } from '../../lib/format.js';

function templateNote(info, key) {
  const t = info?.platforms?.find((p) => p.key === key);
  if (!t) return null;
  return [t.max_rows ? `Up to ${t.max_rows} rows per file` : null, t.template_updated ? `template from ${day(t.template_updated)}` : null]
    .filter(Boolean)
    .join('  ·  ');
}

export function EmptyState(info) {
  return h(
    'div',
    { class: 'output-inner' },
    h(
      'header',
      { class: 'page-head' },
      h('p', { class: 'eyebrow' }, 'Output'),
      h('h1', {}, 'Marketplace upload files'),
      h(
        'p',
        { class: 'page-lead' },
        'Each file is the marketplace’s own template, filled in, with its dropdowns and hidden sheets left as they were. ' +
          'A report lists everything to fix or check before you upload.',
      ),
    ),
    h(
      'ul',
      { class: 'card plan-list' },
      PLATFORMS.map((p) =>
        h(
          'li',
          { class: 'plan-row' },
          h('span', { class: 'swatch', style: { background: p.color } }),
          h('div', { class: 'plan-main' }, h('div', { class: 'plan-name' }, p.name, h('span', { class: 'ext' }, p.ext)), h('p', {}, p.about)),
          h('span', { class: 'plan-note' }, templateNote(info, p.key)),
        ),
      ),
      h(
        'li',
        { class: 'plan-row' },
        icon(FileText, { size: 16, className: 'plan-report-icon' }),
        h(
          'div',
          { class: 'plan-main' },
          h('div', { class: 'plan-name' }, 'Listing report', h('span', { class: 'ext' }, '.xlsx')),
          h('p', {}, 'Every problem, check and automatic correction, one line per product.'),
        ),
        h('span', { class: 'plan-note' }),
      ),
    ),
    h(
      'div',
      { class: 'empty-cta' },
      icon(ArrowLeft, { size: 16, className: 'empty-cta-arrow' }),
      h('span', {}, 'Upload a filled master sheet under “New run” to create these files.'),
    ),
  );
}
