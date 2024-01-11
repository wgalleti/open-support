import { set } from '@/services/helpers'
import Http from '@/services/http'
import { checkUser, refreshToken, signIn, signOut } from '@/services/auth'

export default {
  namespaced: true,
  state: {
    token: '',
    user: null
  },
  mutations: {
    SET_TOKEN (state, payload) {
      localStorage.setItem('token', payload)
      Http.refreshAuth()
      state.token = payload
    },
    SET_USER: set('user')
  },
  getters: {
    userID: state => state.user.id,
    isLogged: state => state.token !== null,
    isCliente: state => state.user && state.user.is_cliente,
    isAtendente: state => state.user && state.user.is_atendente,
    isAdmin: state => state.user && state.user.is_superuser,
    profileImg: state => state.user && state.user.foto === null ? './img/user.jpg' : state.user.foto
  },
  actions: {
    doCheck: async ({ commit, state }) => {
      const token = localStorage.getItem('token')
      if (!token) {
        Http.refreshAuth()
        throw new Error('Token não encontrado')
      }

      commit('SET_TOKEN', token)
      Http.refreshAuth()

      if (!state.user) {
        try {
          const response = await checkUser()
          commit('SET_USER', response)
          return response
        } catch {
          if (!state.token) {
            throw new Error('Não possui token')
          }
          try {
            const response = await refreshToken(state.token)
            commit('SET_TOKEN', response.token)
          } catch {
            throw new Error('Token expirado ou inválido')
          }
        }
      }
    },
    doSignIn: async ({ commit }, credentials) => {
      try {
        const { token, user } = await signIn(credentials)
        commit('SET_TOKEN', token)
        commit('SET_USER', user)
        return {
          token,
          user
        }
      } catch (e) {
        console.log(e)
        throw new Error('Credenciais inválidas!')
      }
    },
    doSignOut: async ({ commit }) => {
      commit('SET_TOKEN', null)
      commit('SET_USER', null)
      await signOut()
    }
  }
}
