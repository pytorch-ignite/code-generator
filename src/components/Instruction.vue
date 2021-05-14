<template>
  <div class="preview">
    <h2>Choose a template on the left to get started.</h2>
    <span class="iconify animate-bounce" data-icon="carbon:arrow-left"></span>
  </div>
</template>

<style scoped>
.preview {
  max-width: 75%;
  margin: 25% auto;
  text-align: center;
  color: #a1a1aa;
}
.iconify {
  vertical-align: middle;
  width: 10%;
  height: 10%;
}
@media (max-width: 768px) {
  .iconify {
    width: 20%;
    height: 20%;
  }
}
/* copied from https://windicss.org/utilities/behaviors.html#animation */
/* adjusted with translateX */
@keyframes bounce {
  0%,
  100% {
    -webkit-transform: translateX(0);
    transform: translateX(0);
    -webkit-animation-timing-function: cubic-bezier(0.8, 0, 1, 1);
    animation-timing-function: cubic-bezier(0.8, 0, 1, 1);
  }
  50% {
    -webkit-transform: translateX(-25%);
    transform: translateX(-25%);
    -webkit-animation-timing-function: cubic-bezier(0, 0, 0.2, 1);
    animation-timing-function: cubic-bezier(0, 0, 0.2, 1);
  }
}
@-webkit-keyframes bounce {
  0%,
  100% {
    -webkit-transform: translateX(0);
    transform: translateX(0);
    -webkit-animation-timing-function: cubic-bezier(0.8, 0, 1, 1);
    animation-timing-function: cubic-bezier(0.8, 0, 1, 1);
  }
  50% {
    -webkit-transform: translateX(-25%);
    transform: translateX(-25%);
    -webkit-animation-timing-function: cubic-bezier(0, 0, 0.2, 1);
    animation-timing-function: cubic-bezier(0, 0, 0.2, 1);
  }
}
.animate-bounce {
  -webkit-animation: bounce 1s infinite;
  animation: bounce 1s infinite;
}
</style>
