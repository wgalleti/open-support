<template>
  <dx-popup v-bind="popupConfig" :visible.sync="modal">
    <dx-load-panel v-bind="loadConfig" :visible.sync="loading"/>
    <dx-scroll-view width="100%" height="100%">
      <lista ref="gridClientes" @close="refresh"/>
      <dx-data-grid v-bind="gridOptions" ref="grid"/>
    </dx-scroll-view>
  </dx-popup>
</template>

<script>
import DxPopup from 'devextreme-vue/popup'
import DxScrollView from 'devextreme-vue/scroll-view'
import DxLoadPanel from 'devextreme-vue/load-panel'
import DxDataGrid from 'devextreme-vue/data-grid'
import Grid from '@/services/grid'
import GrupoCliente from '@/api/grupo-cliente'
import Lista from '@/views/cliente/lista'

export default {
  name: 'Grupos',
  components: {
    Lista,
    DxPopup,
    DxScrollView,
    DxLoadPanel,
    DxDataGrid
  },
  watch: {
    modal (value) {
      if (!value) {
        this.$emit('close')
      }
    }
  },
  data () {
    return {
      gridOptions: null,
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
      this.data = data
      const custom = {
        editing: {
          mode: 'form'
        },
        onToolbarPreparing: (e) => {
          const toolbarItems = e.toolbarOptions.items

          toolbarItems.unshift({
            location: 'after',
            widget: 'dxButton',
            options: {
              icon: 'refresh',
              onClick: evt => {
                e.component.refresh()
              }
            }
          })

          toolbarItems.unshift({
            location: 'before',
            widget: 'dxButton',
            options: {
              icon: 'group',
              text: 'Clientes',
              hint: 'Clientes',
              onClick: evt => {
                const [data = null] = e.component.getSelectedRowsData()
                this.$refs.gridClientes.show(data)
              }
            }
          })
        }
      }

      const gridService = new Grid(GrupoCliente, custom, { cliente: data.id })
      this.gridOptions = gridService.getProps()

      this.modal = true
    }
  }
}
</script>
