import { X } from 'lucide';
import { h, icon } from '../../lib/dom.js';
import './help.css';

const STEPS = [
  ['Fill the master sheet', 'Download the blank sheet from the top bar. Products: one row per colour. Sizes: one row per size. Settings: fill once.'],
  ['Upload it and generate', 'The tool checks the sheet, corrects typing mistakes and fills each marketplace’s own template.'],
  ['Fix, then upload', 'Correct anything under “Must fix” in the master sheet and generate again. Then upload each file in its seller panel.'],
];

const CORRECTIONS = [
  'Double and stray spaces in titles, descriptions, style codes and image links',
  'Prices typed as “Rs. 749” or “₹749” become 749',
  'Sizes typed as “6 - 7 years” or “3-6m” become 6-7 Years and 3-6 Months',
  'Dropdown values typed in the wrong capitals are matched to the list',
  'The same colour typed on several rows is merged into one row',
  'A secondary colour equal to the primary colour is cleared',
  'A shoulder value that is a copy of the front length is cleared',
  'An impossible Meesho kids weight is replaced by the range for that size',
  '“Wishkaro” in Meesho text becomes “Silver Kraft”',
];

const RULES = [
  ['SKU', 'Style Code + size, for example bxa245pkblu_3-6_Months. The same SKU is used on every marketplace.'],
  ['Parent Code', 'Joins the colours of one design, for example bxa245. Used for the Amazon parent row and the Meesho and Flipkart Group ID.'],
  ['Prices', 'Leave a marketplace’s price empty and that product is left out of that marketplace’s file.'],
  ['Baby or girls', 'Sizes up to 1-2 Years are listed as baby girls, larger sizes as girls.'],
];

const PROBLEMS = [
  ['“Could not reach the tool”', 'The black window on the main PC was closed, or the PC is off. Start start_website.bat again.'],
  ['No Flipkart file', 'LibreOffice is not installed on the main PC. Install it (free) and generate again.'],
  ['“Not the master sheet”', 'Upload the filled Wish Karo master sheet (.xlsx), not a file downloaded from a marketplace.'],
  ['A download does nothing', 'Files are deleted from the main PC 2 hours after they are made. Generate again.'],
];

let dialog;

export function openHelp() {
  dialog?.showModal();
}

export function HelpDialog() {
  const close = () => dialog.close();
  dialog = h(
    'dialog',
    {
      class: 'help',
      'aria-labelledby': 'help-title',
      onClick: (e) => {
        if (e.target === dialog) close(); // click on the backdrop
      },
    },
    h(
      'div',
      { class: 'help-head' },
      h('h2', { id: 'help-title' }, 'Help'),
      h('button', { class: 'icon-btn', type: 'button', 'aria-label': 'Close help', onClick: close }, icon(X, { size: 18 })),
    ),
    h(
      'div',
      { class: 'help-body' },
      h(
        'section',
        {},
        h('h3', {}, 'How it works'),
        h('ol', { class: 'help-steps' }, STEPS.map(([t, d]) => h('li', {}, h('strong', {}, t), h('p', {}, d)))),
      ),
      h(
        'section',
        {},
        h('h3', {}, 'Corrections made for you'),
        h('p', { class: 'help-lead' }, 'Each one is listed under “Fixed automatically” after a run, so you can correct the master sheet too.'),
        h('ul', { class: 'help-list' }, CORRECTIONS.map((c) => h('li', {}, c))),
      ),
      h('section', {}, h('h3', {}, 'How products are joined'), h('dl', { class: 'help-defs' }, RULES.map(([t, d]) => [h('dt', {}, t), h('dd', {}, d)]))),
      h('section', {}, h('h3', {}, 'If something goes wrong'), h('dl', { class: 'help-defs' }, PROBLEMS.map(([t, d]) => [h('dt', {}, t), h('dd', {}, d)]))),
    ),
  );
  return dialog;
}
