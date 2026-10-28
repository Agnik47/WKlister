// Talks to app.py. The /generate and /download routes are the same ones the old page used.

const OFFLINE = 'Could not reach the tool. Check that the black window on the main PC is still open.';

async function readJson(res) {
  let data = {};
  try {
    data = await res.json();
  } catch {
    if (res.status === 413) throw new Error('This file is larger than 25 MB. Upload the master sheet only.');
  }
  if (!res.ok || data.error) {
    throw new Error(data.error || `The tool answered with an error (${res.status}). Try again.`);
  }
  return data;
}

export async function getInfo() {
  const res = await fetch('/api/info', { cache: 'no-store' });
  return readJson(res);
}

export async function generateFiles(file) {
  const body = new FormData();
  body.append('master', file);
  let res;
  try {
    res = await fetch('/generate', { method: 'POST', body });
  } catch {
    throw Object.assign(new Error(OFFLINE), { offline: true });
  }
  return readJson(res);
}

export const fileUrl = (job, name) => `/download/${job}/${encodeURIComponent(name)}`;
export const zipUrl = (job) => `/download/${job}/all.zip`;
export const BLANK_MASTER_URL = '/blank-master';
