<template>
  <div class="clientes">
    <versao ref="formVersao" @close="refresh"/>
    <grupos ref="gridGrupo" @close="refresh"/>
    <dx-data-grid v-bind="gridOptions" ref="grid"/>
  </div>
</template>

<script>
import DxDataGrid from 'devextreme-vue/data-grid'

import Grid from '@/services/grid'
import Cliente from '@/api/cliente'
import notify from 'devextreme/ui/notify'
import Versao from '@/views/cliente/versao.vue'
import axios from '@/plugins/axios'
import Grupos from '@/views/cliente/grupos'

export default {
  name: 'Cliente',
  components: {
    Grupos,
    DxDataGrid,
    Versao
  },
  data () {
    return {
      gridOptions: null
    }
  },
  methods: {
    refresh () {
      const gridInstance = this.$refs.grid.instance
      gridInstance.refresh()
    }
  },
  created () {
    const custom = {
      editing: {
        allowUpdating: this.$store.getters['auth/isAdmin'],
        allowDeleting: this.$store.getters['auth/isAdmin'],
        allowAdding: this.$store.getters['auth/isAdmin']
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
            text: 'Grupo',
            hint: 'Grupo',
            onClick: evt => {
              const [data = null] = e.component.getSelectedRowsData()
              this.$refs.gridGrupo.show(data)
            }
          }
        }, {
          location: 'before',
          widget: 'dxButton',
          options: {
            icon: 'columnproperties',
            hint: 'Atualizar',
            onClick: evt => {
              const [data = null] = e.component.getSelectedRowsData()
              if (data === null) {
                notify('Selecione um cliente', 'error')
                return false
              }
              this.$refs.formVersao.show(data)
            }
          }
        }, {
          location: 'before',
          widget: 'dxButton',
          options: {
            icon: 'arrowdown',
            hint: 'Integrar',
            onClick: async evt => {
              await axios.post('/core/clientes/integrar/')
              e.component.refresh()
            }
          }
        })
      },
      onInitNewRow: e => {
        e.data.ativo = true
      },
      onRowInserted: e => {
        e.component.refresh()
      },
      onRowUpdated: e => {
        e.component.refresh()
      }
    }
    const gridService = new Grid(Cliente, custom)
    this.gridOptions = gridService.getProps()
  }
}
</script>
