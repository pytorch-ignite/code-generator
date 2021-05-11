<template>
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
  <div class="right-pane-contexts">
    <KeepAlive>
      <CodeBlock :lang="getLang" :code="formattedCode()" />
    </KeepAlive>
  </div>
</template>

<script>
import CodeBlock from './CodeBlock.vue'
import { getTemplateFileNames, store } from '../store'
import { computed, ref } from 'vue'
import '@iconify/iconify'

export default {
  components: { CodeBlock },
  setup() {
    const currentTab = ref('README.md')
    // search more file types mapping on
    // https://icones.js.org/collection/vscode-icons
    const fileTypes = {
      py: 'python',
      md: 'markdown',
      json: 'json',
      txt: 'text'
    }

    const getLang = computed(() => {
      return currentTab.value.split('.')[1]
    })
    const getFileType = (tab) => {
      const fileType = tab.split('.')[1]
      return `vscode-icons:file-type-${fileTypes[fileType]}`
    }
    const tabs = () => getTemplateFileNames()
    const formattedCode = () => store.code[currentTab.value].trim()
    return { currentTab, tabs, getLang, getFileType, formattedCode }
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
.right-pane-tabs,
.right-pane-contexts {
  padding-right: 1.5rem;
}
.right-pane-tab {
  display: flex;
  place-items: center;
  background-color: var(--c-white);
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
@media (max-width: 768px) {
  .right-pane-contexts {
    height: 100%;
    padding: 0;
  }
}
</style>
