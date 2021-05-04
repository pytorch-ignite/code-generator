<template>
  <div class="right-pane-tabs">
    <div
      v-for="tab in tabs"
      :key="tab"
      class="right-pane-tab"
      :class="{ active: currentTab === tab }"
      @click="currentTab = tab"
    >
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

export default {
  components: { CodeBlock },
  setup() {
    const currentTab = ref('README.md')
    const tabs = ref(getTemplateFileNames())

    const getLang = computed(() => {
      return currentTab.value.split('.')[1]
    })
    const formattedCode = () => {
      return store.code[currentTab.value]
    }
    return { currentTab, tabs, getLang, formattedCode }
  }
}
</script>

<style scoped>
.right-pane-tabs {
  border-bottom: 1px solid var(--c-white-dark);
}
.right-pane-tabs,
.right-pane-contexts {
  padding-right: 1.5rem;
}
.right-pane-tab {
  display: inline-block;
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
</style>
