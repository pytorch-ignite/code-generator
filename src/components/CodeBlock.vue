<template>
  <div class="code-block-wrapper">
    <div :class="className">
      <button class="copy" @click="copyCode">{{ copyText }}</button>
      <pre
        :class="className"
      ><code :class="className" v-html="highlightCode"></code></pre>
      <div class="line-numbers-wrapper">
        <template v-for="i in getLineNumbers" :key="i">
          <span class="line-numbers">{{ i }}</span>
          <br />
        </template>
      </div>
    </div>
  </div>
</template>

<script>
import { highlight, languages } from 'prismjs'
import 'prismjs/components/prism-json'
import 'prismjs/components/prism-yaml'
import 'prismjs/components/prism-python'
import 'prismjs/components/prism-markdown'
import 'prismjs/themes/prism-tomorrow.css'
import { computed, ref, toRefs } from 'vue'
import { msg } from '../store.js'

export default {
  props: {
    lang: {
      type: String,
      default: 'py'
    },
    code: {
      type: String,
      required: true
    }
  },
  setup(props) {
    const { lang, code } = toRefs(props)
    const copyText = ref('Copy')

    // computed properties
    const className = computed(() => {
      if (props.lang === 'txt') {
        return 'language-text'
      }
      return `language-${lang.value}`
    })
    const highlightCode = computed(() => {
      if (lang.value === 'txt') {
        return highlight(code.value, {}, 'txt')
      }
      return highlight(code.value, languages[lang.value], lang.value)
    })
    const getLineNumbers = computed(() => {
      return code.value.split('\n').length
    })
    const copyCode = async () => {
      try {
        await navigator.clipboard.writeText(code.value)
        msg.color = 'blue'
        msg.showMsg = true
        msg.content = 'Code has been copied to Clipboard.'
      } catch (e) {
        console.error(e)
      }
      copyText.value = 'Copied'
      setTimeout(() => (copyText.value = 'Copy'), 1500)
    }

    return { className, highlightCode, getLineNumbers, copyCode, copyText }
  }
}
</script>

<style scoped>
.code-block-wrapper {
  overflow: auto;
  height: 100vh;
}
div[class*='language-'] {
  position: relative;
}

.copy {
  right: 3em !important;
  background: transparent;
  padding-top: 0;
  padding-bottom: 0;
  line-height: inherit;
  cursor: pointer;
}

div[class*='language-']::before,
.copy {
  position: absolute;
  color: var(--c-white-dark);
  font-size: 0.75rem;
  z-index: 3;
  right: 1em;
  top: 0.5em;
}

[class*='language-'] pre {
  position: relative;
  margin: 0;
  padding: 1.25rem 1.5rem 1.25rem 1rem;
  margin-left: 3.5rem;
  vertical-align: middle;
  overflow: auto;
  border-radius: 0 3px 3px 0;
  font-size: var(--font-size) !important;
}

/* font-size is pre's font-size * code's font-size */
[class*='language-'] code {
  padding: 0;
  border-radius: 0;
  line-height: var(--code-line-height);
}

.line-numbers-wrapper {
  position: absolute;
  top: 0;
  bottom: 0;
  border-right: 1px solid rgba(0, 0, 0, 0.5);
  padding: 1.25rem 0;
  width: 3.5rem;
  text-align: center;
  font-family: var(--code-font-family);
  font-size: var(--font-size);
  line-height: var(--code-line-height);
  color: var(--c-white-dark);
  background-color: #2d2d2d;
}

/* font-size is .line-numbers-wrapper's font-size * .line-numbers's font-size */
.line-numbers {
  position: relative;
  font-size: var(--code-font-size);
  -webkit-user-select: none;
  user-select: none;
}

div[class~='language-md']::before,
div[class~='language-markdown']::before {
  content: 'md';
}

div[class~='language-txt']::before,
div[class~='language-text']::before {
  content: 'txt';
}

div[class~='language-json']::before {
  content: 'json';
}

div[class~='language-py']::before,
div[class~='language-python']::before {
  content: 'py';
}

div[class~='language-sh']::before,
div[class~='language-bash']::before {
  content: 'sh';
}

div[class~='language-yml']::before,
div[class~='language-yaml']::before {
  content: 'yaml';
}
/* media queries */
@media (max-width: 915px) {
  .code-block-wrapper {
    height: 100%;
  }
}
</style>
