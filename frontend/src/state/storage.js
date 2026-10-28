// Recent runs and preferences live in this browser only. Storage can be blocked
// (private windows), so every access is wrapped and the app works without it.

const RUNS_KEY = 'wk-listing.runs.v1';
const PREF_KEY = 'wk-listing.prefs.v1';
const MAX_RUNS = 10;
export const DEFAULT_KEEP_MS = 2 * 60 * 60 * 1000; // app.py deletes job files after 2 hours

function read(key, fallback) {
  try {
    const raw = localStorage.getItem(key);
    return raw ? JSON.parse(raw) : fallback;
  } catch {
    return fallback;
  }
}

function write(key, value) {
  try {
    localStorage.setItem(key, JSON.stringify(value));
  } catch {
    /* storage full or blocked: keep working in memory */
  }
}

export function loadRuns(keepMs = DEFAULT_KEEP_MS) {
  const runs = read(RUNS_KEY, []);
  return Array.isArray(runs) ? runs.filter((r) => r && r.id && Date.now() - r.at < keepMs) : [];
}

export function saveRuns(runs) {
  const trimmed = runs.slice(0, MAX_RUNS);
  write(RUNS_KEY, trimmed);
  return trimmed;
}

export function loadPref(name, fallback) {
  const prefs = read(PREF_KEY, {});
  return name in prefs ? prefs[name] : fallback;
}

export function savePref(name, value) {
  write(PREF_KEY, { ...read(PREF_KEY, {}), [name]: value });
}
