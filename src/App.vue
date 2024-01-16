<template>
  <RouterView v-slot="{ Component }">
    <transition name="slide-fade" mode="out-in">
      <component :is="Component" />
    </transition>
  </RouterView>
</template> 

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
  --c-text: white;
  --font-size: 1rem;
  --font-family-base: 'Inter', Avenir, -apple-system, BlinkMacSystemFont,
    'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Fira Sans', 'Droid Sans',
    'Helvetica Neue', sans-serif;
  --code-font-family: Menlo, Monaco, Consolas, 'Courier New', monospace;
  --code-font-size: 0.85em;
  --code-line-height: 24px;
  --code-text-light: #476582;
  --code-inline-bg-color: rgba(27, 31, 35, 0.05);
  --accent-color: #cacaca;
  --background-color-primary:  #1e1e1e;
  --background-color-secondary: #fafafa;
}

:root.dark-theme {
  --background-color-primary: #1e1e1e;
  --background-color-secondary: #2d2d30;
  --accent-color: #3f3f3f;
  --text-primary-color: #ddd;
  --c-text:white;
}

body {
  font-family: var(--font-family-base);
  font-size: var(--font-size);
  line-height: 1.5;
  margin: 0;
  height: 100%;
  color: var(--c-text);
  background-color:  var(--background-color-primary);
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
@media (max-width: 915px) {
  h1 {
    font-size: 1.5rem;
  }
  h2 {
    font-size: 1.25rem;
  }
  h3 {
    font-size: 1.125rem;
  }
}
a {
  text-decoration: none;
  color: var(--c-text);
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
.slide-fade-leave-active,
.slide-fade-enter-active {
  transition: all 0.25s ease-out;
}
.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateY(10px);
  opacity: 0;
}
</style>
