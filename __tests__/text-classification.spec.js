// @ts-check
const { chromium } = require('playwright-chromium')

let browser
let page
let context

beforeAll(async () => {
  browser = await chromium.launch({ headless: true })
})

afterAll(async () => {
  await browser.close()
})

beforeEach(async () => {
  context = await browser.newContext({ acceptDownloads: true })
  page = await context.newPage()
  await page.goto(`http://localhost:5000/create`)
})

afterEach(async () => {
  await page.close()
  await context.close()
})

const parser = ['argparse', 'fire']
for (const name of parser) {
  test(`text-classification simple ${name}`, async () => {
    await page.selectOption('select', 'template-text-classification')

    await page.waitForSelector('text=README.md')

    await page.click('text=Loggers')
    await page.click('text=config.yaml')
    await page.getByText('Training', { exact: true }).click()

    await page
      .getByRole('combobox', {
        name: 'Select the argument parser for training'
      })
      .selectOption(`${name}`)
    // TODO: simplify the downloadPromise calls
    // Here we are trying to wait for 2 seconds before clicking on the `Code` and `Download Zip` button
    const downloadPromise = await page
      .waitForEvent('download', { timeout: 2000 })
      .catch(() => {
        page.getByRole('button', { name: 'Code' }).click()
        page.getByRole('button', { name: 'Download Zip' }).click()
        return page.waitForEvent('download', { timeout: 2000 })
      })
      .catch(() => {
        // these catch calls are required to make sure if CI fails initially then we can have something to rely for further tests
        page.getByRole('button', { name: 'Code' }).click()
        page.getByRole('button', { name: 'Download Zip' }).click()
        return page.waitForEvent('download', { timeout: 2000 })
      })
      .catch(() => {
        page.getByRole('button', { name: 'Code' }).click()
        page.getByRole('button', { name: 'Download Zip' }).click()
        return page.waitForEvent('download', { timeout: 2000 })
      })

    await downloadPromise.saveAs(
      `./dist-tests/text-classification-simple-${name}.zip`
    )
  })

  test(`text-classification all ${name}`, async () => {
    await page.selectOption('select', 'template-text-classification')

    await page.check('#include_test-checkbox')
    expect(await page.isChecked('#include_test-checkbox')).toBeTruthy()

    await page.waitForSelector('text=README.md')
    await page.getByText('Training', { exact: true }).click()
    await page
      .getByRole('combobox', {
        name: 'Select the argument parser for training'
      })
      .selectOption(`${name}`)
    await page.check('#deterministic-checkbox')
    expect(await page.isChecked('#deterministic-checkbox')).toBeTruthy()

    await page.click('text=Handlers')

    await page.check('#save_training-checkbox')
    expect(await page.isChecked('#save_training-checkbox')).toBeTruthy()

    await page.check('#save_evaluation-checkbox')
    expect(await page.isChecked('#save_evaluation-checkbox')).toBeTruthy()

    await page.fill('#filename_prefix-input-text', 'training')
    expect(
      await page.$eval('#filename_prefix-input-text', (e) => e.value)
    ).toBe('training')

    await page.fill('#save_every_iters-input-number', '2')
    expect(
      await page.$eval('#save_every_iters-input-number', (e) => e.value)
    ).toBe('2')

    await page.fill('#n_saved-input-number', '2')
    expect(await page.$eval('#n_saved-input-number', (e) => e.value)).toBe('2')

    await page.check('#terminate_on_nan-checkbox')
    expect(await page.isChecked('#terminate_on_nan-checkbox')).toBeTruthy()

    await page.fill('#patience-input-number', '2')
    expect(await page.$eval('#patience-input-number', (e) => e.value)).toBe('2')

    await page.fill('#limit_sec-input-number', '60')
    expect(await page.$eval('#limit_sec-input-number', (e) => e.value)).toBe(
      '60'
    )

    await page.click('text=Loggers')
    await page.click('text=config.yaml')

    const downloadPromise = await page
      .waitForEvent('download', { timeout: 2000 })
      .catch(() => {
        page.getByRole('button', { name: 'Code' }).click()
        page.getByRole('button', { name: 'Download Zip' }).click()
        return page.waitForEvent('download', { timeout: 2000 })
      })
      .catch(() => {
        page.getByRole('button', { name: 'Code' }).click()
        page.getByRole('button', { name: 'Download Zip' }).click()
        return page.waitForEvent('download', { timeout: 2000 })
      })
      .catch(() => {
        page.getByRole('button', { name: 'Code' }).click()
        page.getByRole('button', { name: 'Download Zip' }).click()
        return page.waitForEvent('download', { timeout: 2000 })
      })
    await downloadPromise.saveAs(
      `./dist-tests/text-classification-all-${name}.zip`
    )
  })

  test(`text-classification launch ${name}`, async () => {
    await page.selectOption('select', 'template-text-classification')

    await page.waitForSelector('text=README.md')
    await page.getByText('Training', { exact: true }).click()

    await page
      .getByRole('combobox', {
        name: 'Select the argument parser for training'
      })
      .selectOption(`${name}`)
    await page.check('#use_dist-checkbox')
    expect(await page.isChecked('#use_dist-checkbox')).toBeTruthy()

    expect(await page.isChecked('#dist-torchrun-radio')).toBeTruthy()

    await page.click('text=Loggers')
    await page.click('text=config.yaml')

    const downloadPromise = await page
      .waitForEvent('download', { timeout: 2000 })
      .catch(() => {
        page.getByRole('button', { name: 'Code' }).click()
        page.getByRole('button', { name: 'Download Zip' }).click()
        return page.waitForEvent('download', { timeout: 2000 })
      })
      .catch(() => {
        page.getByRole('button', { name: 'Code' }).click()
        page.getByRole('button', { name: 'Download Zip' }).click()
        return page.waitForEvent('download', { timeout: 2000 })
      })
      .catch(() => {
        page.getByRole('button', { name: 'Code' }).click()
        page.getByRole('button', { name: 'Download Zip' }).click()
        return page.waitForEvent('download', { timeout: 2000 })
      })

    await downloadPromise.saveAs(
      `./dist-tests/text-classification-launch-${name}.zip`
    )
  })

  test('text-classification spawn', async () => {
    await page.selectOption('select', 'template-text-classification')

    await page.waitForSelector('text=README.md')
    await page.getByText('Training', { exact: true }).click()
    await page
      .getByRole('combobox', {
        name: 'Select the argument parser for training'
      })
      .selectOption(`${name}`)
    await page.check('#use_dist-checkbox')
    expect(await page.isChecked('#use_dist-checkbox')).toBeTruthy()

    await page.check('#dist-spawn-radio')
    expect(await page.isChecked('#dist-spawn-radio')).toBeTruthy()

    await page.click('text=Loggers')
    await page.click('text=config.yaml')

    const downloadPromise = await page
      .waitForEvent('download', { timeout: 2000 })
      .catch(() => {
        page.getByRole('button', { name: 'Code' }).click()
        page.getByRole('button', { name: 'Download Zip' }).click()
        return page.waitForEvent('download', { timeout: 2000 })
      })
      .catch(() => {
        page.getByRole('button', { name: 'Code' }).click()
        page.getByRole('button', { name: 'Download Zip' }).click()
        return page.waitForEvent('download', { timeout: 2000 })
      })
      .catch(() => {
        page.getByRole('button', { name: 'Code' }).click()
        page.getByRole('button', { name: 'Download Zip' }).click()
        return page.waitForEvent('download', { timeout: 2000 })
      })
    await downloadPromise.saveAs(
      `./dist-tests/text-classification-spawn-${name}.zip`
    )
  })
}
