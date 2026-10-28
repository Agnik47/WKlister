import { CircleCheck } from 'lucide';
import { h, icon } from '../../lib/dom.js';

const ITEMS = [
  ['Products: one row per colour', 'Style Code is different for each colour. Parent Code is the same for all colours of one design.'],
  ['Sizes: one row per size', 'Use the same Style Code as in Products. Measurements are in inches, package in cm and grams.'],
  ['Prices decide the marketplaces', 'A product is listed only where its price and MRP are filled.'],
  ['Image links open the picture', 'Meesho accepts only links from its own image uploader. Use the Meesho Image columns for those.'],
];

export function Checklist() {
  return h(
    'section',
    { class: 'side-section', 'aria-labelledby': 'checklist-title' },
    h('h3', { class: 'eyebrow', id: 'checklist-title' }, 'Before you upload'),
    h(
      'ul',
      { class: 'checklist' },
      ITEMS.map(([title, text]) =>
        h('li', {}, icon(CircleCheck, { size: 16, className: 'checklist-icon' }), h('div', {}, h('strong', {}, title), h('p', {}, text))),
      ),
    ),
  );
}
