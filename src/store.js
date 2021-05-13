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

// to store all fetch template files
let files = {}

// main reactive object
// store.code - the final rendered code to be included in archive
// store.config - the internal config to track user input
export const store = reactive({
  code: {},
  config: {
    template: ''
  }
})

/**
 * @param {string} key
 * @param {string | number | boolean | null} value
 */
// save config if the value changes or
// if the key is not saved before
export function saveConfig(key, value) {
  if (store.config[key] === undefined || store.config[key] !== value) {
    store.config[key] = value
  }
}

// render the code
export async function genCode() {
  console.log('watch effect')
  const currentFiles = files[store.config.template]
  if (currentFiles && Object.keys(currentFiles).length) {
    for (const file in currentFiles) {
      store.code[file] = ejs.render(files[file], store.config)
    }
  }
}

/**
 * @param {string} template
 */
// fetch the templates
// save them in the files[template]
export async function fetchTemplates(template) {
  // fetch the template if there is no fetch of template before
  if (files[template] === undefined) {
    for (const filename in templates[template]) {
      const response = await fetch(`${url}/${template}/${filename}`)
      files[template][filename] = await response.text()
    }

    // calling genCode explicitly here
    // since fetch templates is running asynchronously
    // so that rendered code will show up
    // after choosing the template
    genCode()
  }
}

// watch the store.config
// if that changed, call the genCode function
watch(store.config, () => genCode())
