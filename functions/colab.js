import { pushToGitHub, getZip_Uid } from './utils'

const repoOwner = process.env.VUE_APP_GH_USER
const repo = process.env.VUE_APP_GH_REPO

// This function is the one Netlify function runs on
// https://docs.netlify.com/functions/build-with-javascript/#synchronous-function-format
exports.handler = async function (event, _) {
  // event is a JSON object
  const data = JSON.parse(event.body)
  const template = `ignite-${data.template}`
  const nbName = `${template}.ipynb`
  const { zipRes, nbUid } = await getZip_Uid(data)

  const title = template
    .replace('ignite-', '')
    .split('-')
    .map((v) => v[0].toUpperCase() + v.slice(1))
    .join(' ')
  // notebook cell structure

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

  const common_nb_commands = [
    `!wget ${zipRes}\n`,
    `!unzip ${template}.zip\n`,
    '!pip install -r requirements.txt'
  ]

  let argparser = data.argparser
  let execution_nb_commands = []

  if (argparser == 'hydra') {
    execution_nb_commands.push('!python main.py')
  } else {
    execution_nb_commands.push('!python main.py config.yaml')
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
