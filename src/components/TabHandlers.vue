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
      :label="filename_prefix.description"
      :saveKey="filename_prefix.name"
      :type="filename_prefix.type"
    />
    <FormInput
      :label="save_every_iters.description"
      :saveKey="save_every_iters.name"
      :type="save_every_iters.type"
    />
    <FormInput
      :label="n_saved.description"
      :saveKey="n_saved.name"
      :type="n_saved.type"
    />
    <h2>Training Termination</h2>
    <FormCheckbox
      :label="terminate_on_nan.description"
      :saveKey="terminate_on_nan.name"
    />
    <h2>Events Timer</h2>
    <FormCheckbox :label="timer.description" :saveKey="timer.name" />
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

export default {
  components: { FormInput, FormCheckbox },
  setup() {
    return { ...handlers }
  }
}
</script>
