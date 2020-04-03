import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

export const constantRoutes = [

  {
    path: '/register',
    component: () => import('@/views/admin/register/index'),
    hidden: true
  },

  {
    path: '/login',
    component: () => import('@/views/admin/login/index'),
    hidden: true
  },

  // {
  //   path: '/404',
  //   component: () => import('@/views/404'),
  //   hidden: true
  // },

  // {
  //   path: '/notice',
  //   component: () => import('@/views/login/components/notice')
  // },

  {
    path: '/',
    redirect: '/user',
    component: () => import('@/App'),
    children: [{
      path: '/user',
      name: 'user',
      component: () => import('@/views/user/index')
    }]
  },

  {
    path: '/admin',
    component: Layout,
    redirect: '/dashboard',
    children: [{
      path: '/dashboard',
      name: 'Dashboard',
      component: () => import('@/views/admin/dashboard/index'),
      meta: { title: 'Dashboard', icon: 'dashboard' }
    }]
  },

  // {
  //   path: '/prototype',
  //   component: Layout,
  //   redirect: '/prototype/index',
  //   name: 'prototype',
  //   meta: { title: 'prototype', icon: 'table' },
  //   children: [
  //     {
  //       path: 'index',
  //       name: 'index',
  //       component: () => import('@/views/prototype/index'),
  //       meta: { title: 'prototype' }
  //     },
  //     {
  //       path: 'detail',
  //       name: 'detail',
  //       component: () => import('@/views/prototype/detail'),
  //       meta: { title: 'prototypeDetail' }
  //     }
  //   ]
  // },

  {
    path: '/chatroom',
    component: Layout,
    redirect: '/chatroom/prototype',
    meta: { title: 'Chatroom', icon: 'table' },
    children: [
      {
        path: '/prototype',
        name: 'prototype',
        component: () => import('@/views/admin/prototype/index'),
        meta: { title: 'Prototype', icon: 'form' }
      },
      {
        path: '/prototype/:id',
        component: () => import('@/views/admin/prototype/detail')
      },
      {
        path: '/roomlist',
        name: 'roomlist',
        component: () => import('@/views/admin/chatroom/index'),
        meta: { title: 'Room List', icon: 'nested' }
      }
    ]
  },
  // {
  //   path: '/userList',
  //   component: Layout,
  //   children: [{
  //     path: '/userList',
  //     component: () => import('@/views/admin/userList/index'),
  //     meta: { title: 'User', icon: 'user' }
  //   }]

  // },
  // 404 page must be placed at the end !!!
  { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new Router({
  mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
