import { CircleHelp, Download, RefreshCw } from 'lucide';
import { BLANK_MASTER_URL } from '../../api/client.js';
import { h, icon } from '../../lib/dom.js';
import { loadInfo } from '../../state/actions.js';
import { reactive } from '../../state/store.js';
import './header.css';

function ConnectionStatus() {
  return reactive(
    (s) => [s.connected],
    (s) => {
      if (s.connected === false) {
        return h(
          'button',
          {
            class: 'conn conn-off',
            type: 'button',
            title: 'The tool on the main PC is not answering. Click to check again.',
            onClick: () => loadInfo(),
          },
          h('span', { class: 'conn-dot' }),
          h('span', { class: 'conn-label' }, 'Not connected'),
          icon(RefreshCw, { size: 13 }),
        );
      }
      return h(
        'span',
        { class: `conn ${s.connected ? 'conn-on' : 'conn-wait'}`, role: 'status' },
        h('span', { class: 'conn-dot' }),
        h('span', { class: 'conn-label' }, s.connected ? 'Connected' : 'Connecting…'),
      );
    },
    { class: 'conn-wrap' },
  );
}

export function AppHeader({ onHelp }) {
  return h(
    'header',
    { class: 'app-header' },
    h(
      'div',
      { class: 'brand' },
      h('span', { class: 'brand-mark', 'aria-hidden': 'true' }, 'WK'),
      h('span', { class: 'brand-name' }, h('strong', {}, 'Wish Karo'), h('span', {}, 'Listing Tool')),
    ),
    h('span', { class: 'header-scope' }, 'Kids dresses  ·  Meesho, Flipkart, Myntra, Amazon'),
    h(
      'div',
      { class: 'header-actions' },
      ConnectionStatus(),
      h(
        'a',
        { class: 'btn btn-secondary btn-sm', href: BLANK_MASTER_URL, download: '', title: 'Download the empty master sheet' },
        icon(Download, { size: 15 }),
        h('span', { class: 'hide-narrow' }, 'Blank master sheet'),
      ),
      h(
        'button',
        { class: 'btn btn-ghost btn-sm', type: 'button', onClick: onHelp },
        icon(CircleHelp, { size: 16 }),
        h('span', { class: 'hide-narrow' }, 'Help'),
      ),
    ),
  );
}
