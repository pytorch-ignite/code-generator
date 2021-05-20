<template>
  <div class="inputs-wrapper">
    <p v-for="(o, index) in options" :key="index">
      <input
        type="radio"
        v-model="picked"
        :name="saveKey"
        :id="o.description"
        :required="required"
        :value="o.name"
        @change.prevent="saveInput"
      />
      <label :for="o.description">
        {{ o.description }}
      </label>
      {{ isRequired }}
    </p>
  </div>
</template>

<script>
import { computed, ref, toRefs } from 'vue'
import { saveConfig } from '../store'
export default {
  props: {
    required: {
      type: Boolean,
      default: false
    },
    saveKey: {
      type: String,
      required: true
    },
    options: {
      type: Array,
      required: true
    },
    defaultV: {
      type: String,
      default: ''
    }
  },
  setup(props) {
    const { options, saveKey, required, defaultV } = toRefs(props)
    const picked = ref('')
    if (defaultV.value.length > 0) {
      picked.value = defaultV.value
      saveConfig(saveKey.value, picked.value)
    }

    const saveInput = () => saveConfig(saveKey.value, picked.value)
    const isRequired = computed(() => (required.value ? '*' : ''))
    return {
      options,
      saveKey,
      required,
      picked,
      saveInput,
      isRequired
    }
  }
}
</script>

<style scoped>
input {
  font-family: var(--font-family-base);
  font-size: var(--font-size);
}
input[type='radio'] {
  margin-right: 0.5rem;
}
</style>
