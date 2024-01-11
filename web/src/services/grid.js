import axios from '@/plugins/axios'
import _ from 'lodash'
import CustomStore from 'devextreme/data/custom_store'
import bus from '@/plugins/bus'

export default class Grid {
  constructor (model, custom = {}, baseFilter = {}) {
    this.model = model
    this.columns = model.columns
    this.form = model.form
    this.custom = custom
    this.axios = axios
    this.searchTerm = null
    this.baseFilter = baseFilter
  }

  /**
   * Make a devexpress dataSource
   * @returns {CustomStore}
   */
  makeDataSource () {
    return new CustomStore({
      key: this.model.primaryKey,
      load: async options => {
        let ordering = null
        if (options.sort) {
          ordering = options.sort.map(s => s.desc ? `-${s.selector}` : s.selector).join()
        }
        const { skip, take } = options
        bus.$emit('loading')
        const data = await this.model.filter({
          skip,
          take,
          ordering,
          search: this.searchTerm,
          ...this.baseFilter
        })

        bus.$emit('loading')

        if (skip === undefined) {
          return {
            data,
            totalCount: data.length
          }
        }
        return {
          data: data.data,
          totalCount: data.total
        }
      },
      insert: async data => {
        bus.$emit('loading')
        const resp = await this.model.save(data)
        bus.$emit('loading')
        return resp
      },
      update: async (key, data) => {
        bus.$emit('loading')
        const resp = await this.model.save(data, key)
        bus.$emit('loading')
        return resp
      },
      remove: async key => {
        bus.$emit('loading')
        const resp = await this.model.remove(key)
        bus.$emit('loading')
        return resp
      }
    })
  }

  getProps () {
    const { readOnly = false } = this.custom
    delete this.custom.readOnly

    const baseProps = {
      allowColumnReordering: true,
      showBorders: false,
      showColumnLines: false,
      showRowLines: false,
      rowAlternationEnabled: true,
      columnAutoWidth: true,
      allowColumnResizing: true,
      selection: {
        mode: 'single'
      },
      // stateStoring: {
      //   enabled: true,
      //   type: 'localStorage',
      //   storageKey: `gState${this.model.url.replaceAll('/', '')}`
      // },
      paging: {
        pageSize: 10
      },
      remoteOperations: {
        filtering: true,
        paging: true
      },
      editing: {
        enable: true,
        mode: 'form',
        useIcons: true,
        allowUpdating: !readOnly,
        allowDeleting: !readOnly,
        allowAdding: !readOnly,
        form: {
          focusStateEnabled: true,
          hoverStateEnabled: true,
          activeStateEnabled: true,
          scrollingEnabled: true,
          tabIndex: 0,
          labelLocation: 'top',
          showValidationSummary: true,
          showColonAfterLabel: false
        },
        popup: {
          shadingColor: 'rgba(0,0,0,0.7)'
        }
      },
      searchPanel: {
        visible: true,
        searchVisibleColumnsOnly: true,
        width: 300
      },
      loadPanel: {
        enabled: false,
        shading: true,
        shadingColor: 'rgba(255,255,255, 0.7)'
      },
      columnFixing: {
        enable: true
      },
      export: {
        enabled: true,
        allowExportSelectedData: true,
        fileName: 'data-from-web'
      },
      columnChooser: {
        allowSearch: true,
        enabled: false,
        height: 260,
        mode: 'dragAndDrop',
        searchTimeout: 500,
        width: 250
      },
      dateSerializationFormat: 'yyyy-MM-dd',
      focusStateEnabled: true,
      height: '91vh',
      scrolling: {
        mode: 'infinite'
      }
    }

    baseProps.dataSource = this.makeDataSource()
    baseProps.columns = this.columns
    baseProps.onOptionChanged = (e) => {
      if (e.fullName === 'searchPanel.text') {
        this.searchTerm = e.value
      }
    }

    baseProps.onToolbarPreparing = (e) => {
      const toolbarItems = e.toolbarOptions.items

      toolbarItems.unshift({
        location: 'after',
        widget: 'dxButton',
        options: {
          icon: 'refresh',
          onClick (evt) {
            e.component.refresh()
          }
        }
      })
    }

    const form = {
      editing: {
        form: {
          ...this.form
        }
      }
    }

    return _.merge(baseProps, form, this.custom)
  }
}
