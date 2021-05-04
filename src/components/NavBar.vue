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
        <span>Code Generator</span>
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
        <svg
          xmlns="http://www.w3.org/2000/svg"
          xmlns:xlink="http://www.w3.org/1999/xlink"
          aria-hidden="true"
          role="img"
          class="iconify download iconify--system-uicons"
          width="20"
          height="20"
          preserveAspectRatio="xMidYMid meet"
          viewBox="0 0 21 21"
        >
          <g
            fill="none"
            fill-rule="evenodd"
            stroke="currentColor"
            stroke-width="1.5"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <path d="M6.5 10.5l4 4.232l4-4.191"></path>
            <path d="M10.5 3.5v11"></path>
            <path d="M4.5 17.5h12"></path>
          </g>
        </svg>
      </button>
      <a
        class="external-links"
        href="https://github.com/pytorch-ignite/code-generator"
        target="_blank"
        rel="noopener noreferrer"
      >
        GitHub
        <svg
          xmlns="http://www.w3.org/2000/svg"
          xmlns:xlink="http://www.w3.org/1999/xlink"
          aria-hidden="true"
          role="img"
          class="iconify iconify--system-uicons"
          width="15"
          height="15"
          preserveAspectRatio="xMidYMid meet"
          viewBox="0 0 21 21"
        >
          <g
            fill="none"
            fill-rule="evenodd"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <path d="M18.5 8.5v-5h-5"></path>
            <path d="M18.5 3.5l-7 7"></path>
            <path
              d="M10.5 3.5h-5a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h11a2 2 0 0 0 2-2v-4"
            ></path>
          </g>
        </svg>
      </a>
      <a
        class="external-links"
        href="https://twitter.com/pytorch_ignite"
        target="_blank"
        rel="noopener noreferrer"
      >
        Twitter
        <svg
          xmlns="http://www.w3.org/2000/svg"
          xmlns:xlink="http://www.w3.org/1999/xlink"
          aria-hidden="true"
          role="img"
          class="iconify iconify--system-uicons"
          width="15"
          height="15"
          preserveAspectRatio="xMidYMid meet"
          viewBox="0 0 21 21"
        >
          <g
            fill="none"
            fill-rule="evenodd"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <path d="M18.5 8.5v-5h-5"></path>
            <path d="M18.5 3.5l-7 7"></path>
            <path
              d="M10.5 3.5h-5a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h11a2 2 0 0 0 2-2v-4"
            ></path>
          </g>
        </svg>
      </a>
      <a
        class="external-links"
        href="https://discord.gg/djZtm3EmKj"
        target="_blank"
        rel="noopener noreferrer"
      >
        Discord
        <svg
          xmlns="http://www.w3.org/2000/svg"
          xmlns:xlink="http://www.w3.org/1999/xlink"
          aria-hidden="true"
          role="img"
          class="iconify iconify--system-uicons"
          width="15"
          height="15"
          preserveAspectRatio="xMidYMid meet"
          viewBox="0 0 21 21"
        >
          <g
            fill="none"
            fill-rule="evenodd"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <path d="M18.5 8.5v-5h-5"></path>
            <path d="M18.5 3.5l-7 7"></path>
            <path
              d="M10.5 3.5h-5a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h11a2 2 0 0 0 2-2v-4"
            ></path>
          </g>
        </svg>
      </a>
    </div>
  </nav>
</template>

<script>
import { version } from '../../package.json'
import { store } from '../store'
import { saveAs } from 'file-saver'
import JSZip from 'jszip'

export default {
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
  margin: 0.25rem;
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
}
.iconify {
  vertical-align: middle;
  position: relative;
  top: -2px;
}
.iconify.download {
  top: -3px;
}
</style>
