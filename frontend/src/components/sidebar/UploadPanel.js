import { FileSpreadsheet, LoaderCircle, TriangleAlert, Upload, X } from 'lucide';
import { h, icon } from '../../lib/dom.js';
import { day, fileSize } from '../../lib/format.js';
import { chooseFile, clearFile, generate, setAutoDownload } from '../../state/actions.js';
import { reactive } from '../../state/store.js';
import './sidebar.css';

function Dropzone(input) {
  const zone = h(
    'label',
    { class: 'dropzone', for: 'master-file' },
    h('span', { class: 'dropzone-icon' }, icon(Upload, { size: 20 })),
    h('span', { class: 'dropzone-title' }, 'Drop the filled master sheet here'),
    h('span', { class: 'dropzone-hint' }, h('u', {}, 'Choose file'), '  ·  .xlsx, up to 25 MB'),
  );
  const over = (on) => (e) => {
    e.preventDefault();
    zone.classList.toggle('is-over', on);
  };
  zone.addEventListener('dragenter', over(true));
  zone.addEventListener('dragover', over(true));
  zone.addEventListener('dragleave', over(false));
  zone.addEventListener('drop', (e) => {
    over(false)(e);
    chooseFile(e.dataTransfer.files[0]);
  });
  return zone;
}

function FileCard(file, input, busy) {
  return h(
    'div',
    { class: 'file-card' },
    h('span', { class: 'file-card-icon' }, icon(FileSpreadsheet, { size: 20 })),
    h(
      'div',
      { class: 'file-card-text' },
      h('div', { class: 'file-card-name', title: file.name }, file.name),
      h('div', { class: 'file-card-meta' }, `${fileSize(file.size)}  ·  saved ${day(file.lastModified)}`),
    ),
    h('button', { class: 'btn btn-ghost btn-sm', type: 'button', disabled: busy, onClick: () => input.click() }, 'Change'),
    h('button', { class: 'icon-btn', type: 'button', disabled: busy, 'aria-label': 'Remove file', onClick: clearFile }, icon(X, { size: 16 })),
  );
}

export function UploadPanel() {
  // the input stays mounted so "Change" and the drop zone label can both use it
  const input = h('input', {
    id: 'master-file',
    class: 'sr-only',
    type: 'file',
    accept: '.xlsx,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    onChange: (e) => {
      chooseFile(e.target.files[0]);
      e.target.value = '';
    },
  });

  const body = reactive(
    (s) => [s.file, s.fileError, s.phase, s.runError, s.autoDownload],
    (s) => {
      const busy = s.phase === 'running';
      return [
        s.file ? FileCard(s.file, input, busy) : Dropzone(input),
        s.fileError && h('div', { class: 'alert alert-bad', role: 'alert' }, icon(TriangleAlert, { size: 15 }), h('span', {}, s.fileError)),
        h(
          'button',
          { class: 'btn btn-primary btn-lg btn-block', type: 'button', disabled: !s.file || busy, onClick: generate },
          busy ? [icon(LoaderCircle, { size: 18, className: 'spin' }), 'Generating…'] : 'Generate files',
        ),
        h(
          'label',
          { class: 'checkbox' },
          h('input', { type: 'checkbox', checked: s.autoDownload, onChange: (e) => setAutoDownload(e.target.checked) }),
          'Download the zip as soon as it is ready',
        ),
        s.runError &&
          h(
            'div',
            { class: 'alert alert-bad', role: 'alert' },
            icon(TriangleAlert, { size: 15 }),
            h('div', {}, h('strong', {}, 'Files were not created. '), s.runError),
          ),
      ];
    },
    { class: 'upload-body' },
  );

  return h(
    'section',
    { class: 'side-section', 'aria-labelledby': 'new-run-title' },
    h(
      'div',
      { class: 'side-head' },
      h('h2', { id: 'new-run-title' }, 'New run'),
      h('p', {}, 'Upload the filled master sheet to make the upload file for each marketplace.'),
    ),
    input,
    body,
  );
}
