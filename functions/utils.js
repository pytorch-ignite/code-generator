// Below imports are defined in
// `external_node_modules` of [functions] in netlify.toml
// They are required for this function to run

import { Octokit } from '@octokit/core'
import JSZip from 'jszip'
import { v5 as uuidv5 } from 'uuid'
import { commit } from '../src/store'

const repoOwner = process.env.VUE_APP_GH_USER
const repo = process.env.VUE_APP_GH_REPO
const isPRBuild = process.env.PR_BUILD === 'true'

/**
 * Create a file on GitHub with Octokit.
 * @param {string} content
 * @param {string} filename
 * @param {string} nbUid
 * @returns download_url
 */
export async function pushToGitHub(content, filename, nbUid) {
  const octokit = new Octokit({
    auth: process.env.VUE_APP_GH_TOKEN
  })
  try {
    try {
      // first try the GET request to check if the zip/ipynb already exists
      // if it already exists, then return the same url
      const res = await octokit.request(
        'GET /repos/{owner}/{repo}/contents/{path}',
        {
          owner: repoOwner,
          repo: repo,
          path: `nbs/${nbUid}/${filename}`
        }
      )
      return res.data.download_url
    } catch (err) {
      // if the url doesn't exist, then create a new url for that specific nbUid
      // push to github and return the download url
      if (err.status == '404') {
        const res = await octokit.request(
          'PUT /repos/{owner}/{repo}/contents/{path}',
          {
            owner: repoOwner,
            repo: repo,
            path: `nbs/${nbUid}/${filename}`,
            message: `nb: add ${nbUid}`,
            content: content
          }
        )
        return res.data.content.download_url
      } else {
        console.error(err)
      }
    }
  } catch (e) {
    console.error(e)
  }
}

/**
 * Create a file on GitHub with Octokit.
 * @param {JSON} data
 * @returns zipRes, nbUid
 */
// This function is the one Netlify function runs on
// https://docs.netlify.com/functions/build-with-javascript/#synchronous-function-format
export async function getZip_Uid(data) {
  const zip = new JSZip()
  const code = data.code
  const template = `ignite-${data.template}`
  let fullCode = ''

  // As usual from Download component,
  // we will zip the files and
  // generate a base64 format for pushing to GitHub
  // with Octokit.
  for (const filename in code) {
    fullCode += code[filename]
    zip.file(filename, code[filename])
  }
  // since the generated zip varies every time even with the same code
  // it can't be used to generate a UUID
  const content = await zip.generateAsync({ type: 'base64' })
  // we generate an unique id from the current config for pushing to github
  let nbUid = uuidv5(fullCode, uuidv5.URL)
  // To check if PR_Build = true and then add commit hash
  if (isPRBuild) {
    nbUid = nbUid + '-' + commit
  }
  const zipRes = await pushToGitHub(content, `${template}.zip`, nbUid)
  return {
    zipRes: zipRes,
    nbUid: nbUid
  }
}

/**
 * Extracts the root URL from a given URL, excluding trailing slashes.
 * @param {string} url
 * @returns {string} rootUrl
 */
export function getRootUrlWithoutTrailingSlash(url) {
  // Use the URL constructor to parse the input URL
  const parsedUrl = new URL(url)
  // Get the origin (root) part of the URL without a trailing slash
  const rootUrl = parsedUrl.origin.toString()

  return rootUrl
}

/**
 * Get the correct formatted notebook for Colab and Nebari functions
 * @param {string} title
 * @param {string} zipRes
 * @param {string} argparser
 * @param {string} template
 * @param {boolean} nebari
 * @returns {JSON} nb
 */
export function getNbCells(title, zipRes, argparser, template, nebari = false) {
  function create_nb_cell(source_array, cell_type) {
    return {
      cell_type: cell_type,
      metadata: {},
      execution_count: null,
      outputs: [],
      source: source_array
    }
  }

  let specific_commands = []

  if (title === 'Template Vision Segmentation') {
    specific_commands.push(
      '!python -c "from data import download_datasets; download_datasets(\'./\')"'
    )
  }

  const md_cell = [
    `# ${title} by PyTorch-Ignite Code-Generator\n\n`,
    'Please, run the cell below to execute your code.'
  ]

  let common_nb_commands = [
    `!wget ${zipRes}\n`,
    `!unzip ${template}.zip\n`,
    '!pip install -r requirements.txt'
  ]

  let execution_nb_commands = [
    `!python main.py ${
      argparser === 'hydra'
        ? '#--config-dir=/content/ --config-name=config.yaml'
        : 'config.yaml'
    }`
  ]

  // To have seperate folder in Nebari server for downloading and executing files
  if (nebari) {
    common_nb_commands = [
      'cur_dir = !mkdir pytorch-ignite-template-`date "+%Y%m%d-%H%M%S"` && cd $_ && echo $PWD\n',
      `%cd {cur_dir[0]}\n`,
      ...common_nb_commands
    ]
    execution_nb_commands = [`%cd {cur_dir[0]}\n`, ...execution_nb_commands]
  }

  let nb_cells = [
    create_nb_cell(md_cell, 'markdown'),
    create_nb_cell(common_nb_commands, 'code')
  ]
  if (specific_commands.length > 0) {
    nb_cells.push(create_nb_cell(specific_commands, 'code'))
  }
  nb_cells.push(create_nb_cell(execution_nb_commands, 'code'))

  const nb = {
    nbformat: 4,
    nbformat_minor: 0,
    metadata: {
      kernelspec: {
        display_name: 'Python 3',
        name: 'python3'
      },
      accelerator: 'GPU'
    },
    cells: nb_cells
  }
  return nb
}
