<template>
  <div>
    <div class="dropdown">
      <button @click="downloadProject" class="nebari-button external-links">
        <div>
          <!-- Icon like in GH -->
          <span class="topline">
            <img
              src="../assets/Nebari-logo-square.svg"
              height="18"
              viewBox="0 0 18 18"
              version="1.1"
              width="18"
            />
          </span>
          <span id="code">Open in Nebari</span>
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
        <div class="text-box-nebari" id="nebari-text">
          <span class="sub-text">
            <a href="https://www.nebari.dev/" target="_blank">
              <strong>Nebari</strong>: open source data science platform
            </a>
          </span>
        </div>
        <hr class="solid" />
        <div class="text-box-nebari" id="nebari-text">
          <h5 class="requirement-label">Requirement</h5>
          <p class="sub-text">
            Please install
            <a
              href="https://github.com/jupyterlab/jupyterlab-github"
              target="_blank"
              >JupyterLab-GitHub</a
            >
            extension on your Nebari instance.
          </p>
          <pre class="code-snippet">pip install jupyterlab-github <span
              class="material-icons copy-button-nebari copy-link-button-nebari"
              @click="copyCommand"
              ><span v-if="!copiedCommand">
              content_copy
              </span>
              <span v-else>
              check
              </span>
            </span></pre>
        </div>

        <hr class="solid" />
        <div class="text-input-group" id="nebari-text">
          <div class="text-box-nebari">
            <h5 class="form-label">Nebari URL</h5>
            <input
              v-model="hubUrl"
              @input="validateHubUrl"
              placeholder="https://nebari.yourdomain.dev"
              aria-label="JupyterHub URL"
              class="text-box-nebari-details"
            />
            <p v-if="hubUrl != '' && !isValidHubUrl" class="error-text">
              Enter a valid Nebari instance URL
            </p>
          </div>
          <div class="text-box-nebari">
            <h5 class="form-label">Nebari Username</h5>
            <input
              v-model="userName"
              placeholder="username"
              aria-label="Nebari Username"
              @input="validUserName"
              class="text-box-nebari-details"
            />
            <p v-if="userName != '' && !isValidUserName" class="error-text">
              Enter a valid Nebari username
            </p>
          </div>
        </div>
        <div class="text-input-group-generate" id="open-in-nebari">
          <button class="copy-link-input generate" id="nebari-bottom-button">
            <span v-if="!linkGenerating" @click="generateLink"
              >Open in Nebari</span
            >
            <span v-if="linkGenerating">Generating Link...</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavDownload from './NavDownload.vue'
import { ref } from 'vue'
import { store, msg } from '../store'

export default {
  name: 'NavNebari',
  components: { NavDownload },
  setup() {
    // Nebari User details
    const userName = ref('')
    const hubUrl = ref('')
    // CodeUrl
    const nebariCodeUrl = ref('')
    const isValidHubUrl = ref(false)
    const isValidUserName = ref(false)
    const linkGenerating = ref(false)
    const linkGenerated = ref(false)

    const validateHubUrl = () => {
      try {
        new URL(hubUrl.value)
        isValidHubUrl.value = true
      } catch (error) {
        isValidHubUrl.value = false
      }
    }
    const validUserName = () => {
      isValidUserName.value = /^[0-9a-zA-Z_@.-]+$/.test(userName.value)
    }
    const generateLink = async () => {
      if (store.code && Object.keys(store.code).length) {
        msg.color = 'red'
        if (!store.config.output_dir) {
          msg.showMsg = true
          msg.content = `Output directory is required. Please input in Loggers tab.`
        } else if (!store.config.log_every_iters) {
          msg.showMsg = true
          msg.content = `Logging interval is required. Please input in Loggers tab.`
        } else if (
          hubUrl.value == '' ||
          userName.value == '' ||
          !isValidHubUrl.value ||
          !isValidUserName.value
        ) {
          msg.showMsg = true
          msg.content = `Please enter correct Nebari instance details.`
        } else {
          // By default, Netlify function url is
          // base netlify url + .netlify/functions/function-name
          // We make a POST request to the function with
          // the content of store.code in JSON as request body
          linkGenerating.value = true
          const res = await fetch('/.netlify/functions/nebari', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              code: store.code,
              template: store.config.template,
              config: store.config,
              commit: store.commit,
              argparser: store.config.argparser,
              nebariInstanceLink: hubUrl.value,
              userName: userName.value
            })
          })
          if (res.ok) {
            nebariCodeUrl.value = store.nebariCodeUrl = await res.text()
            // create a hyperlink element
            const el = document.createElement('a')
            el.setAttribute('href', nebariCodeUrl.value)
            el.setAttribute('target', '_blank')
            el.setAttribute('rel', 'noopener noreferrer')
            el.click()
          }
        }
      } else {
        msg.showMsg = true
        msg.content = 'Choose a template to Open.'
      }
      linkGenerating.value = false
    }

    const copiedCommand = ref(false)
    const copyCommand = () => {
      try {
        navigator.clipboard.writeText('pip install jupyterlab-github')
        copiedCommand.value = true
        setTimeout(function () {
          copiedCommand.value = false
        }, 2000)
      } catch ($e) {
        alert('Cannot copy')
      }
    }

    return {
      userName,
      hubUrl,
      linkGenerating,
      nebariCodeUrl,
      isValidHubUrl,
      isValidUserName,
      copiedCommand,
      generateLink,
      validateHubUrl,
      validUserName,
      copyCommand
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
#nebari-text {
  margin: 1.5vh;
}
.nebari-button {
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

.nebari-button span {
  margin-left: 0.25rem;
}

/* Dropdown Content (Hidden by Default) */
.dropdown-content {
  display: none;
  position: absolute;
  background-color: var(--background-color-primary);
  min-width: 15vw;
  box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
  z-index: 100;
  padding: 1.5vh;
  text-align: center;
  /* Center-align the dropdown content */
  border: 1px solid var(--c-brand-red);
  border-radius: 3%;
  text-align: -webkit-center;
}

/* Show the dropdown menu on hover */
.dropdown:hover .dropdown-content {
  display: block;
}

.text-input-group {
  margin-top: 2vh;
  display: block;
}
.text-input-group .form-label {
  margin: 0;
  font-size: 80%;
}
/* New style for error message */
.error-text {
  color: red;
  font-size: xx-small;
}

/* Requirement Text CSS */
.requirement-label {
  margin-bottom: 0%;
  margin-top: 1vh;
}
.sub-text {
  font-size: 0.8rem;
  margin-top: 0%;
}
.copy-link-input {
  flex-grow: 0;
  padding: 0 8px;
  font-size: 14px;
  border: 1px solid var(--c-brand-red);
  outline: none;
}
.code-snippet {
  text-align: center;
  background-color: var(--c-white-dark)
}

/* Text Box CSS */
.text-box-nebari {
  text-align: left;
}
.text-input-group-generate {
  margin-top: 2vh;
  text-align: center;
  font-size: larger;
}
.text-box-nebari-details {
  background: var(--background-color-secondary);
  color: var(--c-text);
  width: 95%;
  height: 3vh;
}

.copy-link-input:hover {
  background: var(--c-brand-red) !important;
  border: 1px solid #cccccc;
  color: black;
}

#nebari-bottom-button {
  border-radius: 5px;
  width: 80%;
  height: 4vh;
  display: block;
  font-size: large;
  max-height: 40px;
  margin: 2.8vh;
  margin-top: 3vh;
  margin-bottom: 2vh;
  background: var(--background-color-primary);
  color: var(--c-text);
}
.copy-button-nebari {
  font-size: 1rem;
  vertical-align: sub;
  margin-right: 0.1rem;
}
.copy-button-nebari {
  font-size: 1rem;
}

#open-in-nebari {
  text-align: inherit;
}

/* Solid border */
hr.solid {
  border-top: 1px dotted var(--c-brand-red);
}
</style>
