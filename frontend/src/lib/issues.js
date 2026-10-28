// The generator reports one line per size. Group them the way the Excel report does:
// one line per (level, platform, product, field, message), listing the SKUs it applies to.

export const LEVELS = [
  { key: 'ERROR', id: 'fix', label: 'Must fix', empty: 'Nothing to fix. Every product passed the checks.' },
  { key: 'CHECK', id: 'review', label: 'Review', empty: 'Nothing to review.' },
  { key: 'INFO', id: 'fixed', label: 'Fixed automatically', empty: 'The sheet needed no corrections.' },
];

export function groupIssues(issues = []) {
  const groups = new Map();
  for (const i of issues) {
    const id = [i.level, i.platform, i.style, i.field, i.msg].join('\u0000');
    if (!groups.has(id)) {
      groups.set(id, { level: i.level, platform: i.platform, style: i.style, field: i.field, msg: i.msg, skus: [] });
    }
    if (i.sku && !groups.get(id).skus.includes(i.sku)) groups.get(id).skus.push(i.sku);
  }
  return [...groups.values()];
}

export function countByLevel(groups) {
  const counts = { ERROR: 0, CHECK: 0, INFO: 0 };
  for (const g of groups) counts[g.level] = (counts[g.level] || 0) + 1;
  return counts;
}

export function countForPlatform(groups, platform) {
  const counts = { ERROR: 0, CHECK: 0 };
  for (const g of groups) if (g.platform === platform && g.level in counts) counts[g.level] += 1;
  return counts;
}

export function filterIssues(groups, { level, platform, query }) {
  const q = (query || '').trim().toLowerCase();
  return groups.filter((g) => {
    if (level && g.level !== level) return false;
    if (platform && g.platform !== platform) return false;
    if (!q) return true;
    return [g.platform, g.style, g.field, g.msg, ...g.skus].join(' ').toLowerCase().includes(q);
  });
}
