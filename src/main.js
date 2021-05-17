// main entrypoint of the app
import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import Landing from './components/Landing.vue'
import Create from './components/Create.vue'

const routes = [
  { path: '/', component: Landing },
  { path: '/create', component: Create }
]

const router = createRouter({
  history: createWebHistory(),
  routes: routes
})

createApp(App).use(router).mount('#app')
