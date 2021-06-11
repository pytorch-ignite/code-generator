<template>
  <div class="tab template">
    <h1>Template Selection</h1>
    <div class="template">
      <FormSelect
        required
        saveKey="template"
        :label="templateLabel"
        :options="templateOptions"
        @change.prevent="downloadTemplates"
      />
    </div>
    <div class="include-test">
      <FormCheckbox
        label="Include a test file for the generated code"
        saveKey="include_test"
      />
    </div>
  </div>
</template>

<script>
import FormSelect from './FormSelect.vue'
import FormCheckbox from './FormCheckbox.vue'
import templates from '../templates/templates.json'
import { store, fetchTemplates } from '../store.js'

export default {
  components: { FormSelect, FormCheckbox },
  setup() {
    const templateLabel = 'Choose A Template'
    const templateOptions = Object.keys(templates)

    const downloadTemplates = () => fetchTemplates(store.config.template)

    return {
      templateLabel,
      templateOptions,
      downloadTemplates
    }
  }
}
</script>
