<template>
  <form class="inputs-wrapper" @submit.prevent="saveInput">
    <p v-for="(o, index) in options" :key="index">
      <input
        type="radio"
        v-model="inputted"
        :name="saveKey"
        :id="o.description"
        :required="required"
        :value="o.name"
      />
      <label :for="o.description">
        {{ o.description }}
      </label>
      {{ isRequired }}
    </p>
  </form>
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
      required: false
    }
  },
  setup(props) {
    const { options, saveKey, required } = toRefs(props)
    const inputted = ref('')

    const saveInput = () => saveConfig(saveKey.value, inputted.value)
    const isRequired = computed(() => (required.value ? '*' : ''))
    return {
      options,
      saveKey,
      required,
      inputted,
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
