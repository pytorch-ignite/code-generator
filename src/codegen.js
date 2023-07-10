// @ts-check
import ejs from 'ejs'

// merges the code from the common and specific files using ejs
export function mergeCode(specificFileText, commonFileText) {
  const replaced = specificFileText.replace(
    /#::= from_template_common ::#\n/g,
    commonFileText
  )
  return replaced
}

export function renderCode(code, config) {
  //   code = code
  // .replace(/({ :::#[\n\s]+)/gi, '{ :::#')
  // .replace(/([\s\n]+#:::\s}\s:::#)/gi, '#::: } :::#')

  // replace `\s(s) or \n(s)#:::\s`
  // with `#::: `
  code = code.replace(/([\s\n]+#:::\s)/gi, '#::: ')

  return ejs.render(code, config).replace(/  # usort: skip/g, '')
}

// render the code if there are fetched files for current selected template
export function generateFiles(currentFiles, store) {
  for (const file in currentFiles) {
    if (!store.config.include_test && file === 'test_all.py') {
      delete store.code['test_all.py']
      continue
    }
    store.code[file] = renderCode(currentFiles[file], store.config)
  }
}

// ejs options
ejs.localsName = 'it'
ejs.delimiter = ':::'
ejs.openDelimiter = '#'
ejs.closeDelimiter = '#'
