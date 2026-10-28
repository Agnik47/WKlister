import * as api from '../api/client.js';
import { triggerDownload } from '../lib/dom.js';
import { getState, setState } from './store.js';
import { DEFAULT_KEEP_MS, saveRuns, savePref } from './storage.js';

const MAX_UPLOAD = 25 * 1024 * 1024;

export const keepMs = () => (getState().info?.keep_hours ?? 2) * 60 * 60 * 1000 || DEFAULT_KEEP_MS;
export const isExpired = (run) => Date.now() - run.at >= keepMs();

export async function loadInfo() {
  try {
    const info = await api.getInfo();
    setState({ info, connected: true });
  } catch {
    setState({ connected: false });
  }
}

export function chooseFile(file) {
  if (!file) return;
  if (!/\.xlsx$/i.test(file.name)) {
    setState({ fileError: `“${file.name}” is not an .xlsx file. Upload the filled Wish Karo master sheet.` });
    return;
  }
  if (file.size > MAX_UPLOAD) {
    setState({ fileError: 'This file is larger than 25 MB. Upload the master sheet only.' });
    return;
  }
  setState({ file, fileError: null, runError: null });
}

export const clearFile = () => setState({ file: null, fileError: null, runError: null });

export async function generate() {
  const { file, phase } = getState();
  if (!file || phase === 'running') return;
  setState({ phase: 'running', runningFile: file.name, startedAt: Date.now(), runError: null });
  revealOutput();
  try {
    const result = await api.generateFiles(file);
    const run = { id: result.job, fileName: file.name, fileSize: file.size, at: Date.now(), result };
    const runs = saveRuns([run, ...getState().runs.filter((r) => !isExpired(r))]);
    setState({ phase: 'idle', runs, activeRunId: run.id, file: null, connected: true });
    const fileCount = result.platforms.reduce((n, p) => n + p.files.length, 0);
    if (getState().autoDownload && fileCount) triggerDownload(api.zipUrl(run.id));
  } catch (err) {
    setState((s) => ({ phase: 'idle', runError: err.message, connected: err.offline ? false : s.connected }));
  }
}

// On phones the output sits below the form, so bring it into view.
function revealOutput() {
  if (window.matchMedia('(max-width: 1023px)').matches) {
    requestAnimationFrame(() => document.getElementById('output')?.scrollIntoView({ behavior: 'smooth', block: 'start' }));
  }
}

export function openRun(id) {
  setState({ activeRunId: id });
  revealOutput();
}

export function startNewRun() {
  setState({ activeRunId: null, runError: null });
  document.getElementById('master-file')?.focus();
}

export function setAutoDownload(on) {
  savePref('autoDownload', on);
  setState({ autoDownload: on });
}

export function forgetRun(id) {
  const runs = saveRuns(getState().runs.filter((r) => r.id !== id));
  setState((s) => ({ runs, activeRunId: s.activeRunId === id ? null : s.activeRunId }));
}
