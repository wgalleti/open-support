import store from '@/store'

export default async function guard (to, from, next) {
  if (
    to.matched.some(record =>
      typeof record.meta.requiresAuth === 'undefined'
        ? true
        : record.meta.requiresAuth
    )
  ) {
    try {
      await store.dispatch('auth/doCheck')
      if (from.name === 'sign-in') {
        next('/')
      } else {
        next()
      }
    } catch (e) {
      next('/sign-in')
    }
  } else {
    if (to.name === 'sign-in') {
      next('/')
    } else {
      next()
    }
  }
}
