import { v4 as uuidv4 } from 'uuid'
import { Octokit } from 'https://cdn.skypack.dev/@octokit/core'
import JSZip from 'jszip'

const nbUid = uuidv4()
const nbName = 'pytorch-ignite-notebook.ipynb'
const repoOwner = process.env.VUE_APP_GH_USER
const repo = process.env.VUE_APP_GH_REPO

async function createOnGitHub(nbJSON) {
  const octokit = new Octokit({
    auth: process.env.VUE_APP_GH_TOKEN
  })
  const response = await octokit.request(
    'PUT /repos/{owner}/{repo}/contents/{path}',
    {
      owner: repoOwner,
      repo: repo,
      path: `nbs/${nbUid}/${nbName}`,
      message: `nb: add ${nbUid}`,
      content: btoa(unescape(encodeURIComponent(nbJSON)))
    }
  )
  return response
}

exports.handler = async (event, context) => {
  const data = JSON.parse(event.body)
  const zip = new JSZip()

  for (const filename in data) {
    zip.file(filename, data[filename])
  }
  const content = await zip.generateAsync({ type: 'string' })
  const zipRes = await createOnGitHub(content)
  await createOnGitHub(`wget ${zipRes}`)

  const colabLink = `https://colab.research.google.com/github/${repoOwner}/${repo}/blob/main/nbs/${nbUid}/${nbName}`
  return {
    statusCode: 200,
    body: JSON.stringify({ link: colabLink })
  }
}
