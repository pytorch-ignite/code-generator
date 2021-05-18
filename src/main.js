// main entrypoint of the app
import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import Home from './components/Home.vue'
import Create from './components/Create.vue'

const routes = [
  {
    name: 'home',
    path: '/',
    component: Home,
    meta: { transition: 'slide-left' }
  },
  {
    name: 'create',
    path: '/create',
    component: Create,
    meta: { transition: 'slide-right' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes: routes,
  scrollBehavior(to, from, savedPosition) {
    if (to.hash) {
      return {
        el: to.hash,
        behavior: 'smooth'
      }
    }
  }
})

createApp(App).use(router).mount('#app')
