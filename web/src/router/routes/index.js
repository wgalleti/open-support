import store from '@/store'

export default [
  {
    path: '/sign-in',
    name: 'Sign in',
    component: () => import(/* webpackChunkName: "sign-in" */ '@/views/auth/sign-in.vue'),
    meta: {
      requiresAuth: false,
      layout: 'layout-auth'
    }
  },
  {
    path: '/sign-out',
    name: 'Sign out',
    meta: {
      requiresAuth: false,
      layout: 'layout-auth'
    },
    async beforeEnter (to, from, next) {
      await store.dispatch('auth/doSignOut')
      next('/sign-in')
    }
  },
  {
    path: '/profile',
    name: 'Perfil',
    component: () => import(/* webpackChunkName: "profile" */ '@/views/auth/profile.vue')
  },
  {
    path: '/change-password',
    name: 'Trocar Senha',
    component: () => import(/* webpackChunkName: "password" */ '@/views/auth/password-change.vue')
  },
  {
    path: '/',
    name: 'Home',
    component: () => import(/* webpackChunkName: "home" */ '@/views/home/index.vue')
  },
  {
    path: '/clientes',
    name: 'Clientes',
    component: () => import(/* webpackChunkName: "clientes" */ '@/views/cliente/index.vue')
  },
  {
    path: '/atendentes',
    name: 'Atendentes',
    component: () => import(/* webpackChunkName: "atendentes" */ '@/views/atendente/index.vue')
  },
  {
    path: '/tickets',
    name: 'Tickets',
    component: () => import(/* webpackChunkName: "tickets" */ '@/views/ticket/index.vue')
  },
  {
    path: '/detalhes/:id',
    name: 'Tickets',
    component: () => import(/* webpackChunkName: "tickets" */ '@/views/ticket/detalhes.vue')
  },
  {
    path: '/os',
    name: 'Ordem de Serviço',
    component: () => import(/* webpackChunkName: "tickets" */ '@/views/os/index.vue')
  }
]
