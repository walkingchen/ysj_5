import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    component: () => import('@views/room/Index')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@views/Register')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@views/Login')
  }
]

const router = new VueRouter({
  routes
})

export default router
