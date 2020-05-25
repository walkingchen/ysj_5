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
      component: () => import('@views/Login_user')
    },
    {
      path: '/admin_login',
      name: 'AdminLogin',
      component: () => import('@views/Login_admin')
    },
    {
      path: '/admin',
      name: 'Admin',
      component: () => import('@views/admin/Index'),
      redirect: '/admin/dashboard',
      children: [{
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@views/admin/Dashboard')
      }, {
        path: 'roomPrototype',
        name: 'RoomPrototype',
        component: () => import('@views/admin/RoomPrototype')
      }, {
        path: 'roomPrototype/:id',
        name: 'RoomPrototypeDetail',
        component: () => import('@views/admin/RoomPrototypeDetail')
      }, {
        path: 'rooms',
        name: 'Rooms',
        component: () => import('@views/admin/Rooms')
      }]
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
