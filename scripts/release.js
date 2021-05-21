// @ts-check
// largely stripped from https://github.com/vuejs/vitepress/blob/master/scripts/release.js

const fs = require('fs')
const path = require('path')
const execa = require('execa')
const semver = require('semver')
const prompts = require('prompts')

const pkgDir = process.cwd()
const pkgPath = path.resolve(pkgDir, 'package.json')
const pkg = require(pkgPath)
const currentVersion = pkg.version

const preId = process.argv.slice(2)[0]

/**
 * @type {import('semver').ReleaseType[]}
 */
const versionIncrements = [
  'patch',
  'minor',
  'major',
  'prepatch',
  'preminor',
  'premajor',
  'prerelease'
]

/**
 * @param {import('semver').ReleaseType} i
 */
const inc = (i) => semver.inc(currentVersion, i, preId)

/**
 * @param {string} bin
 * @param {string[]} args
 * @param {object} opts
 */
const run = (bin, args, opts = {}) =>
  execa(bin, args, { stdio: 'inherit', ...opts })

/**
 * @param {string} msg
 */
const step = (msg) => console.log('\x1b[36m%s\x1b[0m', msg)

async function main() {
  /**
   * @type {{ release: string }}
   */
  const { release: targetVersion } = await prompts({
    type: 'select',
    name: 'release',
    message: 'Select release type',
    choices: versionIncrements.map((i) => {
      return { title: `${i} (${inc(i)})`, value: inc(i) }
    })
  })

  if (!semver.valid(targetVersion)) {
    throw new Error(`Invalid target version: ${targetVersion}`)
  }

  const tag = `v${targetVersion}`

  /**
   * @type {{ yes: boolean }}
   */
  const { yes } = await prompts({
    type: 'confirm',
    name: 'yes',
    message: `Releasing ${tag}. Confirm?`
  })

  if (!yes) {
    return
  }

  step('\nUpdating package version...')
  updateVersion(targetVersion)

  step('\nGenerating changelog...')
  await run('pnpm', ['run', 'changelog'])
  await run('pnpm', ['run', 'fmt'])

  const { yes: changelogOk } = await prompts({
    type: 'confirm',
    name: 'yes',
    message: '\nChangelog generated. Does it look good?'
  })

  if (!changelogOk) {
    return
  }

  step('\nCommitting changes...')
  await run('git', ['add', '-A'])
  await run('git', ['commit', '-m', `release: ${tag}`])

  step('\nPushing to GitHub...')
  await run('git', ['tag', tag])
  await run('git', ['push', 'origin', tag])
  await run('git', ['push', '-u', 'origin', 'main'])
}

/**
 * @param {string} version
 */
function updateVersion(version) {
  const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf-8'))
  pkg.version = version
  fs.writeFileSync(pkgPath, JSON.stringify(pkg, null, 2) + '\n')
}

main().catch((err) => console.error(err))
