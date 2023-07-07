// Below imports are defined in
// `external_node_modules` of [functions] in netlify.toml
// They are required for this function to run

import { v4 as uuidv4 } from 'uuid'
import JSZip from 'jszip'
import { pushToGitHub } from './utils'

const nbUid = uuidv4()
const repoOwner = process.env.VUE_APP_GH_USER
const repo = process.env.VUE_APP_GH_REPO

// This function is the one Netlify function runs on
// https://docs.netlify.com/functions/build-with-javascript/#synchronous-function-format
exports.handler = async function (event, _) {
  // event is a JSON object
  const data = JSON.parse(event.body)
  const zip = new JSZip()
  const code = data.code
  const template = `ignite-${data.template}`
  const nbName = `${template}.ipynb`

  // As usual from Download component,
  // we will zip the files and
  // generate a base64 format for pushing to GitHub
  // with Octokit.
  for (const filename in code) {
    zip.file(filename, code[filename])
  }
  const content = await zip.generateAsync({ type: 'base64' })
  const zipRes = await pushToGitHub(
    content,
    `${template}.zip`,
    nbUid,
    repoOwner,
    repo
  )

  const title = template
    .replace('ignite-', '')
    .split('-')
    .map((v) => v[0].toUpperCase() + v.slice(1))
    .join(' ')
  // notebook cell structure
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
    cells: [
      {
        cell_type: 'markdown',
        metadata: {},
        execution_count: null,
        outputs: [],
        source: [
          `# ${title} by PyTorch-Ignite Code-Generator\n\n`,
          'Please, run the cell below to execute your code.'
        ]
      },
      {
        cell_type: 'code',
        metadata: {},
        execution_count: null,
        outputs: [],
        source: [
          `!wget ${zipRes}\n`,
          `!unzip ${template}.zip\n`,
          '!pip install -r requirements.txt\n',
          '!python main.py config.yaml\n'
        ]
      }
    ]
  }
  // Create the notebook on GitHub
  await pushToGitHub(
    Buffer.from(JSON.stringify(nb)).toString('base64'),
    nbName,
    nbUid,
    repoOwner,
    repo
  )

  const colabLink = `https://colab.research.google.com/github/${repoOwner}/${repo}/blob/main/nbs/${nbUid}/${nbName}`
  return {
    statusCode: 200,
    body: colabLink
  }
}
