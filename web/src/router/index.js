import Vue from 'vue'
import VueRouter from 'vue-router'
import routes from '@/router/routes'
import guard from '@/router/guard'

Vue.use(VueRouter)

const router = new VueRouter({
  base: process.env.BASE_URL,
  routes
})

router.beforeEach(guard)

export default router
