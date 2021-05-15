<template>
  <div class="preview">
    <h2>Choose a template on the left to get started.</h2>
    <svg
      xmlns="http://www.w3.org/2000/svg"
      xmlns:xlink="http://www.w3.org/1999/xlink"
      aria-hidden="true"
      role="img"
      class="iconify iconify--carbon animate-bounce"
      width="32"
      height="32"
      preserveAspectRatio="xMidYMid meet"
      viewBox="0 0 32 32"
    >
      <path
        d="M14 26l1.41-1.41L7.83 17H28v-2H7.83l7.58-7.59L14 6L4 16l10 10z"
        fill="currentColor"
      ></path>
    </svg>
  </div>
</template>

<style scoped>
.preview {
  max-width: 75%;
  margin: 25% auto;
  text-align: center;
  color: #a1a1aa;
  text-transform: capitalize;
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
