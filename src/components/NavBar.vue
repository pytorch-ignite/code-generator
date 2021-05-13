<template>
  <nav class="nav-bar">
    <h1>
      <a href="/">
        <img
          src="../assets/ignite_logomark.svg"
          alt="PyTorch-Ignite logo"
          width="50"
          height="50"
        />
        <span class="pname">Code Generator</span>
        <small class="version">v{{ version }}</small>
      </a>
    </h1>
    <div class="left-side-badges">
      <button
        @click="downloadProject"
        class="download-button"
        title="Download the generated code as a zip file"
      >
        <IconDownload />
        <span class="icon-text">Download</span>
      </button>
      <a
        class="external-links"
        href="https://github.com/pytorch-ignite/code-generator"
        target="_blank"
        rel="noopener noreferrer"
      >
        <IconGitHub />
        <span class="icon-text">GitHub</span>
      </a>
      <a
        class="external-links"
        href="https://twitter.com/pytorch_ignite"
        target="_blank"
        rel="noopener noreferrer"
      >
        <IconTwitter />
        <span class="icon-text">Twitter</span>
      </a>
      <a
        class="external-links"
        href="https://discord.gg/djZtm3EmKj"
        target="_blank"
        rel="noopener noreferrer"
      >
        <IconDiscord />
        <span class="icon-text">Discord</span>
      </a>
    </div>
    <div
      class="download-success"
      v-show="showDownloadMsg"
      @click="showDownloadMsg = false"
    >
      <div class="msg-wrapper">
        <div class="msg">
          <h2>🎉 Your Training Script Generated! 🎉</h2>
          <p>
            Thanks for using Code-Generator! Feel free to reach out to us on
            <a
              class="external-links msg-gh"
              href="https://github.com/pytorch-ignite/code-generator"
              target="_blank"
              rel="noopener noreferrer"
            >
              GitHub </a
            >with any feedback, bug report, and feature request.
          </p>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import { version } from '../../package.json'
import { store } from '../store'
import { saveAs } from 'file-saver'
import JSZip from 'jszip'
import IconDiscord from './IconDiscord.vue'
import IconDownload from './IconDownload.vue'
import IconGitHub from './IconGitHub.vue'
import IconTwitter from './IconTwitter.vue'
import { ref } from 'vue'

export default {
  components: { IconDiscord, IconDownload, IconGitHub, IconTwitter },
  setup() {
    let zip = new JSZip()
    const showDownloadMsg = ref(false)

    const downloadProject = () => {
      for (const filename in store.code) {
        zip.file(filename, store.code[filename])
      }
      zip.generateAsync({ type: 'blob' }).then((content) => {
        saveAs(content, 'ignite-project.zip')
      })
      showDownloadMsg.value = true
    }
    return { version, downloadProject, showDownloadMsg }
  }
}
</script>

<style scoped>
h1 {
  margin: 0;
  font-weight: normal;
}
a {
  text-decoration: none;
  color: var(--c-text);
}
h1 img {
  vertical-align: middle;
  position: relative;
  top: -5px;
}
.external-links {
  margin: 0 0.5rem;
  font-size: var(--font-size);
  border-bottom: 2px solid transparent;
}
.external-links:hover {
  border-bottom: 2px solid var(--c-brand-red);
}
.nav-bar {
  display: flex;
  align-items: center;
  padding: 0.5rem 1.5rem 0;
  justify-content: space-between;
  border-bottom: 1px solid var(--c-white-dark);
}
.version {
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
  line-height: 1.25rem;
  margin-left: 0.25rem;
  background-color: #007bff;
  border-radius: 8px 2px 8px 2px;
  color: var(--c-white-light);
  font-weight: bolder;
}
.left-side-badges {
  display: flex;
  align-items: center;
}
.download-button {
  background: none;
  color: var(--c-text);
  cursor: pointer;
  font-family: var(--font-family-base);
  font-size: var(--font-size);
  padding-top: 0;
  padding-bottom: 0;
}
.icons {
  vertical-align: middle;
  position: relative;
  top: -1px;
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
  display: block;
  max-width: 38rem;
  margin: 20vh auto 0;
  text-align: center;
  padding: 0 1rem;
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
.icon-text {
  margin-left: 0.5rem;
}
/* media queries */
@media (max-width: 768px) {
  .pname,
  .version {
    display: none;
  }
  .nav-bar {
    position: fixed;
    z-index: 6;
    width: 100%;
    background-color: var(--c-white);
  }
  .icon-text {
    display: none;
  }
}
</style>
