import Http from '@/services/http'

/**
 * Check user has been logged in
 * @returns {Promise<*>}
 */
export function checkUser () {
  return Http
    .load('auth/user/')
    .catch(err => {
      throw new Error(`Não foi possível efetuar validar o usuário. Erro: ${err.toString()}`)
    })
}

/**
 * Call login method on api and return user and token
 * Save token on localstorage
 * @param credentials
 * @returns {Promise<T>}
 */
export function signIn (credentials) {
  return Http
    .save('auth/login/', credentials)
    .then(response => {
      const { token = null } = response
      localStorage.setItem('token', token)
      Http.refreshAuth()
      return response
    })
    .catch(err => {
      throw new Error('Não foi possível efetuar o login. Erro' + err.toString())
    })
}

/**
 * Call logout method on api and remove token on local storage
 * @returns {Promise<T>}
 */
export function signOut () {
  return Http
    .save('auth/logout/', {})
    .then(response => {
      localStorage.removeItem('token')
      Http.refreshAuth()
      return response
    })
    .catch(err => {
      localStorage.removeItem('token')
      Http.refreshToken()
      return err
    })
}

/**
 * Call refresh token on api
 * @param token
 * @returns {Promise<*>}
 */
export function refreshToken (token) {
  return Http
    .save('auth/refresh-token/', token)
    .catch(err => {
      throw new Error(`Não foi possível atualizar o token. Erro: ${err.toString()}`)
    })
}
