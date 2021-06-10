<template>
  <button
    @click.prevent="showHelp = true"
    title="Help"
    class="help-btn external-links"
  >
    <svg
      xmlns="http://www.w3.org/2000/svg"
      xmlns:xlink="http://www.w3.org/1999/xlink"
      aria-hidden="true"
      role="img"
      class="iconify iconify--carbon"
      width="1.4em"
      height="1.4em"
      preserveAspectRatio="xMidYMid meet"
      viewBox="0 0 32 32"
    >
      <defs></defs>
      <path
        d="M16 2a14 14 0 1 0 14 14A14 14 0 0 0 16 2zm0 23a1.5 1.5 0 1 1 1.5-1.5A1.5 1.5 0 0 1 16 25zm1.142-7.754v2.501h-2.25V15h2.125a2.376 2.376 0 0 0 0-4.753h-1.5a2.378 2.378 0 0 0-2.375 2.375v.638h-2.25v-.638A4.628 4.628 0 0 1 15.517 8h1.5a4.624 4.624 0 0 1 .125 9.246z"
        fill="currentColor"
      ></path>
    </svg>
    <span class="icon-text">Help</span>
  </button>
  <div
    class="help-bg"
    v-show="showHelp"
    @click.prevent="showHelp = false"
  ></div>
  <div class="help-wrapper" v-show="showHelp">
    <div>
      <h1 class="pis-40px">How to use it?</h1>
      <ol class="steps">
        <li v-for="(step, index) in steps" :key="index" class="step">
          {{ step }}
        </li>
      </ol>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
export default {
  setup() {
    const showHelp = ref(false)

    const steps = [
      '📃 Choose a Template.',
      '⚙️ Adjust the configuration in the corresponding tabs.',
      '🔬 Inspect the code in the right pane.',
      '📦 Download the source code as zip.',
      '🚀 Use it for your project.'
    ]

    return { steps, showHelp }
  }
}
</script>

<style scoped>
@import url('./css/nav-right.css');

.help-btn {
  background: none;
  color: var(--c-text);
  font-size: var(--font-size);
  cursor: pointer;
  padding: 0;
}
.help-bg {
  text-align: left;
  color: var(--c-text);
  text-transform: none;
  position: fixed;
  top: 0;
  left: 0;
  background-color: rgba(101, 110, 133, 0.8);
  z-index: 10;
  width: 100vw;
  height: 100vh;
}
.help-wrapper {
  position: absolute;
  max-width: 38rem;
  padding: 0 0.5rem;
  margin: 20vh auto 100%;
  inset: 0;
  z-index: 12;
}
.help-wrapper div {
  padding: 1rem 0;
  background-color: var(--c-white-light);
  font-size: var(--font-size);
  color: var(--c-text);
  border-radius: 8px;
  box-shadow: 0 0 5px 5px rgba(0, 0, 0, 0.33);
}
.pis-40px {
  padding-inline-start: 40px;
}
.step {
  margin-top: 8px;
}
</style>
