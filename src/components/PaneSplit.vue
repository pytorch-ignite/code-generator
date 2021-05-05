<template>
  <div
    ref="container"
    class="split-pane"
    :class="{ dragging: isDragging }"
    @mousemove="onDragging"
    @mouseup="stopDragging"
    @mouseleave="stopDragging"
  >
    <div class="left" :style="{ width: getWidth() + '%' }">
      <slot name="left" />
      <div class="split-line" @mousedown.prevent="startDragging" />
    </div>
    <div class="right" :style="{ width: 100 - getWidth() + '%' }">
      <slot name="right" />
    </div>
  </div>
</template>

<script>
// referenced from
// https://github.com/vuejs/vue-next/blob/master/packages/sfc-playground/src/SplitPane.vue
import { ref } from 'vue'
export default {
  setup() {
    const width = ref(45)
    const isDragging = ref(false)
    const container = ref()

    // functions
    const getWidth = () => {
      return width.value < 20 ? 20 : width.value > 80 ? 80 : width.value
    }
    const onDragging = (e) => {
      if (isDragging.value) {
        const draggingPosition = e.pageX
        const totalSize = container.value.offsetWidth
        width.value = (draggingPosition / totalSize) * 100
      }
    }
    const startDragging = () => {
      isDragging.value = true
    }
    const stopDragging = () => {
      isDragging.value = false
    }
    return {
      width,
      isDragging,
      container,
      getWidth,
      onDragging,
      startDragging,
      stopDragging
    }
  }
}
</script>

<style scoped>
.split-pane {
  display: flex;
}
.split-pane.dragging {
  cursor: ew-resize;
}
.dragging .left,
.dragging .right {
  pointer-events: none;
}
.left,
.right {
  position: relative;
}
.left {
  border-right: 1px solid var(--c-white-dark);
}
.split-line {
  position: absolute;
  z-index: 99;
  top: 0;
  bottom: 0;
  right: -5px;
  width: 10px;
  cursor: ew-resize;
}
/* media queries */
@media (max-width: 768px) {
  .split-pane {
    flex-wrap: wrap;
  }
  .left, .right {
    width: 100% !important;
  }
  .split-line {
    display: none;
  }
}
</style>
