import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src')
    }
  },
  // 生产环境：不使用代理，通过后端CORS处理跨域
  server: {
    port: 3000,
    host: true
  },
  build: {
    outDir: 'dist',
    sourcemap: false,
    assetsDir: 'assets',
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['vue', 'vue-router', 'pinia', 'element-plus'],
          utils: ['axios']
        }
      }
    }
  },
  // 定义API基础URL，可通过环境变量覆盖
  define: {
    __APP_API_URL__: JSON.stringify(
      process.env.VITE_API_URL || 
      'https://api.hengseen.com/api/v1'
    )
  }
})
