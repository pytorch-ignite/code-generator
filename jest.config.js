/** @type {import('@jest/types').Config.InitialOptions} */
const config = {
  verbose: true,
  testTimeout: process.env.CI ? 30000 : 10000
}

module.exports = config
