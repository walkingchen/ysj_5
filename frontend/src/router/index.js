import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const router = new VueRouter({
  routes: [
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
})

router.beforeEach((to, from, next) => {
  if (to.name === 'Login' || localStorage.getItem('roomid')) {
    next()
  } else {
    next({ name: 'Login' })
  }
})

export default router
