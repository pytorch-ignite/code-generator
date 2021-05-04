<template>
  <form class="selector">
    <p>
      <label :for="selectId">
        {{ label }} – <code>{{ saveKey }}</code> {{ isRequired }}
      </label>
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
import { computed, ref, toRefs } from 'vue'
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
    }
  },
  setup(props) {
    const { label, options, required, saveKey } = toRefs(props)
    const selected = ref('')

    const saveSelected = () => saveConfig(saveKey.value, selected.value)
    const selectId = computed(() => label.value + '-select')
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
  appearance: none;
  background: var(--c-white-light);
  border-radius: 3px;
  color: var(--c-text);
  cursor: pointer;
  font-family: var(--font-family-base);
  font-size: var(--font-size);
  padding: 0.5rem 1rem;
  text-align: center;
  width: 100%;
}
.selector::after {
  content: '';
  position: absolute;
  right: 1rem;
  bottom: 16px;
  border-top: 6px solid var(--c-brand-red);
  border-left: 4px solid transparent;
  border-right: 4px solid transparent;
  border-bottom: 0;
  vertical-align: middle;
}
</style>
