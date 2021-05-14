<template>
  <div class="tab handlers">
    <h1>Ignite Handlers Options</h1>
    <h2>Checkpointing</h2>
    <template v-for="(h, index) in handlers" :key="index">
      <template v-if="h.type === 'checkbox'">
        <FormCheckbox :label="h.description" :saveKey="h.name" />
      </template>
      <template v-else>
        <FormInput :label="h.description" :saveKey="h.name" :type="h.type" />
      </template>
    </template>
  </div>
</template>

<script>
import { handlers } from '../metadata/metadata.json'
import FormInput from './FormInput.vue'
import FormCheckbox from './FormCheckbox.vue'

export default {
  components: { FormInput, FormCheckbox },
  setup() {
    return { handlers }
  }
}
</script>
