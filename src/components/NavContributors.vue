<template>
  <button
    @click.prevent="showContributors = true"
    title="Contributors"
    class="contributors-btn external-links"
  >
    <span class="icon-text">Contributors</span>
  </button>
  <div
    class="contributors-bg"
    v-show="showContributors"
    @click.prevent="showContributors = false"
  ></div>
  <div class="contributors-wrapper" v-show="showContributors">
    <div>
      <h1 class="pis-40px">These folks made this web app!</h1>

      <p class="pis-40px">
        🙌 ✨ 🎉 Big shout-out goes to <b>Jeff Yang</b> (<a
          href="https://github.com/ydcjeff"
          >@ydcjeff</a
        >) who coded the base of this web app!
      </p>

      <p class="pis-40px">
        ✨ Thanks to <b>Taras</b> (<a href="https://github.com/trsvchn"
          >@trsvchn</a
        >) who was helping Jeff with the templates and making this app great!
      </p>

      <p class="pis-40px">
        🎉 Thanks to <b>Victor</b> (<a href="https://github.com/vfdev-5"
          >@vfdev-5</a
        >) who is helping with the code and coordinating this project!
      </p>

      <p class="pis-40px">
        🎊 Thanks to <b>Jyotirmay</b> (<a
          href="https://github.com/theory-in-progress"
          >@theory-in-progress</a
        >), GSoC2023 student, who is working on new templates and improving the
        codebase!
      </p>

      <p class="pis-40px">
        👏 Thanks to <b>Aryan</b> (<a href="https://github.com/guptaaryan16"
          >@guptaaryan16</a
        >), <a href="https://labs.quansight.org/">Quansight Labs</a> Intern, who
        worked on adding argparser option and Nebari support!
      </p>

      <p class="pis-40px">
        If you find this app useful, please put a ⭐️ on
        <a href="https://github.com/pytorch-ignite/code-generator"
          >its repository</a
        >
        and give us a feedback
        <a href="https://github.com/pytorch-ignite/code-generator/issues/new"
          >here</a
        >. Thanks you!
      </p>

      <p class="pis-40px">
        If you would like to see your name in this list, join us on our
        <a href="https://pytorch-ignite.ai/chat">Discord</a> and start
        contributing to this app!
      </p>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
export default {
  setup() {
    const showContributors = ref(false)
    return { showContributors }
  }
}
</script>

<style scoped>
@import url('./css/nav-right.css');

.contributors-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: none;
  color: var(--c-text);
  cursor: pointer;
  font-family: var(--font-family-base);
  padding: 0.3rem 0.5rem;
  border: 1px solid darkred;
  border-radius: 4px;
}
.contributors-bg {
  text-align: left;
  color: var(--c-text);
  text-transform: none;
  position: fixed;
  top: 0;
  left: 0;
  background-color: rgba(101, 110, 133, 0.8);
  z-index: 10;
  width: 100vw;
  height: 100vh;
}
.contributors-wrapper {
  position: fixed;
  max-width: 38rem;
  padding: 0 0.5rem;
  margin: 20vh auto 100%;
  inset: 0;
  z-index: 12;
}
.contributors-wrapper div {
  padding: 1rem 0;
  background-color: var(--c-white-light);
  font-size: var(--font-size);
  color: var(--c-text);
  border-radius: 8px;
  box-shadow: 0 0 5px 5px rgba(0, 0, 0, 0.33);
}
.pis-40px {
  padding-inline-start: 40px;
  padding-inline-end: 40px;
}
.step {
  margin-top: 8px;
}
</style>
