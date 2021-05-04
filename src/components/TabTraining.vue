<template>
  <div class="tab training">
    <h1>Training Options</h1>
    <h2 class="training">Deterministic Training</h2>
    <FormCheckbox
      :label="deterministic.description"
      :saveKey="deterministic.name"
    />
    <h2 class="training">Distributed Training</h2>
    <template v-for="(d, index) in distributedConfigs" :key="index">
      <FormInput :label="d.description" :type="d.type" :saveKey="d.name" />
    </template>
  </div>
</template>

<script>
import { computed, ref } from 'vue'
import {
  deterministic,
  nproc_per_node,
  nnodes,
  master_addr,
  master_port
} from '../metadata/training.json'
import FormCheckbox from './FormCheckbox.vue'
import FormInput from './FormInput.vue'

export default {
  components: { FormCheckbox, FormInput },
  setup() {
    const isDeterministic = ref(false)
    const distributedValue = ref({})
    const distributedConfigs = [
      nproc_per_node,
      nnodes,
      master_addr,
      master_port
    ]

    // computed properties
    const saveDeterministic = computed(() => {
      saveConfig(deterministic.name, isDeterministic.value)
    })
    return {
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
@import url('../assets/main.css');

.training {
  margin-bottom: 0;
}
</style>
