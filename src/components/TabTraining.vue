<template>
  <div class="tab training">
    <h1>Training Options</h1>
    <h2 class="training">Deterministic Training</h2>
    <FormCheckbox
      :label="deterministic.description"
      :saveKey="deterministic.name"
    />
    <h2 class="training">Distributed Training (NCCL backend)</h2>
    <FormCheckbox label="Use distributed training" saveKey="use_dist" />
    <div v-show="store.config.use_dist">
      <FormRadio :options="[launch, spawn]" saveKey="dist" defaultV="launch" />
      <FormInput
        :label="nproc_per_node.description"
        :type="nproc_per_node.type"
        :saveKey="nproc_per_node.name"
        :defaultV="nproc_per_node.default"
      />
      <FormInput
        :label="nnodes.description"
        :type="nnodes.type"
        :saveKey="nnodes.name"
        :defaultV="nnodes.default"
      />
      <FormInput
        :label="master_addr.description"
        :type="master_addr.type"
        :saveKey="master_addr.name"
        :defaultV="master_addr.default"
        v-show="store.config.nnodes > 1"
      />
      <FormInput
        :label="master_port.description"
        :type="master_port.type"
        :saveKey="master_port.name"
        :defaultV="master_port.default"
        v-show="store.config.nnodes > 1"
      />
    </div>
  </div>
</template>

<script>
import { computed, ref } from 'vue'
import { training } from '../metadata/metadata.json'
import FormCheckbox from './FormCheckbox.vue'
import FormInput from './FormInput.vue'
import FormRadio from './FormRadio.vue'
import { store } from '../store.js'

export default {
  components: { FormCheckbox, FormInput, FormRadio },
  setup() {
    const {
      deterministic,
      launch,
      spawn,
      nproc_per_node,
      nnodes,
      master_addr,
      master_port
    } = training
    const isDeterministic = ref(false)

    // computed properties
    const saveDeterministic = computed(() => {
      saveConfig(deterministic.name, isDeterministic.value)
    })
    return {
      store,
      deterministic,
      launch,
      spawn,
      nproc_per_node,
      nnodes,
      master_addr,
      master_port,
      isDeterministic,
      saveDeterministic,
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
