import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    proxy: {
      '/api': {
        // target: 'http://101.42.20.174:4000',
        // target: 'http://123.56.222.120:8000',
        target: 'http://localhost:4000',
        changeOrigin: true,
        ws: true
      }
    }
  }
})
