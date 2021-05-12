// @ts-check

const { exec } = require('child_process')
const fs = require('fs')

exec('git rev-parse HEAD', (err, stdout, stderr) => {
  if (err) {
    console.error(err)
  }
  console.log(stdout)
  fs.writeFileSync('./.env', `VITE_GIT_COMMIT=${stdout}`)
})
