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
  <footer class="footer-and-badge">
    BSD-3-Clause License | Copyright &copy; 2021-present PyTorch-Ignite Team &
    Code-Generator Contributors
  </footer>
</template>

<script>
import NavBar from './components/NavBar.vue'
import SplitPane from './components/PaneSplit.vue'
import PaneRight from './components/PaneRight.vue'
import PaneLeft from './components/PaneLeft.vue'

export default {
  components: {
    NavBar,
    SplitPane,
    PaneRight,
    PaneLeft
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
  --font-family-base: Avenir, -apple-system, BlinkMacSystemFont, 'Segoe UI',
    Roboto, Oxygen, Ubuntu, Cantarell, 'Fira Sans', 'Droid Sans',
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
@media (prefers-reduced-motion) {
  :focus {
    border-radius: 3px;
    transition: outline-offset 0.25s ease;
    outline-offset: 5px;
    outline: 2px solid var(--c-brand-yellow);
  }
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
.footer-and-badge {
  border-top: 1px solid var(--c-white-dark);
  text-align: center;
  font-size: 0.875rem;
  line-height: 1.25rem;
  padding: 3rem 1.5rem;
}
</style>
