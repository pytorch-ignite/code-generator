import { pushToGitHub, getZip_Uid, getNbCells } from './utils'

const repoOwner = process.env.VUE_APP_GH_USER
const repo = process.env.VUE_APP_GH_REPO

// This function is the one Netlify function runs on
// https://docs.netlify.com/functions/build-with-javascript/#synchronous-function-format
exports.handler = async function (event, _) {
  // event is a JSON object
  const data = JSON.parse(event.body)
  const template = `ignite-${data.template}`
  const nbName = `${template}.ipynb`
  let { zipRes, nbUid } = await getZip_Uid(data)

  const isPRBuild = process.env.PR_BUILD === 'true'
  const commit = data.commit.substring(0,15)

  // To check if PR_Build = true and then add commit hash
  if (isPRBuild) {
    nbUid = nbUid + '-' + commit
  }

  const argparser = data.argparser
  const title = template
    .replace('ignite-', '')
    .split('-')
    .map((v) => v[0].toUpperCase() + v.slice(1))
    .join(' ')

  // get notebook cell structure
  const nb = getNbCells(title, zipRes, argparser, template)

  // Create the notebook on GitHub
  await pushToGitHub(
    Buffer.from(JSON.stringify(nb)).toString('base64'),
    nbName,
    nbUid
  )

  const colabLink = `https://colab.research.google.com/github/${repoOwner}/${repo}/blob/main/nbs/${nbUid}/${nbName}`
  return {
    statusCode: 200,
    body: colabLink
  }
}
