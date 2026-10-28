import { h } from '../lib/dom.js';
import { loadRuns, loadPref } from './storage.js';

/**
 * phase: 'idle'    nothing running, show the selected run or the empty state
 *        'running' waiting for /generate
 */
let state = {
  connected: null, // null = checking, true/false after /api/info
  info: null,
  file: null,
  fileError: null,
  phase: 'idle',
  runningFile: null,
  startedAt: null,
  runError: null,
  runs: loadRuns(),
  activeRunId: null,
  autoDownload: loadPref('autoDownload', true),
};

const listeners = new Set();

export const getState = () => state;

export function setState(patch) {
  state = { ...state, ...(typeof patch === 'function' ? patch(state) : patch) };
  for (const fn of listeners) fn(state);
}

export function subscribe(fn) {
  listeners.add(fn);
  return () => listeners.delete(fn);
}

export const activeRun = (s = state) => s.runs.find((r) => r.id === s.activeRunId) || null;

/**
 * A container that re-renders only when the selected values change.
 * select(state) returns an array; render(state) returns node(s).
 */
export function reactive(select, render, props = {}) {
  const el = h(props.tag || 'div', { ...props, tag: null });
  let prev = null;
  const update = (s) => {
    const next = select(s);
    if (prev && next.length === prev.length && next.every((v, i) => Object.is(v, prev[i]))) return;
    prev = next;
    el.replaceChildren(...[render(s)].flat().filter(Boolean));
  };
  update(state);
  subscribe(update);
  return el;
}
