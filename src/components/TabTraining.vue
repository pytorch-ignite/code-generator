<template>
  <div class="tab training">
    <h1>Training Options</h1>

    We are using yaml files to set up the training configuration (see
    config.yaml). Additional arguments given to the main script can be parsed
    using one of the tools provided below:

    <h2>Argument Parser</h2>
    <ul>
      <li v-show="argparserOptions.options.includes('argparse')">
        <a href="https://docs.python.org/3/library/argparse.html" id="arg"
          >Argparse</a
        >
        - is a python built-in tool to handle command-line arguments
      </li>
      <li v-show="argparserOptions.options.includes('fire')">
        <a
          href="https://github.com/google/python-fire/blob/master/docs/guide.md"
          id="arg"
          >Python Fire</a
        >
        - transforms Python functions into user-friendly command-line tools,
        ideal for DL experimentation.
      </li>
      <li v-show="argparserOptions.options.includes('hydra')">
        <a href="https://hydra.cc" id="arg">Hydra</a>
        - Simplifying deep learning experiments through flexible configuration
        management
      </li>
    </ul>
    <FormSelect
      :label="argparserOptions.description"
      :options="argparserOptions.options"
      :saveKey="argparserOptions.name"
      :defaultV="argparserOptions.default"
      v-show="argparserOptions.options.length > 0"
    />
    <!-- Deterministic Options -->
    <div v-show="templateOptions.deterministic">
      <h2 class="training">Deterministic Training</h2>
      <FormCheckbox
        :label="deterministic.description"
        :saveKey="deterministic.name"
      />
    </div>
    <!-- Distributed Training -->
    <div v-show="templateOptions.distTraining">
      <h2 class="training">Distributed Training</h2>
      <FormCheckbox label="Use distributed training" saveKey="use_dist" />
      <div v-show="store.config.use_dist && templateOptions.distTraining">
        <FormSelect
          required
          :saveKey="backendOptions.name"
          :label="backendOptions.description"
          :options="backendOptions.options"
          :defaultV="backendOptions.default"
        />
        <FormRadio
          :options="distOptions"
          saveKey="dist"
          :defaultV="distOptions.length > 0 ? distOptions[0].name : 'spawn'"
          v-show="distOptions.length > 0"
        />
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
  </div>
</template>

<script>
import { computed, ref, watch, reactive } from 'vue'
import { training } from '../metadata/metadata.json'
import FormCheckbox from './FormCheckbox.vue'
import FormInput from './FormInput.vue'
import FormRadio from './FormRadio.vue'
import FormSelect from './FormSelect.vue'
import { saveConfig, store } from '../store.js'
import { templates } from '../templates/template_options.json'

export default {
  components: { FormCheckbox, FormInput, FormRadio, FormSelect },
  setup() {
    const {
      argparser,
      deterministic,
      backend,
      torchrun,
      spawn,
      nproc_per_node,
      nnodes,
      master_addr,
      master_port
    } = training
    const isDeterministic = ref(false)

    // computed properties
    const templateOptions = computed(() => {
      return templates[store.config.template]['training']
    })
    const argparserOptions = computed(() => {
      return findAvailableOptions(argparser, templateOptions)
    })
    const backendOptions = computed(() => {
      // To check the state of distTraining
      if (templateOptions.value.distTraining == false) {
        saveConfig('backend', null)
        return backend
      }
      return findAvailableOptions(backend, templateOptions)
    })
    const distOptions = computed(() => {
      let dist_options = []
      if (templateOptions.value.distOptions == 'all') {
        return [spawn, torchrun]
      }
      for (const option of [spawn, torchrun]) {
        if (templateOptions.value.distOptions.includes(option.name)) {
          dist_options.push(option)
        }
      }
      console.log('Printing dist options')
      console.log(dist_options)
      return dist_options
    })

    watch(store.config, () => {
      console.log(templateOptions.value)
      console.log(store.config.template)
      console.log(argparserOptions.value)
    })

    const saveDeterministic = computed(() => {
      saveConfig(deterministic.name, isDeterministic)
    })

    return {
      store,
      argparserOptions,
      deterministic,
      backendOptions,
      distOptions,
      nproc_per_node,
      nnodes,
      master_addr,
      master_port,
      isDeterministic,
      saveDeterministic,
      templateOptions
    }
  }
}

function saveDistributed(key, value) {
  saveConfig(key, value)
}

function findAvailableOptions(tempKey, templateOptions) {
  const key = tempKey.name
  if (
    templateOptions.value[key] == 'all' ||
    !templateOptions.value.hasOwnProperty(key)
  ) {
    return tempKey
  } else {
    store.config[key] = templateOptions.value[key][0]
  }
  return reactive({
    options: templateOptions.value[key],
    default: templateOptions.value[key][0],
    description: tempKey.description,
    name: key,
    type: tempKey.type
  })
}
</script>

<style scoped>
.training {
  margin-bottom: 0;
}

#arg {
  font-weight: bold;
}
</style>
