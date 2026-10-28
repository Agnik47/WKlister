import { defineConfig } from 'vite';

// During `npm run dev` the Python server (app.py) keeps running on port 5050;
// these routes are passed through to it.
const PYTHON_SERVER = 'http://127.0.0.1:5050';

export default defineConfig({
  server: {
    port: 5173,
    proxy: {
      '/api': PYTHON_SERVER,
      '/generate': PYTHON_SERVER,
      '/download': PYTHON_SERVER,
      '/blank-master': PYTHON_SERVER,
    },
  },
  build: {
    outDir: 'dist',
    emptyOutDir: true,
  },
});
