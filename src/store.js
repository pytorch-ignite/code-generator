// central store for user input configs and generated codes
import { reactive, watchEffect } from 'vue'
import ejs from 'ejs'

import readme from './templates/README.md?raw'
import requirements from './templates/requirements.txt?raw'
import utils from './templates/utils.py?raw'
import configJSON from './templates/config.json'
import utilsJSON from './metadata/utils.json'

// Vision Classification Template
import vClassData from './templates/template-vision-classification/data.py?raw'
import vClassMain from './templates/template-vision-classification/main.py?raw'
import vClassModel from './templates/template-vision-classification/model.py?raw'
import vClassTrainers from './templates/template-vision-classification/trainers.py?raw'

// ejs options
ejs.localsName = 'it'

const visionClassiModules = {
  'data.py': vClassData,
  'main.py': vClassMain,
  'model.py': vClassModel,
  'trainers.py': vClassTrainers,
  'utils.py': utils
}

const visionDetectModules = {
  'data.py': 'a',
  'main.py': 'b',
  'transforms.py': 'c'
}

const templates = {
  'Vision Classification': visionClassiModules,
  'Vision Detection': visionDetectModules
}

export const store = reactive({
  code: {},
  config: configJSON,
  _config: {}
})

export function saveConfig(key, value) {
  if (store.config[key] === undefined || store.config[key] !== value) {
    store.config[key] = value
  }
}

export function getTemplateFileNames() {
  const files = ['README.md', 'config.json']
  files.push(...Object.keys(templates[store.config.template]))
  files.push('requirements.txt')
  return files
}

export function genCode() {
  const currentTemplate = templates[store.config.template]

  // render all files from template
  for (const path in currentTemplate) {
    store.code[path] = ejs.render(currentTemplate[path], store.config).replaceAll(
      /(\s+)\#(\s)/gi,
      '\n'
    )
  }
  store.code['main.py'] = genMain()
  store.code['trainers.py'] = genTrainers()
  store.code['README.md'] = ejs.render(readme, store.config)
  store.code['config.json'] = JSON.stringify(store.config, null, 2)
  store.code['requirements.txt'] = requirements
}

watchEffect(() => genCode())

function genMain() {
  let tempCode = store.code['main.py']
  const { to_save } = utilsJSON
  let toSaveTrain = ''
  // to_save from utils.json
  let save = []
  for (const o in to_save.options) {
    const isTrue = store.config[to_save.options[o].name]
    if (isTrue) {
      save.push(isTrue)
      toSaveTrain += `'${o}': ${o}, `
    }
  }
  if (save.every((value) => value === true) && save.length > 0) {
    tempCode = tempCode.replaceAll('None', `{${toSaveTrain}}`)
  }

  return tempCode
}

function genTrainers() {
  let tempCode = store.code['trainers.py']

  if (store.config['deterministic']) {
    tempCode = tempCode.replaceAll('Engine', 'DeterministicEngine')
  }
  return tempCode
}

function splitCode(rawCode) {
  const arrCode = rawCode
    .split('### ')
    .slice(1)
    .map((value) => value.split(' ###'))
  return Object.fromEntries(arrCode)
}
