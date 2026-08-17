import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: '/projects'
    },
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/views/Login.vue'),
      meta: { guest: true }
    },
    {
      path: '/register',
      name: 'Register',
      component: () => import('@/views/Register.vue'),
      meta: { guest: true }
    },
    {
      path: '/projects',
      name: 'ProjectList',
      component: () => import('@/views/ProjectList.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/project/:id',
      name: 'ProjectDetail',
      component: () => import('@/views/ProjectDetail.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/interview/:id',
      name: 'Interview',
      component: () => import('@/views/Interview.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/outline/:id',
      name: 'Outline',
      component: () => import('@/views/Outline.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/contract/:id',
      name: 'Contract',
      component: () => import('@/views/Contract.vue'),
      meta: { requiresAuth: true }
    }
  ]
})

router.beforeEach((to, _from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth && !authStore.isLoggedIn) {
    next('/login')
  } else if (to.meta.guest && authStore.isLoggedIn) {
    next('/projects')
  } else {
    next()
  }
})

export default router
