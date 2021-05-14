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
import NavBar from './components/NavBar.vue'
import SplitPane from './components/PaneSplit.vue'
import PaneRight from './components/PaneRight.vue'
import PaneLeft from './components/PaneLeft.vue'
import Footer from './components/Footer.vue'

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

<style>
*,
::before,
::after {
  box-sizing: border-box;
  border-width: 0;
}
::selection {
  color: var(--c-white-light);
  background: var(--c-brand-red);
}
:root {
  --c-white: #fff;
  --c-white-light: #f6f6f6;
  --c-white-dark: #e4e4e7;
  --c-brand-red: #ee4c2c;
  --c-brand-yellow: #eaa700;
  --c-text: #475569;
  --font-size: 1rem;
  --font-family-base: 'Inter', Avenir, -apple-system, BlinkMacSystemFont,
    'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Fira Sans', 'Droid Sans',
    'Helvetica Neue', sans-serif;
  --code-font-family: Menlo, Monaco, Consolas, 'Courier New', monospace;
  --code-font-size: 0.85em;
  --code-line-height: 24px;
  --code-text-light: #476582;
  --code-inline-bg-color: rgba(27, 31, 35, 0.05);
}
body {
  font-family: var(--font-family-base);
  font-size: var(--font-size);
  line-height: 1.5;
  margin: 0;
  height: 100%;
  color: var(--c-text);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
h1 {
  font-weight: 600;
}
h2,
h3,
h4,
h5,
h6 {
  font-weight: 500;
}
@media (prefers-reduced-motion) {
  :focus {
    border-radius: 3px;
    transition: outline-offset 0.25s ease;
    outline-offset: 5px;
    outline: 2px solid var(--c-brand-yellow);
  }
}
/* margin for left pane tabs */
.tab {
  --left-pane-margin-x: 1.5rem;
  margin: 0 var(--left-pane-margin-x);
  padding-bottom: 2rem;
}
/* overriding prismjs defaults */
pre,
code {
  font-family: var(--code-font-family) !important;
  font-size: var(--code-font-size) !important;
}
/* for three backticks code block */
code {
  margin: 0;
  border-radius: 3px;
  padding: 0.25rem 0.5rem;
  color: var(--code-text-light);
  background-color: var(--code-inline-bg-color);
}
</style>
