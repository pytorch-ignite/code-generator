<template>
  <main class="landing">
    <div class="heading">
      <img
        src="../assets/ignite_logomark.svg"
        alt="PyTorch-Ignite logo"
        width="200"
        height="200"
      />
      <h1>Code-Generator</h1>
      <p>
        The easiest way to create your training scripts with PyTorch-Ignite.
      </p>
    </div>
    <div class="links">
      <div>
        <RouterLink to="/create" class="link" :style="getStarted"
          >Get Started</RouterLink
        >
      </div>
      <div>
        <RouterLink to="/#learn-more" class="link alt" :style="learnMore"
          >Learn More</RouterLink
        >
      </div>
    </div>
    <div class="preview-image">
      <img
        src="../assets/code-generator-preview.png"
        alt="Code Generator Preview"
        width="500"
        height="160"
      />
    </div>
    <div id="learn-more" class="learn-more">
      <h3>What is Code-Generator?</h3>
      <p>
        "Code Generator" is a web application built with Vue.js 3 to quickly
        produce quick-start python code for common training tasks in deep
        learning. Code is using PyTorch framework and PyTorch-Ignite library and
        it can be configured in the UI.
      </p>
      <h3>Why to use Code-Generator?</h3>
      <p>
        Start working on a task without rewriting everything from scratch:
        Kaggle competition, client prototype project, etc.
      </p>
    </div>
    <Footer />
  </main>
</template>

<script>
import Footer from '../components/Footer.vue'
export default {
  components: { Footer },
  setup() {
    const len = 'PyTorch-Ignite'.length
    const learnMore = {
      'border-bottom-left-radius': Math.floor(Math.random() * len) + 'px',
      'border-bottom-right-radius': Math.floor(Math.random() * len) + 'px',
      'border-top-left-radius': Math.floor(Math.random() * len) + 'px',
      'border-top-right-radius': Math.floor(Math.random() * len) + 'px'
    }
    const getStarted = {
      'border-bottom-left-radius': Math.floor(Math.random() * len) + 'px',
      'border-bottom-right-radius': Math.floor(Math.random() * len) + 'px',
      'border-top-left-radius': Math.floor(Math.random() * len) + 'px',
      'border-top-right-radius': Math.floor(Math.random() * len) + 'px'
    }
    return { getStarted, learnMore }
  }
}
</script>

<style scoped>
.landing {
  max-width: 75vw;
  margin: auto;
  text-align: center;
}
.heading {
  margin-top: 6rem;
}
.landing h1 {
  font-size: 3rem;
  margin-bottom: 0;
}
.landing p {
  margin-top: 0;
  font-size: 1.5rem;
  color: #6b7280;
}
.landing .links {
  display: flex;
  justify-items: center;
  justify-content: center;
  align-content: center;
  align-items: center;
  margin: 2.5rem 0;
}
.landing .link {
  /* border-radius: 8px; */
  padding: 0.75rem 1rem;
  border: 2px solid #de4c2c;
  background: #de4c2c;
  margin: 0 0.75rem;
  color: var(--c-white-light);
  font-size: 1.25rem;
  transition: background 0.1s ease;
}
.landing .link:hover {
  background: var(--c-brand-red);
}
.landing .alt {
  background: var(--c-white);
  color: var(--c-brand-red);
}
.landing .alt:hover {
  color: var(--c-white-light);
  background: var(--c-brand-red);
}
.learn-more h3 {
  font-size: 1.5rem;
}
.learn-more p {
  font-size: 1.25rem;
}
.learn-more {
  text-align: left;
  padding: 0.5rem 1rem;
}
.preview-image img {
  width: 100%;
  height: 100%;
  margin-top: 5rem;
}
@media (max-width: 860px) {
  .landing {
    max-width: 95vw;
  }
  .landing .heading {
    margin-top: 3rem;
  }
  .landing h1 {
    font-size: 1.5rem;
  }
  .landing h3 {
    font-size: 1.25rem;
  }
  .landing p,
  .landing .link {
    font-size: 1rem;
  }
  .landing .preview-image img {
    margin-top: 0;
  }
}
</style>
