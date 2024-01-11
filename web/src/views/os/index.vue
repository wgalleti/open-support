<template>
  <div class="clientes">
    <tecnico ref="gridTecnico" @close="refresh"/>
    <finalizar ref="formFinalizar" @close="refresh"/>
    <cancelar ref="formCancelar" @close="refresh"/>
    <dx-data-grid v-bind="gridOptions" ref="grid"/>
  </div>
</template>

<script>
import DxDataGrid from 'devextreme-vue/data-grid'

import Grid from '@/services/grid'
import OrdemServico from '@/api/ordem-servico'
import { dataHoje } from '@/uteis/helpers'
import notify from 'devextreme/ui/notify'
import Tecnico from '@/views/os/tecnico'
import axios from '@/plugins/axios'
import Finalizar from '@/views/os/finalizar'
import Cancelar from '@/views/os/cancelar'
import { confirm } from 'devextreme/ui/dialog'

export default {
  name: 'OrdemServico',
  components: {
    Cancelar,
    Finalizar,
    Tecnico,
    DxDataGrid
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
        mode: 'popup',
        allowDeleting: false,
        popup: {
          showTitle: true,
          title: 'Ordem de serviço',
          height: 'auto',
          width: '70%'
        }
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
            icon: 'user',
            text: 'Técnicos',
            hint: 'Adicionar Técnicos',
            onClick: evt => {
              const [data = null] = e.component.getSelectedRowsData()
              if (data === null) {
                notify('Selecione uma OS', 'error')
                return false
              }

              if (data.status >= 3) {
                notify('Status da OS não permite alteração', 'error')
                return false
              }

              this.$refs.gridTecnico.show(data)
            }
          }
        }, {
          location: 'before',
          widget: 'dxButton',
          options: {
            icon: 'check',
            text: 'Finalizar',
            hint: 'Finalizar',
            onClick: async evt => {
              const [data = null] = e.component.getSelectedRowsData()
              if (data === null) {
                notify('Selecione uma OS', 'error')
                return false
              }

              if (data.status >= 3) {
                notify('Status da OS não permite alteração', 'error')
                return false
              }

              try {
                const response = await axios.post(`servicos/ordens/${data.id}/preparar_finalizacao/`)
                const finalizar = {
                  ...response.data
                }
                this.$refs.formFinalizar.show(finalizar)
                notify('OS Finalizada')
                this.refresh()
              } catch (e) {
                notify('Falha ao finalizar a OS.' + e.message, 'error')
              }
            }
          }
        }, {
          location: 'before',
          widget: 'dxButton',
          options: {
            icon: 'close',
            text: 'Cancelar',
            hint: 'Cancelar',
            onClick: async evt => {
              const [data = null] = e.component.getSelectedRowsData()
              if (data === null) {
                notify('Selecione uma OS', 'error')
                return false
              }

              if (data.status >= 3) {
                notify('Status da OS não permite alteração', 'error')
                return false
              }

              const dialogResult = await confirm('<strong>Tem certeza que deseja cancelar a Ordem de Serviço?</strong>', 'Confirma?')

              if (!dialogResult) {
                return
              }

              this.$refs.formCancelar.show(data)
            }
          }
        })
      },
      onInitNewRow: e => {
        e.data.status = 1
        e.data.data = dataHoje()
      },
      onRowInserted: e => {
        e.component.refresh()
      },
      onRowUpdated: e => {
        e.component.refresh()
      }

    }
    const gridService = new Grid(OrdemServico, custom)
    this.gridOptions = gridService.getProps()
  }
}
</script>
