<template>
  <button
    @click="downloadProject"
    class="download-button external-links"
    id="download-zip"
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
    <span>Download Zip</span>
  </button>
</template>

<script>
import { ref } from 'vue'
import { store, msg } from '../store'
import { saveAs } from 'file-saver'
import JSZip from 'jszip'

export default {
  emits: ['showDownloadMsg'],
  setup(props, { emit }) {
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
          emit('showDownloadMsg', showDownloadMsg)
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
#download-zip {
  font-size: 1.6vh;
}

.download-button span {
  margin-left: 0.25rem;
}
</style>
