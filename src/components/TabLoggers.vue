<template>
  <div class="tab loggers">
    <h1>Ignite Loggers Selection</h1>
    <FormInput
      type="text"
      :label="output_dir.description"
      :saveKey="output_dir.name"
      :defaultV="output_dir.default"
    />
    <FormInput
      type="number"
      :label="log_every_iters.description"
      :saveKey="log_every_iters.name"
      :defaultV="log_every_iters.default"
    />
    <FormSelect
      :label="logger.description"
      :options="logger.options"
      :saveKey="logger.name"
      :defaultV="logger.default"
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
