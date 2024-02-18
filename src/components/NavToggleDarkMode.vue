<template>
  <button
    aria-label="Toggle Color Scheme"
    @click="toggleTheme"
    title="Toggle Light/Dark mode"
    class="sun-moon-btn"
    id="toggleDark"
  >
    <svg
      id="sun"
      v-show="isDark"
      xmlns="http://www.w3.org/2000/svg"
      class="h-6 w-6"
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-width="2"
        d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"
      />
    </svg>

    <svg
      id="moon"
      xmlns="http://www.w3.org/2000/svg"
      v-show="!isDark"
      class="h-6 w-6"
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-width="2"
        d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"
      />
    </svg>
  </button>
</template>

<style scoped>
@import url('./css/nav-right.css');

*,
::before,
::after {
  -webkit-box-sizing: border-box;
  box-sizing: border-box;
  border-width: 0;
  border-style: solid;
  border-color: #e5e7eb;
}

* {
  --tw-ring-inset: var(--tw-empty, /*!*/ /*!*/);
  --tw-ring-offset-width: 0px;
  --tw-ring-offset-color: #fff;
  --tw-ring-color: rgba(59, 130, 246, 0.5);
  --tw-ring-offset-shadow: 0 0 #0000;
  --tw-ring-shadow: 0 0 #0000;
  --tw-shadow: 0 0 #0000;
}

button {
  font-family: inherit;
  font-size: 100%;
  line-height: 1.15;
  margin: 0;
  text-transform: none;
  background-color: transparent;
  background-image: none;
  padding: 0;
  line-height: inherit;
  color: inherit;
}

button,
[type='button'] {
  appearance: button;
  -webkit-appearance: button;
}

button,
[role='button'] {
  cursor: pointer;
}

svg {
  display: block;
  vertical-align: middle;
}

.before\:hidden::before {
  display: none;
}
.h-6 {
  height: 1.5rem;
}
.w-6 {
  width: 1.5rem;
}
</style>

<script>
export default {
  mounted() {
    const initUserTheme = this.getTheme() || this.getMediaPreference()
    this.setTheme(initUserTheme)
  },

  data() {
    return {
      userTheme: 'light-theme',
      isDark: true
    }
  },

  methods: {
    toggleTheme() {
      const activeTheme = localStorage.getItem('user-theme')
      if (activeTheme === 'light-theme') {
        this.setTheme('dark-theme')
      } else {
        this.setTheme('light-theme')
      }
    },

    getTheme() {
      return localStorage.getItem('user-theme')
    },

    setTheme(theme) {
      localStorage.setItem('user-theme', theme)
      this.userTheme = theme
      document.documentElement.className = theme
      this.isDark = !this.isDark
    },

    getMediaPreference() {
      const hasDarkPreference = window.matchMedia(
        '(prefers-color-scheme: dark)'
      ).matches
      if (hasDarkPreference) {
        return 'dark-theme'
      } else {
        return 'light-theme'
      }
    }
  }
}
</script>
