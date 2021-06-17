import { v4 as uuidv4 } from 'uuid'
import { Octokit } from '@octokit/core'
import JSZip from 'jszip'

const nbUid = uuidv4()
const nbName = 'pytorch-ignite-notebook.ipynb'
const repoOwner = process.env.VUE_APP_GH_USER
const repo = process.env.VUE_APP_GH_REPO

async function createOnGitHub(content, filename) {
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
    return res.data.content.download_url
  } catch (e) {
    console.error(e)
  }
}

export async function handler(event, context) {
  const data = JSON.parse(event.body)
  const zip = new JSZip()

  for (const filename in data) {
    zip.file(filename, data[filename])
  }
  const content = await zip.generateAsync({ type: 'base64' })
  const zipRes = await createOnGitHub(content, 'pytorch-ignite-notebook.zip')
  await createOnGitHub(
    Buffer.from(`curl ${zipRes.replace('blob', 'raw')}`).toString('base64'),
    nbName
  )

  const colabLink = `https://colab.research.google.com/github/${repoOwner}/${repo}/blob/main/nbs/${nbUid}/${nbName}`
  return {
    statusCode: 200,
    body: JSON.stringify({ link: colabLink })
  }
}
