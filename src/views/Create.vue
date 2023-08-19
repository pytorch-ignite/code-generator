<template>
  <main>
    <NavBar />
    <SplitPane>
      <template #left>
        <PaneLeft />
      </template>
      <template #right>
        <PaneRight />
      </template>
    </SplitPane>
    <Footer />
  </main>
</template>

<script>
import NavBar from '../components/NavBar.vue'
import SplitPane from '../components/PaneSplit.vue'
import PaneRight from '../components/PaneRight.vue'
import PaneLeft from '../components/PaneLeft.vue'
import Footer from '../components/Footer.vue'
import { defineAsyncComponent, onUnmounted } from 'vue'
import { default_config, store } from '../store'

export default {
  components: {
    NavBar,
    SplitPane,
    PaneRight,
    PaneLeft,
    Footer
  },
  setup() {
    onUnmounted(() => {
      // delete each property of config
      // since `store.config` is being watched in store.js
      // and Vue watch function does not tracked
      // if we reassign `store.config` (i.e. store.config = {})
      for (const config in store.config) {
        delete store.config[config]
      }
      // since we delete each property,
      // it is better to reassign the initial values
      // which are defined in store.js
      for (const key in default_config) {
        store.config[key] = default_config[key]
      }
    })
  }
}
</script>
