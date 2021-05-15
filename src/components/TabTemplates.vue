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
    <h2>Choose Configuration Library and File</h2>
    <FormRadio :options="[argparse, hydra]" saveKey="config_lib" required />
  </div>
</template>

<script>
import FormSelect from './FormSelect.vue'
import FormRadio from './FormRadio.vue'
import templates from '../templates/templates.json'
import { store, fetchTemplates } from '../store.js'
import { templates_config_lib } from '../metadata/metadata.json'

export default {
  components: { FormSelect, FormRadio },
  setup() {
    const templateLabel = 'Choose A Template'
    const templateOptions = Object.keys(templates)
    const { argparse, hydra } = templates_config_lib
    const downloadTemplates = () => fetchTemplates(store.config.template)

    return {
      templateLabel,
      templateOptions,
      downloadTemplates,
      argparse,
      hydra
    }
  }
}
</script>
