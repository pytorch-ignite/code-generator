<template>
  <button
    @click="downloadProject"
    class="download-button external-links"
    title="Download the generated code as a zip file"
  >
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="1.4em"
      height="1.4em"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      stroke-width="2"
      stroke-linecap="round"
      stroke-linejoin="round"
      class="icons feather feather-download"
    >
      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
      <polyline points="7 10 12 15 17 10"></polyline>
      <line x1="12" y1="15" x2="12" y2="3"></line>
    </svg>
    <span class="icon-text">Download</span>
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
import { saveAs } from 'file-saver'
import JSZip from 'jszip'

export default {
  setup() {
    const showDownloadMsg = ref(false)

    const downloadProject = () => {
      const zip = new JSZip()
      if (store.code && Object.keys(store.code).length) {
        msg.color = 'red'
        if (!store.config.output_dir) {
          msg.showMsg = true
          msg.content = `Output directory is required. Please input in Loggers tab.`
        } else if (!store.config.log_every_iters) {
          msg.showMsg = true
          msg.content = `Logging interval is required. Please input in Loggers tab.`
        } else {
          for (const filename in store.code) {
            zip.file(filename, store.code[filename])
          }
          zip.generateAsync({ type: 'blob' }).then((content) => {
            saveAs(content, `ignite-${store.config.template}.zip`)
          })
          showDownloadMsg.value = true
        }
      } else {
        msg.showMsg = true
        msg.content = 'Choose a template to download.'
      }
    }
    return { downloadProject, showDownloadMsg }
  }
}
</script>

<style scoped>
@import url('./css/nav-right.css');

.download-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: none;
  color: var(--c-text);
  cursor: pointer;
  font-family: var(--font-family-base);
  font-size: 1em;
  padding: 0;
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
  margin: 20vh auto 0;
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
