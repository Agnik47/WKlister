// Fonts are bundled, so the page looks the same on the office PC without internet.
import '@fontsource/ibm-plex-sans/latin-400.css';
import '@fontsource/ibm-plex-sans/latin-500.css';
import '@fontsource/ibm-plex-sans/latin-600.css';
import '@fontsource/ibm-plex-mono/latin-400.css';
import '@fontsource/ibm-plex-mono/latin-500.css';

import './styles/tokens.css';
import './styles/base.css';
import './styles/controls.css';
import './styles/layout.css';

import { AppHeader } from './components/header/AppHeader.js';
import { HelpDialog, openHelp } from './components/header/HelpDialog.js';
import { OutputPanel } from './components/output/OutputPanel.js';
import { Checklist } from './components/sidebar/Checklist.js';
import { RecentRuns } from './components/sidebar/RecentRuns.js';
import { UploadPanel } from './components/sidebar/UploadPanel.js';
import { h } from './lib/dom.js';
import { loadInfo } from './state/actions.js';

document.getElementById('app').replaceChildren(
  AppHeader({ onHelp: openHelp }),
  h(
    'div',
    { class: 'workspace' },
    h('aside', { class: 'sidebar', 'aria-label': 'New run' }, UploadPanel(), Checklist(), RecentRuns()),
    h('main', { class: 'output', id: 'output' }, OutputPanel()),
  ),
  HelpDialog(),
);

loadInfo();
