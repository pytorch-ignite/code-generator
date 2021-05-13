// @ts-check
// central store for user input configs and generated codes
import { reactive, watch } from 'vue'
import ejs from 'ejs'

import templates from './templates/templates.json'

// get env variables for template fetching
// @ts-ignore
const isProd = import.meta.env.PROD
// @ts-ignore
const isDev = import.meta.env.DEV
// @ts-ignore
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
ejs.delimiter = ':::'
ejs.openDelimiter = '#'
ejs.closeDelimiter = '#'

export let files = {}
export const store = reactive({
  code: {},
  config: {}
})

export function saveConfig(key, value) {
  if (store.config[key] === undefined || store.config[key] !== value) {
    store.config[key] = value
  }
}

export async function genCode() {
  console.log('watch effect')
  if (files && Object.keys(files).length) {
    for (const file in files) {
      // console.log(file)
      store.code[file] = ejs.render(files[file], store.config)
    }
  }
}

export async function fetchTemplates(template) {
  for (const filename in templates[template]) {
    const res = await fetch(`${url}/${template}/${filename}`)
    const text = await res.text()
    files[filename] = text
  }
  console.log('after fetch')
  genCode()
}

watch(store.config, () => genCode())
