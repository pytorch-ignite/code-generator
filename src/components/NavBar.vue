<template>
  <nav class="nav-bar">
    <h1>
      <RouterLink to="/">
        <img
          src="../assets/ignite_logomark.svg"
          alt="PyTorch-Ignite logo"
          width="50"
          height="50"
        />
        <span class="pname">Code Generator</span>
      </RouterLink>
    </h1>
    <div class="right-side-badges">
      <NavIgniteDocs />
      <NavIgniteWebsite />
      <NavHelp />
      <NavGitHub />
      <NavTwitter />
      <NavDiscord />
      <a
        :href="`https://github.com/pytorch-ignite/code-generator/commit/${currentCommit}`"
        target="_blank"
        rel="noopener noreferrer"
        class="version external-links"
      >
        v{{ version }}@{{ currentCommit.slice(0, 7) }}
      </a>
      <NavContributors />
    </div>
  </nav>
</template>

<script>
import { version } from '../../package.json'
import NavDiscord from './NavDiscord.vue'
import NavDownload from './NavDownload.vue'
import NavColab from './NavColab.vue'
import NavGitHub from './NavGitHub.vue'
import NavIgniteWebsite from './NavIgniteWebsite.vue'
import NavIgniteDocs from './NavIgniteDocs.vue'
import NavTwitter from './NavTwitter.vue'
import NavHelp from './NavHelp.vue'
import NavContributors from './NavContributors.vue'

export default {
  components: {
    NavDiscord,
    NavDownload,
    NavColab,
    NavGitHub,
    NavIgniteWebsite,
    NavTwitter,
    NavHelp,
    NavIgniteDocs,
    NavContributors
  },
  setup() {
    const currentCommit = __COMMIT__ // from vite.config.js

    return { version, currentCommit }
  }
}
</script>

<style scoped>
@import url('./css/nav-right.css');

h1 {
  margin: 0;
  font-weight: normal;
}
h1 img {
  vertical-align: middle;
  position: relative;
  top: -5px;
}
.nav-bar {
  display: flex;
  align-items: center;
  padding: 0.5rem 1.5rem 0;
  justify-content: space-between;
  border-bottom: 1px solid var(--c-white-dark);
}
.right-side-badges {
  display: flex;
  align-items: right;
  font-size: 0.95em;
}
/* media queries */
@media (max-width: 915px) {
  .pname {
    display: none;
  }
  .nav-bar {
    position: fixed;
    z-index: 6;
    width: 100%;
    padding: 0.5rem 0.5rem 0;
    background-color: var(--c-white);
  }
}
</style>
