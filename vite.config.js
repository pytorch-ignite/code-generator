// @ts-check
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { execSync } from 'child_process'

const commit = execSync('git rev-parse HEAD', { encoding: 'utf-8' })

console.log('> git commit from git    ', commit)
console.log('> git commit from netlify', process.env.COMMIT_REF)

export default defineConfig({
  plugins: [vue()],
  // define global CONSTANTS variable https://vitejs.dev/config/#define
  define: {
    __COMMIT__: JSON.stringify(commit)
  }
})
