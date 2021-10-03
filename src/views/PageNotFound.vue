<template>
  <div class="heading">
    <h1>404 Page Not Found</h1>
    <p>
      Oops we couldn't find that page. Try going
      <RouterLink to="/" class="link alt" :style="learnMore">home</RouterLink>
    </p>
  </div>
</template>
  <style scoped>
h1{
  color: orange;
}
.heading {
  max-width: 75vw;
  margin: auto;
  text-align: center;
}
.heading .alt {
  background: var(--c-white);
  color: var(--c-brand-red);
}
</style>