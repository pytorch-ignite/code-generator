<template>
  <div class="left-pane-tabs">
    <div
      v-for="tab in tabs"
      :key="tab"
      class="left-pane-tab"
      :class="{ active: currentTab === tab }"
      @click="currentTab = tab"
    >
      {{ tab }}
    </div>
  </div>
  <div class="left-pane-contexts">
    <KeepAlive>
      <component :is="currentTabComponent"></component>
    </KeepAlive>
  </div>
</template>

<script>
import TabModel from './TabModel.vue'
import TabTraining from './TabTraining.vue'
import TabHandlers from './TabHandlers.vue'
import TabLoggers from './TabLoggers.vue'
import { computed, ref } from 'vue'

export default {
  components: { TabModel, TabTraining, TabLoggers, TabHandlers },
  setup() {
    const currentTab = ref('Model')
    const tabs = ref(['Model', 'Training', 'Handlers', 'Loggers'])

    // computed properties
    const currentTabComponent = computed(() => {
      return 'tab-' + currentTab.value.toLowerCase()
    })

    return { currentTab, tabs, currentTabComponent }
  }
}
</script>

<style scoped>
.left-pane-tabs {
  border-bottom: 1px solid var(--c-white-dark);
}
.left-pane-tabs,
.left-pane-contexts {
  padding-left: 1.5rem;
}
.left-pane-tab {
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
.left-pane-tab:hover,
.active {
  color: var(--c-brand-red);
  border-bottom-color: var(--c-brand-red);
}
.left-pane-contexts {
  height: 100vh;
  overflow: auto;
}
</style>
