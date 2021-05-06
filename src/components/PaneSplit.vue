<template>
  <div
    ref="container"
    class="split-pane"
    :class="{ dragging: isDragging }"
    @mousemove="onDragging"
    @mouseup="stopDragging"
    @mouseleave="stopDragging"
  >
    <div
      class="left"
      :class="{ open: clicked }"
      :style="{ width: getWidth() + '%' }"
    >
      <slot name="left" />
      <div class="split-line" @mousedown.prevent="startDragging" />
    </div>
    <div class="right" :style="{ width: 100 - getWidth() + '%' }">
      <slot name="right" />
    </div>
  </div>
  <div class="sidebar" @click="openSideBar">
    <div class="icon">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        xmlns:xlink="http://www.w3.org/1999/xlink"
        aria-hidden="true"
        role="img"
        class="iconify iconify--mdi"
        width="2rem"
        height="2rem"
        preserveAspectRatio="xMidYMid meet"
        viewBox="0 0 24 24"
      >
        <path
          d="M3 6h18v2H3V6m0 5h18v2H3v-2m0 5h18v2H3v-2z"
          fill="currentColor"
        ></path>
      </svg>
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
    const clicked = ref(false)
    const container = ref()

    // functions
    const openSideBar = () => {
      clicked.value = !clicked.value
    }
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
      clicked,
      openSideBar,
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
.sidebar {
  display: none;
}
/* media queries */
@media (max-width: 768px) {
  .split-pane {
    flex-wrap: wrap;
  }
  .left,
  .right {
    width: 100% !important;
    padding-top: 0.5rem;
    margin-top: 51px;
    border: 0;
  }
  .split-line {
    display: none;
  }
  .sidebar {
    position: absolute;
    display: block;
  }
  .sidebar .icon {
    cursor: pointer;
    display: block;
    position: fixed;
    right: 1rem;
    bottom: 1rem;
    color: var(--c-brand-red);
    background-color: var(--c-white-light);
    border-radius: 2px;
    width: 2rem;
    height: 2rem;
    z-index: 99999;
  }
  .left {
    position: fixed;
    transform: translateX(-100%);
    transition: transform 0.25s ease-in;
    z-index: 10;
    background-color: var(--c-white);
    top: 0;
    bottom: 0;
    overflow: auto;
    height: auto;
  }
  .left.open {
    transform: translateX(0);
    transition: transform 0.35s ease-out;
  }
}
</style>
