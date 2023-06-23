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
const urlDev = `${location.origin}/${urlTemplates}`
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
  color: 'red'
})

// main reactive object
// store.code - the final rendered code to be included in archive
// store.config - the internal config to track user input
export const store = reactive({
  code: {},
  config: {
    template: '',
    include_test: false,
    output_dir: './logs',
    log_every_iters: 10
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

// merges the code from the common and specific files using ejs
function mergeCode(specificFileText, commonFileText) {
  const replaced = specificFileText.replace(
    /#::= from_template_common ::#/g,
    commonFileText
  )
  return replaced
}

// render the code if there are fetched files for current selected template
export function genCode() {
  const currentFiles = files[store.config.template]
  store.code = {} // empty the `store.code` after changing templates
  if (currentFiles && Object.keys(currentFiles).length) {
    for (const file in currentFiles) {
      if (!store.config.include_test && file === 'test_all.py') {
        delete store.code['test_all.py']
        continue
      }
      store.code[file] = ejs
        .render(
          // replace `\s(s) or \n(s)#:::\s`
          // with `#::: `
          currentFiles[file].replace(/([\s\n]+#:::\s)/gi, '#::: '),
          store.config
        )
        // trim `    #`
        .replace(/\s{4}#$/gim, '')
        .replace(/  # usort: skip/g, '')
    }
    if (isDev) {
      store.code[__DEV_CONFIG_FILE__] =
        '# THIS FILE APPEARS ONLY IN DEV MODE\n' +
        JSON.stringify(store.config, null, 2)
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
    files[template] = {}
    for (const filename of templates[template]) {
      const response = await fetch(`${url}/${template}/${filename}`)
      const text_specific = await response.text()
      // Dynamically fetch the common templates-code, if the file exists in common,
      // then render the replace_here code tag using ejs template
      // If the file doesn't exist in common, then it will fetch an empty string
      // then the code tag is replaced with empty string
      const res_common = await fetch(`${url}/template-common/${filename}`)
      const text_common = await res_common.text()
      files[template][filename] = mergeCode(text_specific, text_common)
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
// same as watch(() => store.config, () => genCode(), { deep: true })
watch(store.config, () => genCode())

// ejs options
ejs.localsName = 'it'
ejs.delimiter = ':::'
ejs.openDelimiter = '#'
ejs.closeDelimiter = '#'
