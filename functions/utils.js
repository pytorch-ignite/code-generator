// Below imports are defined in
// `external_node_modules` of [functions] in netlify.toml
// They are required for this function to run

import { Octokit } from '@octokit/core'

/**
 * Create a file on GitHub with Octokit.
 * @param {string} content
 * @param {string} filename
 * @param {string} nbUid
 * @param {string} repoOwner
 * @param {string} repo
 * @returns download_url
 */
export async function pushToGitHub(content, filename, nbUid, repoOwner, repo) {
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
