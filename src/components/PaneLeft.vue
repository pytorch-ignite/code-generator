<template>
  <div class="left-pane-tabs">
    <div
      v-for="tab in tabs"
      :key="tab"
      class="left-pane-tab"
      :class="{ active: currentTab === tab, disable: !hasTemplate }"
      @click="switchTab(tab)"
    >
      {{ tab }}
    </div>
  </div>
  <div class="left-pane-contexts">
    <div class="download-n-colab">
      <NavDownload />
      <NavColab />
    </div>
    <KeepAlive>
      <component :is="currentTabComponent" />
    </KeepAlive>
  </div>
  <Message :message="msg.content" :color="msg.color" />
</template>

<script>
import TabTemplates from './TabTemplates.vue'
import TabTraining from './TabTraining.vue'
import TabHandlers from './TabHandlers.vue'
import TabLoggers from './TabLoggers.vue'
import Message from './Message.vue'
import NavDownload from './NavDownload.vue'
import NavColab from './NavColab.vue'
import { computed, ref } from 'vue'
import { msg, store } from '../store.js'

export default {
  components: {
    TabTemplates,
    TabTraining,
    TabLoggers,
    TabHandlers,
    Message,
    NavDownload,
    NavColab
  },
  setup() {
    const currentTab = ref('Templates')
    const tabs = ['Templates', 'Training', 'Handlers', 'Loggers']

    // computed properties
    const currentTabComponent = computed(() => {
      return 'tab-' + currentTab.value.toLowerCase()
    })

    const switchTab = (tab) => {
      if (store.config.template) {
        currentTab.value = tab
      }
    }
    const hasTemplate = computed(() => {
      return store.config.template
    })

    return {
      currentTab,
      tabs,
      currentTabComponent,
      msg,
      switchTab,
      hasTemplate
    }
  }
}
</script>

<style scoped>
.left-pane-tabs {
  display: flex;
  flex-direction: row;
  overflow-x: auto;
  overflow-y: hidden;
  scrollbar-width: none;
  border-bottom: 1px solid var(--c-white-dark);
}
.left-pane-tabs::-webkit-scrollbar {
  display: none;
}
.left-pane-tabs,
.left-pane-contexts {
  padding-left: 1.5rem;
}
.left-pane-tab {
  background-color: var(--c-white);
  cursor: pointer;
  color: var(--c-text);
  font-family: var(--font-family-base);
  font-size: var(--font-size);
  text-align: center;
  padding: 0.4rem 0.8rem;
  border-bottom: 3px solid transparent;
}
.disable {
  cursor: not-allowed;
}
.active {
  cursor: pointer;
}
.left-pane-tab:hover,
.active {
  color: var(--c-brand-red);
  border-bottom-color: var(--c-brand-red);
}
.left-pane-contexts {
  height: 100vh;
  overflow: auto;
}
/* media queries */
@media (max-width: 915px) {
  .left-pane-contexts {
    height: 100%;
    padding: 0;
    margin-bottom: 2.5rem;
  }
}
.download-n-colab {
  display: flex;
  align-items: center;
  justify-content: space-evenly;
  margin-top: 1rem;
  padding-bottom: 1em;
  border-bottom: 1px solid #ddd;
}
</style>
