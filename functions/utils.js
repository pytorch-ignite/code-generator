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
  const template = `ignite-${data.template}`

  // As usual from Download component,
  // we will zip the files and
  // generate a base64 format for pushing to GitHub
  // with Octokit.
  for (const filename in code) {
    zip.file(filename, code[filename])
  }
  // since the generated zip varies every time even with the same code
  // it can't be used to generate a UUID
  const content = await zip.generateAsync({ type: 'base64' })
  // we generate an unique id form the current config for pushing to github
  const nbUid = uuidv5(JSON.stringify(data.config), uuidv5.URL)
  const zipRes = await pushToGitHub(content, `${template}.zip`, nbUid)
  return {
    zipRes: zipRes,
    nbUid: nbUid
  }
}
