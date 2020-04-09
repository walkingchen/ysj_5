import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    component: () => import('@views/userHome/Index')
  },
  {
    path: '/register',
    component: () => import('@views/Register')
  },
  {
    path: '/login',
    component: () => import('@views/Login')
  }
]

const router = new VueRouter({
  routes
})

export default router
