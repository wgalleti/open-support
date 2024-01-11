import Http from '@/services/http'
import CustomStore from 'devextreme/data/custom_store'

export default class Model {
  /**
   * @param url (address for endpoint resource)
   * @param columns (devExpress columns Grid)
   * @param form (devExpress form Config)
   * @param primaryKey (resource primary key)
   */
  constructor (url, columns = null, form = {}, primaryKey = 'id') {
    this.url = url
    this.primaryKey = primaryKey
    this.columns = columns
    this.form = form
    this.http = Http
  }

  /**
   * List all resource on endpoint
   * @returns {Promise<Array>}
   */
  all () {
    return this.http.load(this.url)
  }

  /***
   * List a instance of resource on endpoint
   * @param pk
   * @returns {Promise<Object>}
   */
  find (pk, url = '') {
    return this.http.load(`${this.url}${pk}/${url}`)
  }

  /***
   * Return a list of filtered resource on endpoint
   * @param params
   * @param url
   * @returns {Promise<Array>}
   */
  filter (params = {}, url = '') {
    return this.http.load(`${this.url}${url}`, params)
  }

  /***
   * Return a list of search on endpoint
   * @param term
   * @param url
   * @returns {*}
   */
  search (term = '', url = '') {
    return this.http.get(`${this.url}${url}`, { search: term })
  }

  /**
   * Sometimes we need a custom load
   * @param url
   * @param params
   * @returns {*}
   */
  static load (url, params) {
    return this.http.load(url, params)
  }

  /**
   * Save resource on endpoint
   * @param data
   * @param pk
   * @param url
   * @returns {*}
   */
  save (data = {}, pk = null, url = '') {
    return this.http.save(`${this.url}${url}`, data, pk)
  }

  /**
   * Remove resource on endpoint
   * @param pk
   * @returns {Q.Promise<any> | Promise<postcss.Result> | undefined}
   */
  remove (pk) {
    return this.http.remove(this.url, pk)
  }

  /**
   * Make a devexpress lookup for grid columns lookup
   * @param params
   * @param chache
   * @param url
   * @param isDataSource
   * @returns {{paginate: boolean, store: CustomStore}}
   */
  makeLookup (params = {}, chache = false, url = '', isDataSource = true, local = false) {
    return {
      paginate: true,
      pageSize: 10,
      store: new CustomStore({
        key: this.primaryKey,
        loadMode: isDataSource ? 'processed' : 'raw',
        cacheRawData: chache,
        byKey: async key => {
          if (!local) {
            return this.find(key)
          }

          const data = await this.filter({
            ...params,
            lookup: true
          }, url)

          const row = data.filter(f => f[this.primaryKey] === key)

          if (row.length !== 0) {
            return row[0]
          }

          return {}
        },
        load: loadOptions => {
          const {
            take,
            skip,
            searchValue: search
          } = loadOptions
          return this.filter({
            ...params,
            take,
            skip,
            search,
            lookup: true
          }, url)
        }
      })
    }
  }
}
