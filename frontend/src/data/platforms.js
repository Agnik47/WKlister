// What each output file is. Names match the "platforms" list returned by /generate.
export const PLATFORMS = [
  {
    key: 'meesho',
    name: 'Meesho',
    ext: '.xlsx',
    color: 'var(--meesho)',
    about: 'Listed under the Silver Kraft brand. Designs are grouped as Group 01–30; a new file starts after 30 groups.',
  },
  {
    key: 'flipkart',
    name: 'Flipkart',
    ext: '.xls',
    color: 'var(--flipkart)',
    about: 'Flipkart’s old Excel format, written with LibreOffice on the main PC. One row per size.',
  },
  {
    key: 'myntra',
    name: 'Myntra',
    ext: '.xlsx',
    color: 'var(--myntra)',
    about: 'One style group per colour and MRP. Article names are cut to 40 characters.',
  },
  {
    key: 'amazon',
    name: 'Amazon',
    ext: '.xlsm',
    color: 'var(--amazon)',
    about: 'Amazon’s new template. One parent row per design, then one row per size.',
  },
];

export const ISSUE_SOURCES = {
  'Master sheet': 'var(--master)',
  ...Object.fromEntries(PLATFORMS.map((p) => [p.name, p.color])),
};

export const sourceColor = (name) => ISSUE_SOURCES[name] || 'var(--muted)';
export const platformByName = (name) => PLATFORMS.find((p) => p.name === name);
