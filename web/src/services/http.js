import http from '@/plugins/axios'
import store from '@/store'

class Http {
  constructor () {
    this.http = http
  }

  /**
   * Refresh auth on http
   */
  refreshAuth () {
    const { token = null } = store.state.auth
    delete http.defaults.headers.Authorization

    if (token) {
      http.defaults.headers.Authorization = 'Token ' + token
    }
  }

  /**
   * Parser error on axios request
   * @param err
   * @private
   */
  async _error (err) {
    const { response = null } = err

    // Check is network error
    if (!response) {
      throw new Error(err.message)
    }

    const { status } = response

    if (status === 401) {
      localStorage.removeItem('token')
      this.refreshAuth()
    }

    const checkStatus = status === 400 || status === 404 || status === 500

    if (checkStatus) {
      const { data } = response
      Object.keys(data).forEach(m => {
        if (Array.isArray(data[m])) {
          data[m].forEach(k => {
            throw new Error(`${m}: ${k}`)
          })
        } else {
          throw new Error(`${m}: ${data[m]}`)
        }
      })
    }
  }

  /**
   * Should be call get on url passing params to filter
   * @param url
   * @param params
   * @returns {Promise<*>}
   */
  async load (url, params = {}) {
    const { data } = await this.http.get(url, { params }).catch(err => this._error(err))
    return data
  }

  /***
   * Should be save data. If has pk, call post method on api, else call patch for update data
   * @param url
   * @param data
   * @param pk
   * @returns {Promise<*>}
   */
  save (url, data = {}, pk = null) {
    if (!pk) {
      return this.http
        .post(url, data)
        .then(response => response.data)
        .catch(err => this._error(err))
    }
    return this.http
      .patch(`${url}${pk}/`, data)
      .then(response => response.data)
      .catch(err => this._error(err))
  }

  /***
   * Should be remove data.
   * @param url
   * @param pk
   * @returns {Promise<*>}
   */
  remove (url, pk) {
    return this.http.delete(`${url}${pk}/`).catch(err => this._error(err))
  }
}

const HttpSingleton = (function () {
  const instance = null

  return {
    getInstance: () => !instance ? new Http() : instance
  }
})()

export default HttpSingleton.getInstance()
