<template>
  <button
    @click="downloadProject"
    class="download-button"
    title="Open in Colab"
  >
    <a
      class="external-links"
      :href="colabLink"
      target="_blank"
      rel="noopener noreferrer"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        xmlns:xlink="http://www.w3.org/1999/xlink"
        width="2.0em"
        height="1.4em"
      >
        <linearGradient id="b" x2="0" y2="100%">
          <stop offset="0" stop-color="#bbb" stop-opacity=".1" />
          <stop offset="1" stop-opacity=".1" />
        </linearGradient>
        <clipPath id="a">
          <rect width="117" height="20" rx="3" fill="#fff" />
        </clipPath>
        <g clip-path="url(#a)">
          <path fill="#fff" d="M0 0h30v20H0z" />
        </g>
        <g
          fill="#fff"
          text-anchor="middle"
          font-family="DejaVu Sans,Verdana,Geneva,sans-serif"
          font-size="110"
        >
          <svg
            x="4px"
            y="0px"
            width="23px"
            height="21px"
            viewBox="0 0 24 24"
            style="background-color: #fff; border-radius: 1px"
          >
            <path
              style="fill: #e8710a"
              d="M1.977,16.77c-2.667-2.277-2.605-7.079,0-9.357C2.919,8.057,3.522,9.075,4.49,9.691c-1.152,1.6-1.146,3.201-0.004,4.803C3.522,15.111,2.918,16.126,1.977,16.77z"
            />
            <path
              style="fill: #f9ab00"
              d="M12.257,17.114c-1.767-1.633-2.485-3.658-2.118-6.02c0.451-2.91,2.139-4.893,4.946-5.678c2.565-0.718,4.964-0.217,6.878,1.819c-0.884,0.743-1.707,1.547-2.434,2.446C18.488,8.827,17.319,8.435,16,8.856c-2.404,0.767-3.046,3.241-1.494,5.644c-0.241,0.275-0.493,0.541-0.721,0.826C13.295,15.939,12.511,16.3,12.257,17.114z"
            />
            <path
              style="fill: #e8710a"
              d="M19.529,9.682c0.727-0.899,1.55-1.703,2.434-2.446c2.703,2.783,2.701,7.031-0.005,9.764c-2.648,2.674-6.936,2.725-9.701,0.115c0.254-0.814,1.038-1.175,1.528-1.788c0.228-0.285,0.48-0.552,0.721-0.826c1.053,0.916,2.254,1.268,3.6,0.83C20.502,14.551,21.151,11.927,19.529,9.682z"
            />
            <path
              style="fill: #f9ab00"
              d="M4.49,9.691C3.522,9.075,2.919,8.057,1.977,7.413c2.209-2.398,5.721-2.942,8.476-1.355c0.555,0.32,0.719,0.606,0.285,1.128c-0.157,0.188-0.258,0.422-0.391,0.631c-0.299,0.47-0.509,1.067-0.929,1.371C8.933,9.539,8.523,8.847,8.021,8.746C6.673,8.475,5.509,8.787,4.49,9.691z"
            />
            <path
              style="fill: #f9ab00"
              d="M1.977,16.77c0.941-0.644,1.545-1.659,2.509-2.277c1.373,1.152,2.85,1.433,4.45,0.499c0.332-0.194,0.503-0.088,0.673,0.19c0.386,0.635,0.753,1.285,1.181,1.89c0.34,0.48,0.222,0.715-0.253,1.006C7.84,19.73,4.205,19.188,1.977,16.77z"
            />
          </svg>
        </g>
      </svg>
      <span>Open in Colab</span>
    </a>
  </button>
  <div
    class="download-success"
    v-show="showDownloadMsg"
    @click="showDownloadMsg = false"
  ></div>
  <div class="msg-wrapper" v-show="showDownloadMsg">
    <div class="msg">
      <h2>🎉 Your Training Script Has Been Generated! 🎉</h2>
      <p>
        Thanks for using Code-Generator! Feel free to reach out to us on
        <a
          class="external-links msg-gh"
          href="https://github.com/pytorch-ignite/code-generator"
          target="_blank"
          rel="noopener noreferrer"
          >GitHub</a
        >
        with any feedback, bug report, and feature request.
      </p>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { store, msg } from '../store'
import { v4 as uuidv4 } from 'uuid'
import { Octokit } from 'https://cdn.skypack.dev/@octokit/core'

export default {
  setup() {
    const showDownloadMsg = ref(false)
    const colabLink = ref()
    const downloadProject = () => {
      if (store.code && Object.keys(store.code).length) {
        msg.color = 'red'
        if (!store.config.output_dir) {
          msg.showMsg = true
          msg.content = `Output directory is required. Please input in Loggers tab.`
        } else if (!store.config.log_every_iters) {
          msg.showMsg = true
          msg.content = `Logging interval is required. Please input in Loggers tab.`
        } else {
          // Create notebook placeholder
          var nb = {
            metadata: {},
            cells: [],
            nbformat: 4,
            nbformat_minor: 2
          }

          var firstCell // README
          var reqCell // !pip install ...
          var configCell // %%writefile config.yaml
          var lastCell // main()

          for (const filename in store.code) {
            // Append regular py files
            if (filename.includes('.py')) {
              var cell = {
                cell_type: 'code',
                metadata: {},
                source: [store.code[filename]],
                outputs: [],
                execution_count: null
              }
              // main will be at the end
              if (filename.includes('main.py')) {
                lastCell = cell
              } else if (filename.includes('test_all.py')) {
                continue
              } else {
                nb['cells'].push(cell)
              }
              // Readme will be at the beginning
            } else if (filename.includes('README.md')) {
              var firstCell = {
                cell_type: 'markdown',
                metadata: {},
                source: [store.code[filename]]
              }
              // requirements should be just after the README
            } else if (filename.includes('requirements.txt')) {
              var cell = {
                cell_type: 'code',
                metadata: {},
                source: [
                  '!pip install '.concat(
                    store.code[filename]
                      .split('\n')
                      .join(' ')
                      .replace('pytest', '')
                  )
                ],
                outputs: [],
                execution_count: null
              }
              reqCell = cell
              // config will be after installing requirements
            } else if (filename.includes('config.yaml')) {
              var cell = {
                cell_type: 'code',
                metadata: {},
                source: ['%%writefile config.yaml\n', store.code[filename]],
                outputs: [],
                execution_count: null
              }
              configCell = cell
            }
          }

          // Finalize notebook structure
          nb['cells'] = [
            firstCell,
            reqCell,
            {
              cell_type: 'markdown',
              metadata: {},
              source: ['### Create a config file\n']
            },
            configCell,
            ...nb['cells'],
            lastCell
          ]

          // Conver to json
          var nbJSON = JSON.stringify(nb)

          var nbUid = uuidv4()
          var nbName = 'pytorch-ignite-notebook.ipynb'
          var repoOwner = process.env.VUE_APP_GH_USER
          var repo = process.env.VUE_APP_GH_REPO

          const octokit = new Octokit({
            auth: process.env.VUE_APP_GH_TOKEN
          })
          const response = octokit.request(
            'PUT /repos/{owner}/{repo}/contents/{path}',
            {
              owner: repoOwner,
              repo: repo,
              path: `nbs/${nbUid}/${nbName}`,
              message: `nb: add ${nbUid}`,
              content: btoa(unescape(encodeURIComponent(nbJSON)))
            }
          )

          // Getting static link
          colabLink.value = `https://colab.research.google.com/github/${repoOwner}/${repo}/blob/main/nbs/${nbUid}/${nbName}`
        }
      } else {
        msg.showMsg = true
        msg.content = 'Choose a template to Open.'
      }
    }
    return { downloadProject, showDownloadMsg, colabLink }
  }
}
</script>

<style scoped>
.download-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: none;
  color: var(--c-text);
  cursor: pointer;
  font-family: var(--font-family-base);
  font-size: 1em;
  padding: 0.5rem 1rem;
  border: 1px solid var(--c-brand-red);
  border-radius: 4px;
}
.external-links {
  display: flex;
  align-items: center;
}
.download-success {
  position: fixed;
  top: 0;
  left: 0;
  background-color: rgba(101, 110, 133, 0.8);
  z-index: 10;
  width: 100vw;
  height: 100vh;
}
.msg-wrapper {
  position: absolute;
  max-width: 38rem;
  padding: 0 1rem;
  text-align: center;
  margin: 20vh auto 100%;
  inset: 0;
  z-index: 12;
}
.msg {
  padding: 2rem 1rem;
  background-color: var(--c-white-light);
  color: var(--c-text);
  border-radius: 8px;
  box-shadow: 0 0 5px 5px rgba(0, 0, 0, 0.33);
}
.msg-gh {
  margin: 0;
  color: var(--c-brand-red);
}
</style>
