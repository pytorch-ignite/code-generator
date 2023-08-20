// Below imports are defined in
// `external_node_modules` of [functions] in netlify.toml
// They are required for this function to run

import { Octokit } from '@octokit/core'
import JSZip from 'jszip'
import { v5 as uuidv5 } from 'uuid'

const repoOwner = process.env.VUE_APP_GH_USER
const repo = process.env.VUE_APP_GH_REPO

/**
 * Create a file on GitHub with Octokit.
 * @param {string} content
 * @param {string} filename
 * @param {string} nbUid
 * @param {string} repoOwner
 * @param {string} repo
 * @returns download_url
 */
export async function pushToGitHub(content, filename, nbUid) {
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

// This function is the one Netlify function runs on
// https://docs.netlify.com/functions/build-with-javascript/#synchronous-function-format
export async function getZip_Uid(data) {
  const zip = new JSZip()
  const code = data.code
  let hash = ''
  const template = `ignite-${data.template}`

  // As usual from Download component,
  // we will zip the files and
  // generate a base64 format for pushing to GitHub
  // with Octokit.
  // we generate a hash for unique code identification and
  // zip generation
  for (const filename in code) {
    hash += code[filename]
    zip.file(filename, code[filename])
  }
  const nbUid = uuidv5(hash, uuidv5.URL)
  const content = await zip.generateAsync({ type: 'base64' })
  const zipRes = await pushToGitHub(content, `${template}.zip`, nbUid)
  return {
    zipRes: zipRes,
    nbUid: nbUid
  }
}
