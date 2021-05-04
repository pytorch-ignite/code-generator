<template>
  <div class="tab handlers">
    <h1>Ignite Handlers Options</h1>
    <h2>Checkpointing</h2>
    <p>{{ to_save.description }}</p>
    <template v-for="(o, index) in to_save.options" :key="index">
      <FormCheckbox :label="o.description" :saveKey="o.name" />
    </template>
    <FormCheckbox
      :label="terminate_on_nan.description"
      :saveKey="terminate_on_nan.name"
    />
    <template
      v-for="(o, index) in [filename_prefix, n_saved, limit_sec]"
      :key="index"
    >
      <FormInput :label="o.description" :saveKey="o.name" :type="o.type" />
    </template>
  </div>
</template>

<script>
import {
  to_save,
  filename_prefix,
  n_saved,
  terminate_on_nan,
  limit_sec
} from '../metadata/utils.json'
import FormInput from './FormInput.vue'
import FormCheckbox from './FormCheckbox.vue'

export default {
  components: { FormInput, FormCheckbox },
  setup() {
    return {
      to_save,
      filename_prefix,
      n_saved,
      terminate_on_nan,
      limit_sec
    }
  }
}
</script>

<style scoped>
@import url('../assets/main.css');
</style>
