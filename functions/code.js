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
  return {
    statusCode: 200,
    body: zipRes
  }
}
