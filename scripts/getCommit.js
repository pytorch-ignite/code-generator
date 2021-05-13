// @ts-check

const { exec } = require('child_process')
const fs = require('fs')

exec('git rev-parse HEAD', (err, stdout, stderr) => {
  if (err) {
    console.error(err)
  }
  console.log('> git commit from git    ', stdout)
  console.log('> git commit from netlify', process.env.COMMIT_REF)
  fs.writeFileSync('./.env.local', `VITE_COMMIT=${stdout}`)
})
