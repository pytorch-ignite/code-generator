<template>
  <div>
    <div class="dropdown">
      <button
        @click="downloadProject"
        class="download-button external-links"
        title="Get the code of the template"
      >
        <div>
          <!-- Icon like in GH -->
          <span class="topline">
            <svg
              aria-hidden="true"
              height="16"
              viewBox="0 0 15 15"
              version="1.1"
              width="16"
              data-view-component="true"
            >
              <path
                d="m11.28 3.22 4.25 4.25a.75.75 0 0 1 0 1.06l-4.25 4.25a.749.749 0 0 1-1.275-.326.749.749 0 0 1 .215-.734L13.94 8l-3.72-3.72a.749.749 0 0 1 .326-1.275.749.749 0 0 1 .734.215Zm-6.56 0a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042L2.06 8l3.72 3.72a.749.749 0 0 1-.326 1.275.749.749 0 0 1-.734-.215L.47 8.53a.75.75 0 0 1 0-1.06Z"
              ></path>
            </svg>
          </span>
          <span id="code">Code</span>
          <span class="topline">
            <svg
              aria-hidden="true"
              height="16"
              viewBox="0 0 16 16"
              version="1.1"
              width="16"
              data-view-component="true"
            >
              <path
                d="m4.427 7.427 3.396 3.396a.25.25 0 0 0 .354 0l3.396-3.396A.25.25 0 0 0 11.396 7H4.604a.25.25 0 0 0-.177.427Z"
              ></path>
            </svg>
          </span>
        </div>
      </button>
      <div class="dropdown-content">
        <div class="text-input-group">
          <div class="copy-link">
            <button
              v-if="!linkGenerated"
              class="copy-link-input generate"
              id="text-box"
              @click="generateLink"
            >
              <span v-if="!linkGenerating">Generate Link</span>
              <span v-if="linkGenerating">Generating...</span>
            </button>
            <input
              v-if="linkGenerated"
              type="url"
              class="copy-link-input generate"
              v-model="codeUrl"
              readonly
            />
            <button
              type="button"
              class="copy-link-button"
              @click="copyURL"
              id="text-box"
            >
              <span class="material-icons copy-button">content_copy </span>
            </button>
          </div>
          <span class="copy-notification">Copied!</span>
          <p class="wget-text">Use wget or paste the link in your browser.</p>
          <hr class="solid" />
        </div>
        <NavDownload @showDownloadMsg="DownloadMsg" />
      </div>
    </div>
    <!-- creating a one-way binding for download success message -->
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
  </div>
</template>

<script>
import NavDownload from './NavDownload.vue'
import { ref, watch } from 'vue'
import { store, msg } from '../store'

export default {
  name: 'NavCode',
  components: { NavDownload },
  setup() {
    const linkGenerating = ref(false)
    const linkGenerated = ref(false)
    const codeUrl = ref('')
    const DownloadMsgUpdate = ref(false)
    const showDownloadMsg = ref(false)

    const generateLink = async () => {
      if (store.code && Object.keys(store.code).length) {
        msg.color = 'red'
        if (!store.config.output_dir) {
          msg.showMsg = true
          msg.content = `Output directory is required. Please input in Loggers tab.`
        } else if (!store.config.log_every_iters) {
          msg.showMsg = true
          msg.content = `Logging interval is required. Please input in Loggers tab.`
        } else {
          // By default, Netlify function url is
          // base netlify url + .netlify/functions/function-name
          // We make a POST request to the function with
          // the content of store.code in JSON as request body
          linkGenerating.value = true
          const res = await fetch('/.netlify/functions/code', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              code: store.code,
              template: store.config.template,
              config: store.config
            })
          })
          if (res.ok) {
            linkGenerated.value = true
            codeUrl.value = store.codeUrl = await res.text()
          }
        }
      } else {
        msg.showMsg = true
        msg.content = 'Choose a template to Open.'
      }
    }

    const DownloadMsg = () => {
      DownloadMsgUpdate.value = true
    }
    const copyURL = () => {
      try {
        if (codeUrl.value != '') {
          navigator.clipboard.writeText(store.codeUrl)
          const button = document.querySelector('.copy-link-button')
          const notification = document.querySelector('.copy-notification')

          button.classList.add('copied')
          notification.style.display = 'inline'

          setTimeout(function () {
            button.classList.remove('copied')
            notification.style.display = 'none'
          }, 2000)
        }
      } catch ($e) {
        alert('Cannot copy')
      }
    }
    // for the download message
    watch(DownloadMsgUpdate, () => {
      showDownloadMsg.value = true
      DownloadMsgUpdate.value = false
    })
    // To have a new wget URL for change in configuration
    watch(store.config, () => {
      linkGenerated.value = false
      store.codeUrl = codeUrl.value = ''
      linkGenerating.value = false
    })

    return {
      linkGenerated,
      codeUrl,
      showDownloadMsg,
      linkGenerating,
      DownloadMsg,
      copyURL,
      generateLink
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
/* Adjusting the top Code button */
.topline {
  vertical-align: middle;
}

#code {
  font-size: 1rem;
}

.download-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: none;
  color: var(--c-text);
  cursor: pointer;
  font-family: var(--font-family-base);
  font-size: 14px;
  padding: 0.5rem 1rem;
  border: 1px solid var(--c-brand-red);
  border-radius: 4px;
}

.download-button span {
  margin-left: 0.25rem;
}

/* Dropdown Button */
.dropbtn {
  background-color: #04aa6d;
  color: white;
  text-align: center;
}
/* Dropdown Content (Hidden by Default) */
.dropdown-content {
  display: none;
  position: absolute;
  background-color: var(--c-white-light);
  min-width: 15vw;
  box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
  z-index: 1;
  padding: 0.5vh;
  text-align: center; /* Center-align the dropdown content */
  border: 1px solid var(--c-brand-red);
  border-radius: 3%;
  text-align: -webkit-center;
}

/* Show the dropdown menu on hover */
.dropdown:hover .dropdown-content {
  display: block;
}

/* Change the background color of the dropdown button when the dropdown content is shown */
.dropdown:hover .dropbtn {
  background-color: var(--c-brand-red);
}

.text-input-group {
  margin-top: 2vh;
}

.copy-link {
  --height: 1.6rem;
  display: flex;
  max-width: 50vw;
  font-size: 80%;
  margin-top: 8%;
  align-self: center;
  margin-left: 1.1vw;
}
.generate {
  background-color: #ffffff;
  width: 80%;
  font-size: 60%;
  height: 1.5rem;
}
#text-box {
  font-size: 90%;
  height: 1.6rem;
  border-radius: 3%;
}

.icon {
  vertical-align: bottom;
}
.inline-icon {
  display: inline-flex;
  vertical-align: bottom;
}

.copy-link-input {
  flex-grow: 0;
  padding: 0 8px;
  font-size: 14px;
  border: 1px solid var(--c-brand-red);
  border-right: none;
  outline: none;
}

.copy-link-input:hover {
  background: var(--c-brand-red);
  border: 1px solid #cccccc;
  color: #f1f1f1;
}

.copy-link-button {
  width: 2rem;
  height: 8%;
  display: flex;
  background: #dddddd;
  color: #333333;
  border: 1px solid var(--c-brand-red);
  font-size: 50%;
}

.copy-link-button:hover {
  background: #cccccc;
}

.copy-notification {
  display: none;
  margin-left: 75%;
  color: var(--c-white-light);
  font-size: 0.6rem;
  background-color: var(--c-brand-red);
  padding: 2%;
  border-radius: 10%;
}

.copy-link-button.copied + .copy-notification {
  display: block;
  z-index: 10;
}
.copy-button {
  font-size: 1rem;
}
.wget-text {
  font-size: 0.6em;
}

/* Solid border */
hr.solid {
  border-top: 1px solid var(--c-brand-red);
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
  position: fixed;
  max-width: 38rem;
  padding: 0 1rem;
  text-align: center;
  margin: 20vh auto 100%;
  inset: 0;
  z-index: 10;
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
