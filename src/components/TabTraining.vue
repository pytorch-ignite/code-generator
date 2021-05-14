<template>
  <div class="tab training">
    <h1>Training Options</h1>
    <h2 class="training">Deterministic Training</h2>
    <FormCheckbox
      :label="deterministic.description"
      :saveKey="deterministic.name"
    />
    <h2 class="training">Distributed Training</h2>
    <FormRadio :options="[launch, spawn]" saveKey="dist" />
    <template v-for="(d, index) in distributedConfigs" :key="index">
      <FormInput :label="d.description" :type="d.type" :saveKey="d.name" />
    </template>
  </div>
</template>

<script>
import { computed, ref } from 'vue'
import { training } from '../metadata/metadata.json'
import FormCheckbox from './FormCheckbox.vue'
import FormInput from './FormInput.vue'
import FormRadio from './FormRadio.vue'

export default {
  components: { FormCheckbox, FormInput, FormRadio },
  setup() {
    const { deterministic, launch, spawn, ...distributedConfigs } = training
    const isDeterministic = ref(false)
    const distributedValue = ref({})

    // computed properties
    const saveDeterministic = computed(() => {
      saveConfig(deterministic.name, isDeterministic.value)
    })
    return {
      launch,
      spawn,
      deterministic,
      isDeterministic,
      saveDeterministic,
      distributedConfigs,
      distributedValue,
      saveDistributed
    }
  }
}

function saveDistributed(key, value) {
  saveConfig(key, value)
}
</script>

<style scoped>
.training {
  margin-bottom: 0;
}
</style>
