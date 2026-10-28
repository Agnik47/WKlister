import { LoaderCircle } from 'lucide';
import { PLATFORMS } from '../../data/platforms.js';
import { h, icon } from '../../lib/dom.js';
import { seconds } from '../../lib/format.js';

export function RunningState(s) {
  const elapsed = h('span', { class: 'num' }, seconds(Date.now() - s.startedAt));
  const timer = setInterval(() => {
    if (!elapsed.isConnected) return clearInterval(timer);
    elapsed.textContent = seconds(Date.now() - s.startedAt);
  }, 1000);

  return h(
    'div',
    { class: 'output-inner' },
    h(
      'header',
      { class: 'page-head' },
      h('p', { class: 'eyebrow' }, 'Generating'),
      h('h1', { class: 'truncate', title: s.runningFile }, s.runningFile),
      h(
        'p',
        { class: 'page-lead' },
        'Checking the sheet, correcting typing mistakes and filling the four templates. This usually takes under a minute; the Flipkart file takes longest. Keep this page open.',
      ),
    ),
    h(
      'div',
      { class: 'card running', role: 'status', 'aria-live': 'polite' },
      h(
        'div',
        { class: 'running-top' },
        icon(LoaderCircle, { size: 20, className: 'spin running-spinner' }),
        h('strong', {}, 'Working on your files'),
        h('span', { class: 'running-time' }, 'Elapsed ', elapsed),
      ),
      h('div', { class: 'meter', 'aria-hidden': 'true' }, h('span')),
      h(
        'ul',
        { class: 'running-list' },
        PLATFORMS.map((p) =>
          h('li', {}, h('span', { class: 'swatch', style: { background: p.color } }), p.name, h('span', { class: 'ext' }, p.ext)),
        ),
      ),
    ),
  );
}
