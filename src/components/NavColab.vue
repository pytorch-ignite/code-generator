<template>
  <button
    @click="downloadProject"
    class="download-button"
    title="Open in Colab"
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
    <span>{{ colabText }}</span>
  </button>
</template>

<script>
import { ref } from 'vue'
import { store, msg } from '../store'

export default {
  setup() {
    const showDownloadMsg = ref(false)
    const colabText = ref('Open in Colab')

    const downloadProject = async () => {
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
          colabText.value = 'Opening in Colab'
          const res = await fetch('/.netlify/functions/colab', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              code: store.code,
              template: store.config.template
            })
          })
          // response body is plain text
          const colabLink = await res.text()
          // create a hyperlink element
          const el = document.createElement('a')
          el.setAttribute('href', colabLink)
          el.setAttribute('target', '_blank')
          el.setAttribute('rel', 'noopener noreferrer')
          el.click()
        }
      } else {
        msg.showMsg = true
        msg.content = 'Choose a template to Open.'
      }
      colabText.value = 'Open in Colab'
    }
    return { downloadProject, showDownloadMsg, colabText }
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
