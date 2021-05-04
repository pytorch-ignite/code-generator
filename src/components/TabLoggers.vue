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
import { logger, output_dir } from '../metadata/utils.json'
import { saveConfig } from '../store'
import FormSelect from './FormSelect.vue'
import FormInput from './FormInput.vue'

export default {
  components: { FormInput, FormSelect },
  setup() {
    const outputDirValue = ref('')
    const loggerValue = ref('')

    return {
      logger,
      output_dir,
      saveConfig,
      outputDirValue,
      loggerValue
    }
  }
}
</script>

<style scoped>
@import url('../assets/main.css');
</style>
