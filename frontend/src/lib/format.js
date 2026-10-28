export const plural = (n, one, many = `${one}s`) => `${n} ${n === 1 ? one : many}`;

export function fileSize(bytes) {
  if (bytes == null) return '';
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${Math.round(bytes / 1024)} KB`;
  return `${(bytes / 1024 / 1024).toFixed(1)} MB`;
}

const timeFmt = new Intl.DateTimeFormat('en-IN', { hour: '2-digit', minute: '2-digit', hour12: false });
const dateFmt = new Intl.DateTimeFormat('en-IN', { day: 'numeric', month: 'short', year: 'numeric' });

export const clock = (ms) => timeFmt.format(new Date(ms));
export const day = (value) => (value ? dateFmt.format(new Date(value)) : '');

export function ago(ms, now = Date.now()) {
  const min = Math.round((now - ms) / 60000);
  if (min < 1) return 'just now';
  if (min < 60) return `${min} min ago`;
  const hours = Math.floor(min / 60);
  return `${hours} h ${min % 60} min ago`;
}

export function seconds(ms) {
  const s = Math.max(0, Math.floor(ms / 1000));
  return s < 60 ? `${s} s` : `${Math.floor(s / 60)} min ${s % 60} s`;
}

/** Amazon issues can name raw template keys like 'purchasable_offer#1.our_price…'; show them readably. */
export function fieldLabel(field) {
  if (!field) return '';
  if (!/[#_]/.test(field) || /\s/.test(field)) return field;
  const base = field.split(/[#[]/)[0].replace(/^:+/, '').replace(/_/g, ' ');
  return base.charAt(0).toUpperCase() + base.slice(1);
}
