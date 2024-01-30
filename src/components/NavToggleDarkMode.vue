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
      class="h-6 w-6 hidden"
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

.hidden {
  display: none;
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

@media (min-width: 640px) {
  .sm\:grid-cols-2 {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .sm\:grid-cols-3 {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }

  .sm\:col-start-2 {
    grid-column-start: 2;
  }

  .sm\:row-span-2 {
    -ms-grid-row-span: span 2 / span 2;
    grid-row: span 2 / span 2;
  }
}

@media (min-width: 1024px) {
  .lg\:block {
    display: block;
  }

  .group:hover .lg\:group-hover\:block {
    display: block;
  }

  .lg\:flex {
    display: -webkit-box;
    display: -ms-flexbox;
    display: -webkit-flex;
    display: flex;
  }

  .lg\:grid {
    display: -ms-grid;
    display: grid;
  }

  .lg\:hidden {
    display: none;
  }

  .lg\:text-3xl {
    font-size: 1.875rem;
    line-height: 2.25rem;
  }

  .lg\:text-xl {
    font-size: 1.25rem;
    line-height: 1.75rem;
  }

  .lg\:text-2xl {
    font-size: 1.5rem;
    line-height: 2rem;
  }

  .lg\:p-2 {
    padding: 0.5rem;
  }

  .lg\:absolute {
    position: absolute;
  }

  .lg\:sticky {
    position: -webkit-sticky;
    position: sticky;
  }

  .lg\:w-3\/5 {
    width: 60%;
  }

  .lg\:grid-flow-row-dense {
    grid-auto-flow: row dense;
  }

  .lg\:grid-cols-2 {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .lg\:grid-cols-3 {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }

  .lg\:col-span-1 {
    -ms-grid-column-span: span 1 / span 1;
    grid-column: span 1 / span 1;
  }

  .lg\:col-start-2 {
    grid-column-start: 2;
  }

  .lg\:col-start-1 {
    grid-column-start: 1;
  }
}

@media (min-width: 1280px) {
  .xl\:grid-cols-\[1fr\2c 3fr\2c 1fr\] {
    grid-template-columns: 1fr 3fr 1fr;
  }
}

@media (max-width: 1023.9px) {
  .\<lg\:border-r {
    border-right-width: 1px;
  }

  .\<lg\:hidden {
    display: none;
  }

  .\<lg\:w-75 {
    width: 18.75rem;
  }

  .\<lg\:-translate-x-full {
    --tw-translate-x: -100%;
  }
}

@media (max-width: 639.9px) {
  .\<sm\:px-4 {
    padding-left: 1rem;
    padding-right: 1rem;
  }
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
      userTheme: 'light-theme'
    }
  },

  methods: {
    toggleTheme() {
      const sun = document.getElementById('sun')
      const moon = document.getElementById('moon')
      const activeTheme = localStorage.getItem('user-theme')
      if (activeTheme === 'light-theme') {
        this.setTheme('dark-theme')
        this.toggleClassList()
      } else {
        this.setTheme('light-theme')
        this.toggleClassList()
      }
    },

    getTheme() {
      return localStorage.getItem('user-theme')
    },

    setTheme(theme) {
      localStorage.setItem('user-theme', theme)
      this.userTheme = theme
      document.documentElement.className = theme
    },

    toggleClassList() {
      sun.classList.toggle('hidden')
      moon.classList.toggle('hidden')
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
