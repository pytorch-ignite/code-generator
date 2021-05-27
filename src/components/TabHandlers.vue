<template>
  <div class="tab handlers">
    <h1>Ignite Handlers Options</h1>
    <h2>Checkpointing</h2>
    <FormCheckbox
      :label="save_training.description"
      :saveKey="save_training.name"
    />
    <FormCheckbox
      :label="save_evaluation.description"
      :saveKey="save_evaluation.name"
    />
    <FormInput
      v-if="store.config.save_training"
      :label="filename_prefix.description"
      :saveKey="filename_prefix.name"
      :type="filename_prefix.type"
    />
    <FormInput
      v-if="store.config.save_training"
      :label="save_every_iters.description"
      :saveKey="save_every_iters.name"
      :type="save_every_iters.type"
    />
    <FormInput
      v-if="store.config.save_training || store.config.save_evaluation"
      :label="n_saved.description"
      :saveKey="n_saved.name"
      :type="n_saved.type"
    />
    <h2>Training Termination</h2>
    <FormCheckbox
      :label="terminate_on_nan.description"
      :saveKey="terminate_on_nan.name"
    />
    <h2>Early Stopping</h2>
    <FormInput
      :label="patience.description"
      :saveKey="patience.name"
      :type="patience.type"
    />
    <h2>Limit Training Time</h2>
    <FormInput
      :label="limit_sec.description"
      :saveKey="limit_sec.name"
      :type="limit_sec.type"
    />
  </div>
</template>

<script>
import { handlers } from '../metadata/metadata.json'
import FormInput from './FormInput.vue'
import FormCheckbox from './FormCheckbox.vue'
import { store } from '../store.js'

export default {
  components: { FormInput, FormCheckbox },
  setup() {
    return { ...handlers, store }
  }
}
</script>
