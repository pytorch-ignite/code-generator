import { reactive, watchEffect } from 'vue'
import datasets from './templates/datasets.py?raw'
import main from './templates/main.py?raw'
import models from './templates/models.py?raw'
import readme from './templates/README.md?raw'
import requirements from './templates/requirements.txt?raw'
import trainers from './templates/trainers.py?raw'
import utilsPy from './templates/utils.py?raw'
import utilsJSON from './metadata/utils.json'
import configJSON from './templates/config.json'

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
  return [
    'README.md',
    'config.json',
    'datasets.py',
    'main.py',
    'models.py',
    'trainers.py',
    'utils.py',
    'requirements.txt'
  ]
}

export function generateCode(currentTab) {
  const fileNames = getTemplateFileNames()
  const generateFnArray = [
    generateReadme,
    generateConfig,
    generateDatasets,
    generateMain,
    generateModels,
    generateTrainers,
    generateUtils,
    generateRequirements
  ]

  const index = fileNames.findIndex((value) => value === currentTab)
  return generateFnArray[index]().trim()
}

watchEffect(() => {
  for (const filename of getTemplateFileNames()) {
    generateCode(filename)
  }
})

function generateConfig() {
  // model tab
  const subDomains = ['vision', 'text', 'audio']
  let validSubDomain
  const found = subDomains.some((value) => {
    validSubDomain = value
    return Object.keys(store._config).includes(value)
  })
  if (found) {
    const modelObj = store._config[validSubDomain]
    const key = Object.keys(modelObj)
    store.config['model'] = modelObj[key[0]]
  }
  // for (const key of ['filename_prefix', 'dirname', 'n_saved']) {
  //   store.config[key] = store._config[key]
  // }
  store.code['config.json'] = JSON.stringify(store.config, null, 2)
  return store.code['config.json']
}

function generateDatasets() {
  store.code['datasets.py'] = datasets.trim()
  return store.code['datasets.py']
}

function generateMain() {
  let tempCode = splitCode(main)
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
    tempCode.checkpointing = tempCode.checkpointing.replaceAll('{}', `{ ${toSaveTrain} }`)
  } else {
    delete tempCode.checkpointing
  }

  store.code['main.py'] = Object.values(tempCode).join('#').trim()
  return store.code['main.py']
}

function generateModels() {
  let tempCode = splitCode(models)
  const domain = store.config.domain
  const subdomain = store.config.subdomain
  const model = store.config.model

  if (domain === 'vision') {
    if (subdomain && subdomain !== 'classification') {
      tempCode.get_model = tempCode.get_model.replaceAll('models.__dict__', `models.${subdomain.toString()}.__dict__`)
    }
  }
  store.code['models.py'] = Object.values(tempCode).join('#').trim()
  return store.code['models.py']
}

function generateReadme() {
  const launch = 'python -m torch.distributed.launch'
  const nproc_per_node = store.config.nproc_per_node
  const nnodes = store.config.nnodes
  const master_addr = store.config.master_addr
  const master_port = store.config.master_port
  let tempReadme = readme
  const cmdRegex = /python.*main.py/gi

  // multi processes
  if (nproc_per_node && nproc_per_node > 1) {
    // single node
    if (nnodes === 1 || !nnodes) {
      tempReadme = readme.replaceAll(
        cmdRegex,
        launch + ` --nproc_per_node ${nproc_per_node} main.py --backend nccl`
      )
    }
    // multi node
    if (nnodes && nnodes > 1) {
      const multinode =
        ` --nproc_per_node ${nproc_per_node}` +
        ` --nnodes ${nnodes}` +
        ` --master_addr ${master_addr}` +
        ` --master_port ${master_port}` +
        ' main.py --backend nccl'

      tempReadme = readme.replaceAll(cmdRegex, launch + multinode)
    }
  }
  store.code['README.md'] = tempReadme.trim()
  return store.code['README.md']
}

function generateRequirements() {
  store.code['requirements.txt'] = requirements.trim()
  return store.code['requirements.txt']
}

function generateTrainers() {
  store.code['trainers.py'] = trainers.trim()
  if (store.config['deterministic']) {
    store.code['trainers.py'] = trainers.replaceAll(
      'Engine',
      'DeterministicEngine'
    )
  }
  return store.code['trainers.py']
}

function generateUtils() {
  let tempCode = splitCode(utilsPy)
  const { to_save } = utilsJSON

  // to_save from utils.json
  let save = []
  for (const o in to_save.options) {
    const isTrue = store.config[to_save.options[o].name]
    if (isTrue) {
      save.push(isTrue)
    }
  }
  if (save.every((value) => value === false) || !save) {
    delete tempCode.checkpointing
  }

  store.code['utils.py'] = Object.values(tempCode).join('#').trim()
  return store.code['utils.py']
}

function splitCode(rawCode) {
  const arrCode = rawCode
    .split('### ')
    .slice(1)
    .map((value) => value.split(' ###'))
  return Object.fromEntries(arrCode)
}
