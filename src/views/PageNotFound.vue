<template>
  <main>
    <NavBar />
    <div class="heading">
      <h1>404 Page Not Found</h1>
      <p>
        Oops we couldn't find that page. Try going
        <RouterLink to="/" class="link alt" :style="learnMore">home</RouterLink>
      </p>
    </div>
    <Footer />
  </main>
</template>

<script>
import NavBar from '../components/NavBar.vue'
import SplitPane from '../components/PaneSplit.vue'
import PaneRight from '../components/PaneRight.vue'
import PaneLeft from '../components/PaneLeft.vue'
import Footer from '../components/Footer.vue'
import { onUnmounted } from 'vue'
import { store } from '../store'

export default {
  components: {
    NavBar,
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
      store.config.template = ''
      store.config.include_test = false
      store.config.output_dir = './logs'
      store.config.log_every_iters = 2
    })
  }
}
</script>

<style scoped>
h1 {
  color: orange;
}
.heading {
  max-width: 75vw;
  margin: auto;
  text-align: center;
}
.heading .alt {
  background: var(--c-white);
  color: var(--c-brand-red);
}
</style>
