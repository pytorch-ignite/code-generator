<template>
  <form class="selector">
    <p>
      <label :for="selectId">
        {{ label }}
      </label>
      {{ isRequired }}
    </p>
    <select
      :id="selectId"
      :required="required"
      v-model.trim="selected"
      @change.prevent="saveSelected"
    >
      <option disabled value="">
        --- Choose {{ toTitleCase(saveKey) }} ---
      </option>
      <option :value="o" v-for="(o, index) in options" :key="index">
        {{ toTitleCase(o) }}
      </option>
    </select>
  </form>
</template>

<script>
import { computed, onMounted, ref, toRefs } from 'vue'
import { saveConfig } from '../store.js'
export default {
  props: {
    label: {
      type: String,
      required: true
    },
    options: {
      type: Array,
      required: true
    },
    required: {
      type: Boolean,
      default: false
    },
    saveKey: {
      type: String,
      required: true
    },
    defaultV: {
      type: String,
      default: ''
    }
  },
  setup(props) {
    const { label, options, required, saveKey, defaultV } = toRefs(props)
    const selected = ref('')

    onMounted(() => {
      if (defaultV.value.length > 0) {
        selected.value = defaultV.value
        saveSelected()
      }
    })
    const saveSelected = () => {
      if (typeof selected.value === 'string') {
        saveConfig(saveKey.value, selected.value.toLowerCase())
      }
      saveConfig(saveKey.value, selected.value)
    }
    const selectId = computed(() => saveKey.value + '-select')
    const isRequired = computed(() => (required.value ? '*' : ''))
    return {
      saveKey,
      label,
      options,
      required,
      selected,
      selectId,
      isRequired,
      toTitleCase,
      saveConfig,
      saveSelected
    }
  }
}

function toTitleCase(v) {
  return v[0].toUpperCase() + v.slice(1)
}
</script>

<style scoped>
.selector {
  position: relative;
}
.selector select {
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  background: var(--c-white-light);
  border-radius: 3px;
  color: var(--c-text);
  cursor: pointer;
  font-family: var(--font-family-base);
  font-size: var(--font-size);
  padding: 0.5rem 1rem;
  text-align: center;
  text-align-last: center;
  width: 100%;
}
.selector::after {
  content: '';
  position: absolute;
  right: 1rem;
  bottom: 15px;
  border-top: 6px solid var(--c-brand-red);
  border-left: 4px solid transparent;
  border-right: 4px solid transparent;
  border-bottom: 0;
  vertical-align: middle;
}
</style>
