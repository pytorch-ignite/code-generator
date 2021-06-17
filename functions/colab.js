// Below imports are defined in
// `external_node_modules` of [functions] in netlify.toml
// They are required for this function to run

import { v4 as uuidv4 } from 'uuid'
import { Octokit } from '@octokit/core'
import JSZip from 'jszip'

const nbUid = uuidv4()
const nbName = 'pytorch-ignite-notebook.ipynb'
const repoOwner = process.env.VUE_APP_GH_USER
const repo = process.env.VUE_APP_GH_REPO

/**
 * Create a file on GitHub with Octokit.
 * @param {string} content
 * @param {string} filename
 * @returns download_url
 */
async function pushToGitHub(content, filename) {
  const octokit = new Octokit({
    auth: process.env.VUE_APP_GH_TOKEN
  })
  try {
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
    // the download url is raw url - https://raw.githubusercontent.com/...
    return res.data.content.download_url
  } catch (e) {
    console.error(e)
  }
}

// This function is the one Netlify function runs on
// https://docs.netlify.com/functions/build-with-javascript/#synchronous-function-format
export async function handler(event, _) {
  // event is a JSON object
  const data = JSON.parse(event.body)
  const zip = new JSZip()

  // As usual from Download component,
  // we will zip the files and
  // generate a base64 format for pushing to GitHub
  // with Octokit.
  for (const filename in data) {
    zip.file(filename, data[filename])
  }
  const content = await zip.generateAsync({ type: 'base64' })
  const zipRes = await pushToGitHub(content, 'pytorch-ignite-notebook.zip')

  // notebook cell structure
  const nb = {
    nbformat: 4,
    nbformat_minor: 0,
    metadata: {
      kernelspec: {
        display_name: 'Python 3',
        name: 'python3'
      }
    },
    cells: [
      {
        cell_type: 'code',
        metadata: {},
        execution_count: null,
        outputs: [],
        source: [
          `!wget ${zipRes}\n`,
          '!unzip pytorch-ignite-notebook.zip\n',
          '!pip install -r requirements.txt\n',
          '!python main.py\n'
        ]
      }
    ]
  }
  // Create the notebook on GitHub
  await pushToGitHub(Buffer.from(JSON.stringify(nb)).toString('base64'), nbName)

  const colabLink = `https://colab.research.google.com/github/${repoOwner}/${repo}/blob/main/nbs/${nbUid}/${nbName}`
  return {
    statusCode: 200,
    body: colabLink
  }
}
