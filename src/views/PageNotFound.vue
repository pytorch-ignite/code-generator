<template>
  <main>
    <NavBar />
    <div class="heading">
      <h1>404 Page Not Found</h1>
      <p>Oops! We couldn't find that page.</p>
      <p>
        Go back to the
        <RouterLink to="/" class="link alt" :style="learnMore"
          >homepage</RouterLink
        >.
      </p>
    </div>
    <Footer class="footer" />
  </main>
</template>

<script>
import NavBar from '../components/NavBar.vue'
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
  color: var(--c-brand-red);
}
.heading {
  padding-top: 12rem;
  max-width: 75vw;
  margin: auto;
  text-align: center;
}
.heading .alt {
  background: var(--c-white);
  color: var(--c-brand-red);
}

.footer {
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 100vw;
  margin: auto;
}
</style>
