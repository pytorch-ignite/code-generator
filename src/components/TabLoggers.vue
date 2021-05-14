<template>
  <div class="tab loggers">
    <h1>Ignite Loggers Selection</h1>
    <FormInput
      type="text"
      :label="output_dir.description"
      :saveKey="output_dir.name"
      required
    />
    <FormSelect
      :label="logger.description"
      :options="logger.options"
      :saveKey="logger.name"
    />
  </div>
</template>

<script>
import { ref } from 'vue'
import { loggers } from '../metadata/metadata.json'
import { saveConfig } from '../store'
import FormSelect from './FormSelect.vue'
import FormInput from './FormInput.vue'

export default {
  components: { FormInput, FormSelect },
  setup() {
    const outputDirValue = ref('')
    const loggerValue = ref('')

    return { ...loggers, saveConfig, outputDirValue, loggerValue }
  }
}
</script>
