<template>
  <div v-if="tabs()">
    <div class="right-pane-tabs">
      <div
        v-for="tab in tabs()"
        :key="tab"
        class="right-pane-tab"
        :class="{ active: currentTab === tab }"
        @click="currentTab = tab"
      >
        <span class="iconify" :data-icon="getFileType(tab)"></span>
        {{ tab }}
      </div>
    </div>
    <div class="right-pane-contexts" v-if="currentCode()">
      <KeepAlive>
        <CodeBlock :lang="getLang" :code="formattedCode()" />
      </KeepAlive>
    </div>
    <div v-else class="loading-code">
      <h2>Loading Code...</h2>
    </div>
  </div>
  <div v-else>
    <Instruction />
  </div>
</template>

<script>
import CodeBlock from './CodeBlock.vue'
import Instruction from './Instruction.vue'
import { store, __DEV_CONFIG_FILE__ } from '../store'
import { computed, ref } from 'vue'
import '@iconify/iconify'

export default {
  components: { CodeBlock, Instruction },
  setup() {
    const currentTab = ref('README.md')
    const tabs = () => {
      if (store.config.template) {
        return Object.keys(store.code)
      }
    }
    // search more file types mapping on
    // https://icones.js.org/collection/vscode-icons
    const fileTypes = {
      py: 'python',
      md: 'markdown',
      json: 'json',
      txt: 'text',
      yml: 'yaml',
      yaml: 'yaml'
    }

    const getFileType = (tab) => {
      const fileType = tab.split('.')[1]
      return `vscode-icons:file-type-${fileTypes[fileType]}`
    }
    const getLang = computed(() => currentTab.value.split('.')[1])
    const formattedCode = () => store.code[currentTab.value].trim()
    const currentCode = () => {
      const code = store.code[currentTab.value]
      if (code) {
        return code
      }
      currentTab.value = 'README.md'
      return store.code[currentTab.value]
    }
    return {
      currentCode,
      currentTab,
      tabs,
      getLang,
      getFileType,
      formattedCode
    }
  }
}
</script>

<style scoped>
.right-pane-tabs {
  display: flex;
  flex-direction: row;
  overflow-x: auto;
  overflow-y: hidden;
  scrollbar-width: none;
  border-bottom: 1px solid var(--c-white-dark);
}
.right-pane-tabs::-webkit-scrollbar {
  display: none;
}
.right-pane-tabs,
.right-pane-contexts {
  margin-right: 1.5rem;
}
.right-pane-tab {
  display: flex;
  place-items: center;
  background-color: var(--background-color-primary);
  cursor: pointer;
  color: var(--c-text);
  font-family: var(--font-family-base);
  font-size: var(--font-size);
  text-align: center;
  padding: 0.4rem 0.8rem;
  border-bottom: 3px solid transparent;
}
.right-pane-tab:hover,
.active {
  color: var(--c-brand-red);
  border-bottom-color: var(--c-brand-red);
}
.iconify {
  margin-right: 6px;
}
/* media queries */
@media (max-width: 915px) {
  .right-pane-contexts {
    height: 100%;
    margin: 0;
  }
}
.loading-code {
  max-width: 75%;
  margin: 25% auto;
  text-align: center;
  color: #a1a1aa;
}
</style>
