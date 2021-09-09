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
      component: () => import('@views/admin/main/Main'),
      redirect: '/admin/assign',
      children: [{
        path: 'assign',
        name: 'Assign',
        component: () => import('@views/admin/Assign')
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
        component: () => import('@views/admin/room/Rooms')
      }]
    }
  ]
})

router.beforeEach((to, from, next) => {
  if (to.name === 'Login' || to.name === 'AdminLogin' || localStorage.getItem('roomid')) {
    next()
  } else {
    next({ name: 'Login' })
  }
})

export default router
