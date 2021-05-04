<template>
  <form class="inputs-wrapper" @submit.prevent="saveInput">
    <p class="label-wrapper">
      <label :for="inputId">
        {{ label }} – <code>{{ saveKey }}</code> {{ isRequired }}
      </label>
    </p>
    <input
      minlength="1"
      v-if="type === 'text'"
      v-model.trim="inputted"
      :type="type"
      :id="inputId"
      :required="required"
    />
    <input
      min="0"
      v-else-if="type === 'number'"
      v-model.number="inputted"
      :type="type"
      :id="inputId"
      :required="required"
    />
    <input
      v-else
      v-model="inputted"
      :type="type"
      :id="inputId"
      :required="required"
    />
    <span class="expand"></span>
  </form>
</template>

<script>
import { computed, ref, toRefs } from 'vue'
import { saveConfig } from '../store'
export default {
  props: {
    label: {
      type: String,
      required: true
    },
    type: {
      type: String,
      default: 'text'
    },
    required: {
      type: Boolean,
      default: false
    },
    saveKey: {
      type: String,
      required: true
    }
  },
  setup(props) {
    const { label, type, saveKey, required } = toRefs(props)
    const inputted = ref('')

    const saveInput = () => saveConfig(saveKey.value, inputted.value)
    const inputId = computed(() => label.value + '-input-' + type.value)
    const isRequired = computed(() => (required.value ? '*' : ''))
    return {
      label,
      type,
      saveKey,
      required,
      inputted,
      saveInput,
      inputId,
      isRequired
    }
  }
}
</script>

<style scoped>
/* input style for text and number */
.inputs-wrapper {
  position: relative;
}
input {
  font-family: var(--font-family-base);
  font-size: var(--font-size);
}
input[type='text'],
input[type='number'] {
  border-radius: 3px 3px 0 0;
  border: 1px solid var(--c-white-light);
  background: var(--c-white-light);
  padding: 0.5rem 1rem;
  width: 100%;
}
input[type='text'] ~ .expand,
input[type='number'] ~ .expand {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  border-bottom: 2px solid var(--c-brand-red);
  transform: scaleX(0);
  transition: transform 0.25s ease-in-out;
}
input[type='text']:focus,
input[type='number']:focus {
  outline: none;
  background: var(--c-white);
}
input[type='text']:focus ~ .expand,
input[type='number']:focus ~ .expand {
  transform: scaleX(1);
}
</style>
