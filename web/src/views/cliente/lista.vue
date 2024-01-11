<template>
  <dx-popup v-bind="popupConfig" :visible.sync="modal">
    <dx-load-panel v-bind="loadConfig" :visible.sync="loading"/>
    <dx-scroll-view width="100%" height="100%">
      <dx-data-grid v-bind="gridOptions" ref="grid"/>
    </dx-scroll-view>
  </dx-popup>
</template>

<script>
import DxDataGrid from 'devextreme-vue/data-grid'
import axios from '@/plugins/axios'
import CustomStore from 'devextreme/data/custom_store'
import bus from '@/plugins/bus'
import DxPopup from 'devextreme-vue/popup'
import DxScrollView from 'devextreme-vue/scroll-view'
import DxLoadPanel from 'devextreme-vue/load-panel'
import { colunas, formulario } from '@/api/grupo_cliente-cliente'

export default {
  name: 'Lista',
  components: {
    DxDataGrid,
    DxPopup,
    DxScrollView,
    DxLoadPanel
  },
  data () {
    return {
      gridOptions: null,
      dataSource: null,
      data: {},
      loading: false,
      modal: false,
      popupConfig: {
        dragEnabled: false,
        hideOnOutsideClick: false,
        title: 'Gestão de grupos de Clientes',
        width: '80%',
        height: '50vh'
      },
      loadConfig: {
        position: { of: 'body' },
        message: 'Carregando grupos',
        showIndicator: true,
        showPane: true,
        shading: true,
        hideOnOutsideClick: false,
        shadingColor: 'rgba(0, 0, 0, 0.7)'
      }
    }
  },
  methods: {
    refresh () {
      const gridInstance = this.$refs.grid.instance
      gridInstance.refresh()
    },
    show (data) {
      const { id } = data
      const dataSource = new CustomStore({
        key: 'id',
        load: async options => {
          bus.$emit('loading')
          try {
            const { data } = await axios.get(`/core/grupos/${id}/`)

            bus.$emit('loading')

            return {
              data: data.clientes,
              totalCount: data.clientes.length
            }
          } catch (e) {
            console.log(e)
            return {
              data: [],
              totalCount: 0
            }
          }
        },
        insert: async data => {
          bus.$emit('loading')
          const resp = await axios.post(`/core/grupos/${id}/adicionar/`, data)
          bus.$emit('loading')
          return resp
        },
        remove: async key => {
          bus.$emit('loading')
          const resp = await axios.post(`/core/grupos/${id}/remover/`, { id: key })
          bus.$emit('loading')
          return resp
        }
      })

      this.gridOptions = {
        dataSource,
        columns: colunas,
        editing: {
          allowAdding: true,
          allowDeleting: true,
          enable: true,
          mode: 'form',
          useIcons: true,
          form: {
            ...formulario
          }
        }
      }

      this.modal = true
    }
  }
}
</script>
