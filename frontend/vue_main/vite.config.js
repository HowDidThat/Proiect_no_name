import { fileURLToPath } from 'url'
import { mergeConfig, defineConfig } from 'vite'
import { configDefaults, defineConfig as defineVitestConfig } from 'vitest/config'
import vuePlugin from '@vitejs/plugin-vue'

export default mergeConfig(
  defineConfig({
    plugins: [vuePlugin()],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url))
      }
    }
  }),
  defineVitestConfig({
    test: {
      globals: true,
      environment: 'jsdom',
      root: fileURLToPath(new URL('./', import.meta.url)),
      setupFiles: ['./vitest.setup.js'],
      coverage: {
        provider: 'v8',
        reporter: ['text', 'json', 'html'],
        reportsDirectory: './coverage',
        exclude: [
          'node_modules/',
          'src/main.js',
          'src/App.vue',
          '**/*.config.js',
          '**/*.d.ts',
          'src/components/',
          'src/router.js',
          'src/utils/old_code.js'
        ]
      }
    }
  })
)