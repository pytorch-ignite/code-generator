<template>
  <Transition name="fade">
    <div class="msg-wrapper" v-if="msg.showMsg" @click="msg.showMsg = false">
      <div class="msg" :style="style">
        {{ message }}
      </div>
    </div>
  </Transition>
</template>

<script>
// referenced on
// https://github.com/vuejs/vue-next/blob/master/packages/sfc-playground/src/Message.vue
import { computed, toRefs, watch } from 'vue'
import { msg } from '../store.js'

export default {
  props: {
    message: {
      type: String,
      required: true
    },
    color: {
      type: String,
      required: true
    }
  },
  setup(props) {
    const { message, color } = toRefs(props)
    const style = computed(() => {
      return {
        borderColor: color.value,
        color: color.value,
        background: color.value === 'blue' ? '#dbeafe' : '#fee2e2'
      }
    })
    watch(
      () => msg.showMsg,
      () => {
        if (msg.showMsg) {
          setTimeout(() => (msg.showMsg = false), 5000)
        }
      }
    )

    return { message, color, style, msg }
  }
}
</script>

<style scoped>
.msg-wrapper {
  position: fixed;
  --msg-offset: 1.5rem;
  bottom: var(--msg-offset);
  right: var(--msg-offset);
  left: 0;
  padding-left: var(--msg-offset);
  width: inherit;
  z-index: 10;
}
.msg {
  border-radius: 8px;
  border-width: 2px;
  border-style: solid;
  margin-right: var(--msg-offset);
  padding: 1rem 2rem;
}
.fade-enter-active,
.fade-leave-active {
  transition: all 0.25s ease-out;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translate(0, 10px);
}
</style>
