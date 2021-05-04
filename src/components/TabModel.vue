<template>
  <div class="tab models">
    <h1>Model Selection</h1>
    <div class="domain">
      <FormSelect
        required
        saveKey="domain"
        :label="labelDomain"
        :options="optionsDomain"
        @change="domainChange"
      />
      <template v-if="selectedDomain">
        <FormSelect
          required
          saveKey="subdomain"
          :label="labalSubDomain"
          :options="optionsSubDomain"
          @change="subDomainChange"
        />
      </template>
      <template v-if="selectedSubDomain">
        <FormSelect
          required
          saveKey="model"
          :label="labelModel"
          :options="optionsModel"
        />
      </template>
    </div>
    <a
      class="learn-more"
      target="_blank"
      rel="noopener noreferrer"
      :href="urls[selectedDomain]"
      v-show="selectedDomain"
      >Learn more about available {{ selectedDomain }} models.</a
    >
  </div>
</template>

<script>
import vision from '../metadata/models/vision.json'
import text from '../metadata/models/text.json'
import { computed, ref } from 'vue'
import FormSelect from './FormSelect.vue'
import { store } from '../store.js'

export default {
  components: { FormSelect },
  setup() {
    const domainsObj = { vision: vision, text: text, audio: {} }
    const labelDomain = 'Choose domain'
    const labalSubDomain = 'Choose subdomain'
    const labelModel = 'Choose model'
    const optionsDomain = Object.keys(domainsObj)
    const urls = {
      Vision: 'https://pytorch.org/vision/stable/models.html',
      Text: '',
      Audio: ''
    }
    const selectedDomain = ref('')
    const selectedSubDomain = ref('')
    const selectedModel = ref('')

    // computed properties
    const domainChange = computed(() => {
      selectedDomain.value = store.config.domain
    })
    const subDomainChange = computed(() => {
      selectedSubDomain.value = store.config.subdomain
    })
    const optionsSubDomain = computed(() => {
      if (selectedDomain.value) {
        return Object.keys(domainsObj[selectedDomain.value])
      }
    })
    const optionsModel = computed(() => {
      // alert('optionsModel')
      if (selectedSubDomain.value) {
        return domainsObj[selectedDomain.value][selectedSubDomain.value]
      }
    })

    return {
      labelDomain,
      labalSubDomain,
      labelModel,
      selectedDomain,
      selectedSubDomain,
      selectedModel,
      optionsDomain,
      optionsSubDomain,
      optionsModel,
      domainsObj,
      urls,
      domainChange,
      subDomainChange
    }
  }
}
</script>

<style scoped>
@import url('../assets/main.css');

.domain h2 {
  margin-bottom: 0;
}
.subdomain h3 {
  margin-bottom: 0.25rem;
}
.model h4 {
  margin-bottom: 0.5rem;
}
.learn-more {
  display: block;
  margin-top: 1rem;
  max-width: max-content;
  font-weight: bold;
  text-transform: capitalize;
  text-decoration: none;
  border-bottom: 2px solid var(--c-brand-red);
  color: var(--c-text);
}
.learn-more:hover {
  border-bottom-color: transparent;
}
</style>
