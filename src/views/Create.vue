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

export default {
  components: {
    NavBar,
    SplitPane,
    PaneRight,
    PaneLeft,
    Footer
  }
}
</script>
