import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { resolve } from 'path';

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: '../assets',
    emptyOutDir: true,
    rollupOptions: {
      input: {
        'news-list': resolve(__dirname, 'src/NewsListWidget.tsx'),
        'news-search': resolve(__dirname, 'src/NewsSearchWidget.tsx'),
      },
      output: {
        entryFileNames: '[name].js',
        chunkFileNames: '[name]-[hash].js',
        assetFileNames: (assetInfo) => {
          if (assetInfo.name?.endsWith('.css')) {
            return '[name].css';
          }
          return '[name]-[hash][extname]';
        },
      },
    },
  },
  server: {
    port: 5173,
    cors: true,
  },
  preview: {
    port: 4444,
    cors: true,
  },
});
