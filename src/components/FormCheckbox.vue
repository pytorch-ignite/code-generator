<template>
  <form class="checkbox-wrapper">
    <p>
      <label :for="checkboxId">
        <input
          type="checkbox"
          :id="checkboxId"
          :required="required"
          v-model="checked"
          @change="saveChecked"
        />
        {{ label }} – <code>{{ saveKey }}</code> {{ isRequired }}
      </label>
    </p>
  </form>
</template>

<script>
import { ref, toRefs, computed } from 'vue'
import { saveConfig } from '../store.js'

export default {
  props: {
    label: {
      type: String,
      required: true
    },
    saveKey: {
      type: String,
      required: true
    },
    required: {
      type: Boolean,
      required: false
    }
  },
  setup(props) {
    const { label, saveKey, required } = toRefs(props)
    const checked = ref(false)

    const saveChecked = () => saveConfig(saveKey.value, checked.value)
    const checkboxId = computed(() => label.value + '-checkbox')
    const isRequired = computed(() => (required.value ? '*' : ''))

    return {
      label,
      saveKey,
      required,
      checked,
      saveChecked,
      checkboxId,
      isRequired
    }
  }
}
</script>

<style scoped>
.checkbox-wrapper label {
  display: block;
  margin-top: 0.5rem;
  width: max-content;
}
</style>
