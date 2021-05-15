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
const commit = __COMMIT__ /* from vite.config.js */

// set url for template fetching
// this only works in production and local mode
// not in network mode
const urlTemplates = 'src/templates'
const urlDev = `${location.href}/${urlTemplates}`
const urlProd = `https://raw.githubusercontent.com/pytorch-ignite/code-generator/${commit}/${urlTemplates}`
const url = isDev ? urlDev : isProd ? urlProd : null

// to store all fetch template files
const files = {}

// filename to store user input config during development
export const __DEV_CONFIG_FILE__ = '__DEV_CONFIG__.json'

// to track message box
export const msg = reactive({
  showMsg: false,
  content: '',
  color: '#ff0000'
})

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

// render the code if there are fetched files for current selected template
export async function genCode() {
  const currentFiles = files[store.config.template]
  if (currentFiles && Object.keys(currentFiles).length) {
    for (const file in currentFiles) {
      store.code[file] = ejs.render(currentFiles[file], store.config)
    }
    const config = JSON.parse(store.code['config.json'])
    store.code['config.json'] = JSON.stringify(
      { ...config, ...store.config },
      null,
      2
    )
  }
  if (isDev) {
    store.code[__DEV_CONFIG_FILE__] = JSON.stringify(store.config, null, 2)
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
    files[template] = {}
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

// ejs options
ejs.localsName = 'it'
ejs.delimiter = ':::'
ejs.openDelimiter = '#'
ejs.closeDelimiter = '#'
