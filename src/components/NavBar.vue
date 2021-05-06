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
        Download
        <IconDownload />
      </button>
      <a
        class="external-links"
        href="https://github.com/pytorch-ignite/code-generator"
        target="_blank"
        rel="noopener noreferrer"
      >
        <IconGitHub />
      </a>
      <a
        class="external-links"
        href="https://twitter.com/pytorch_ignite"
        target="_blank"
        rel="noopener noreferrer"
      >
        <IconTwitter />
      </a>
      <a
        class="external-links"
        href="https://discord.gg/djZtm3EmKj"
        target="_blank"
        rel="noopener noreferrer"
      >
        <IconDiscord />
      </a>
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

export default {
  components: { IconDiscord, IconDownload, IconGitHub, IconTwitter },
  setup() {
    let zip = new JSZip()

    const downloadProject = () => {
      for (const filename in store.code) {
        zip.file(filename, store.code[filename])
      }
      zip.generateAsync({ type: 'blob' }).then((content) => {
        saveAs(content, 'ignite-project.zip')
      })
    }

    return { version, downloadProject }
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
}
.iconify {
  vertical-align: middle;
  position: relative;
  top: -3px;
}
/* media queries */
@media (max-width: 768px) {
  .pname,
  .version {
    display: none;
  }
  .nav-bar {
    position: fixed;
    z-index: 11;
    width: 100%;
    background-color: var(--c-white);
  }
}
</style>
