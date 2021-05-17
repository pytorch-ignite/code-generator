<template>
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
</template>

<script>
import NavBar from './NavBar.vue'
import SplitPane from './PaneSplit.vue'
import PaneRight from './PaneRight.vue'
import PaneLeft from './PaneLeft.vue'
import Footer from './Footer.vue'

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
