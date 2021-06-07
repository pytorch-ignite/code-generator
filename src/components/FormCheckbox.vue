<template>
  <form class="checkbox-wrapper">
    <p>
      <label :for="checkboxId">
        <input
          type="checkbox"
          :id="checkboxId"
          :required="required"
          :disabled="noTemplate"
          v-model="checked"
          @change.prevent="saveChecked"
        />
        {{ label }}
      </label>
      {{ isRequired }}
    </p>
  </form>
</template>

<script>
import { ref, toRefs, computed, onMounted } from 'vue'
import { saveConfig, store } from '../store.js'

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
    },
    defaultV: {
      type: Boolean,
      default: false
    }
  },
  setup(props) {
    const { label, saveKey, required, defaultV } = toRefs(props)
    const checked = ref(false)

    onMounted(() => {
      if (defaultV.value) {
        checked.value = defaultV.value
        saveChecked()
      }
    })
    const saveChecked = () => saveConfig(saveKey.value, checked.value)
    const checkboxId = computed(() => saveKey.value + '-checkbox')
    const isRequired = computed(() => (required.value ? '*' : ''))
    const noTemplate = computed(() => !store.config.template)

    return {
      label,
      saveKey,
      required,
      checked,
      saveChecked,
      checkboxId,
      isRequired,
      noTemplate
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
