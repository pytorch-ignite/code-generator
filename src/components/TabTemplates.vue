<template>
  <div class="tab template">
    <h1>Template Selection</h1>
    <div class="template">
      <FormSelect
        required
        saveKey="template"
        :label="templateLabel"
        :options="templateOptions"
      />
    </div>
  </div>
</template>

<script>
import FormSelect from './FormSelect.vue'

export default {
  components: { FormSelect },
  setup() {
    const templateLabel = 'Choose Template'
    const templateOptions = ['Vision Classification', 'Vision Detection']

    return { templateLabel, templateOptions }
  }
}
</script>
