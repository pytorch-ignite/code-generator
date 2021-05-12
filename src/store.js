// central store for user input configs and generated codes
import { reactive, watchEffect } from 'vue'
import ejs from 'ejs'

import templates from './templates/templates.json'

// get env variables for template fetching
const isProd = import.meta.env.PROD
const isDev = import.meta.env.DEV
const gitCommit = import.meta.env.VITE_GIT_COMMIT

// set url for template fetching
// this only works in production and local mode
// not in network mode
const templatesURL = 'src/templates'
const localhostURL = `http://localhost:3000/${templatesURL}`
const rawGitURL = `https://raw.githubusercontent.com/pytorch-ignite/code-generator/${gitCommit}/${templatesURL}`
const url = isDev ? localhostURL : isProd ? rawGitURL : null

// ejs options
ejs.localsName = 'it'
ejs.delimiter = '@'
ejs.openDelimiter = '#'
ejs.closeDelimiter = '#'

export const store = reactive({
  code: {},
  config: {
    template: 'template-vision-classification'
  }
})

export function saveConfig(key, value) {
  if (store.config[key] === undefined || store.config[key] !== value) {
    store.config[key] = value
  }
  store.config[key] = value
}

export function getTemplateFileNames() {
  const files = []
  files.push(...Object.keys(templates[store.config.template]))
  // files.push('requirements.txt')
  return files
}

export function genCode() {}

export async function fetchTemplates(template) {
  for (const filename in templates[template]) {
    const res = await fetch(`${url}/${template}/${filename}`)
    store.code[filename] = await res.text()
  }
}

watchEffect(() => genCode())
