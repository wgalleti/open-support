<template>
  <div class="tickets">
    <direcionar ref="formDirecionar" @close="refresh"/>
    <info ref="formInfo" @close="refresh"/>
    <rapido ref="formRapido" @close="refresh"/>
    <filtros ref="filtro" @filter="loadFilters" :visible="showFilter"/>
    <dx-data-grid v-bind="gridOptions" ref="grid">
      <template #dataRowTemplate="{ data: rowInfo }">
        <fragment>
          <tr class="main-row">
            <td rowspan="2" class="text-4xl">{{ rowInfo.data.id }}</td>
            <td class="text-caption">
              {{ rowInfo.data.cliente_display }} - {{ rowInfo.data.versao }}
            </td>
            <td class="text-caption">{{ rowInfo.data.data_display }}</td>
            <td class="text-caption">{{ rowInfo.data.atendente_display }}</td>
            <td class="text-caption">{{ rowInfo.data.nivel_display }}</td>
            <td class="text-caption">{{ rowInfo.data.status_display }}</td>
            <td class="text-caption">{{ rowInfo.data.departamento_display }}</td>
          </tr>
          <tr class="notes-row">
            <td colspan="7">
              <div class="text-sm font-semibold">{{ rowInfo.data.titulo }}</div>
            </td>
          </tr>
        </fragment>
      </template>
    </dx-data-grid>
  </div>
</template>

<script>
import DxDataGrid from 'devextreme-vue/data-grid'
import notify from 'devextreme/ui/notify'
import { confirm } from 'devextreme/ui/dialog'

import Grid from '@/services/grid'
import Ticket from '@/api/ticket'

import Info from '@/views/ticket/info.vue'
import Direcionar from '@/views/ticket/direcionar.vue'
import axios from '@/plugins/axios'
import Rapido from '@/views/ticket/rapido'
import Filtros from '@/views/ticket/filtros'

export default {
  name: 'Ticket',
  components: {
    Filtros,
    Rapido,
    DxDataGrid,
    Info,
    Direcionar
  },
  data () {
    return {
      filtros: {},
      fileUpload: [],
      gridService: null,
      showFilter: false
    }
  },
  methods: {
    refresh () {
      const gridInstance = this.$refs.grid.instance
      gridInstance.refresh()
    },
    loadFilters (e) {
      this.filtros = e
      const gridInstance = this.$refs.grid.instance
      gridInstance.refresh()
    }
  },
  computed: {
    gridOptions () {
      const custom = {
        rowAlternationEnabled: true,
        editing: {
          mode: 'popup',
          allowUpdating: false,
          allowDeleting: false,
          popup: {
            showTitle: true,
            title: 'Formulário de Ticket',
            height: 'auto',
            width: '80%'
          }
        },
        onToolbarPreparing: (e) => {
          const toolbarItems = e.toolbarOptions.items
          const self = this

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

          const filters = [
            {
              id: 'finalizados',
              nome: 'Finalizados'
            },
            {
              id: 'sem_atendimento',
              nome: 'Sem Atendimento'
            }
          ]

          toolbarItems.unshift({
            location: 'before',
            widget: 'dxSelectBox',
            options: {
              dataSource: filters,
              displayExpr: 'nome',
              valueExpr: 'id',
              showClearButton: true,
              onValueChanged ({ value }) {
                self.gridService.baseFilter = {
                  personalizado: value
                }
                e.component.refresh()
              }
            }
          })

          toolbarItems.unshift({
            location: 'before',
            widget: 'dxButton',
            visible: this.$store.getters['auth/isAdmin'],
            options: {
              icon: 'check',
              text: 'Ordem Serviço',
              hint: 'Gerar OS',
              onClick: async evt => {
                const [data = null] = e.component.getSelectedRowsData()
                if (data === null) {
                  notify('Selecione um ticket', 'error')
                  return false
                }
                const {
                  id = 0,
                  nivel = 1
                } = data

                if (nivel <= 1) {
                  notify('Não é possível gerar OS para um chamdo de nível 1.', 'error')
                  return
                }

                const dialogResult = await confirm('<strong>Tem certeza que deseja gerar uma OS?</strong>', 'Confirma?')

                if (!dialogResult) {
                  return
                }

                if (data.os) {
                  notify('Já existe uma OS para esse ticket', 'error')
                  return
                }

                try {
                  const { data } = await axios.post(`/chamados/tickets/${id}/gerar_os/`)
                  notify(`Foi gerada a OS ${data.id}.`)
                  e.component.refresh()
                } catch (e) {
                  notify(e, 'error')
                }
              }
            }
          }, {
            location: 'before',
            widget: 'dxButton',
            visible: !this.$store.getters['auth/isCliente'],
            options: {
              icon: 'arrowup',
              hint: 'Subir o nível do Ticket',
              onClick: async evt => {
                const [data = null] = e.component.getSelectedRowsData()
                if (data === null) {
                  notify('Selecione um ticket', 'error')
                  return false
                }
                const {
                  id = 0,
                  nivel = 1
                } = data

                if (nivel >= 3) {
                  notify('Chamado no nível maximo.', 'error')
                  return
                }

                const dialogResult = await confirm('<strong>Tem certeza que deseja subir o nível do chamado?</strong>', 'Confirma?')

                if (!dialogResult) {
                  return
                }

                try {
                  await axios.post(`/chamados/tickets/${id}/upgrade/`)
                  e.component.refresh()
                } catch (e) {
                  notify(e, 'error')
                }
              }
            }
          }, {
            location: 'before',
            widget: 'dxButton',
            options: {
              icon: 'info',
              hint: 'Detalhes',
              onClick: evt => {
                const [data = null] = e.component.getSelectedRowsData()
                if (data === null) {
                  notify('Selecione um ticket', 'error')
                  return false
                }
                this.$refs.formInfo.show(data)
              }
            }
          }, {
            location: 'before',
            widget: 'dxButton',
            options: {
              icon: 'card',
              hint: 'Interação',
              onClick: evt => {
                const [data = null] = e.component.getSelectedRowsData()
                if (data === null) {
                  notify('Selecione um ticket', 'error')
                  return false
                }
                this.$refs.formDirecionar.show(data)
              }
            }
          }, {
            location: 'after',
            widget: 'dxButton',
            visible: !this.$store.getters['auth/isCliente'],
            options: {
              icon: 'plus',
              text: 'Rápido',
              hint: 'Atendimento rápido',
              onClick: evt => {
                this.$refs.formRapido.show()
              }
            }
          }, {
            location: 'after',
            widget: 'dxButton',
            options: {
              icon: 'filter',
              text: 'Filtro',
              hint: 'Filtro Avançado',
              onClick: evt => {
                this.showFilter = !this.showFilter
              }
            }
          })
        },
        onInitNewRow: e => {
          if (this.$store.getters['auth/isCliente']) {
            e.data.cliente = this.$store.state.auth.user.cliente
          }
        },
        onCellPrepared: e => {
          if (e.rowType === 'data' && (e.column.name === 'nivel' || e.column.name === 'cliente_display')) {
            e.cellElement.style.fontWeight = '600'
          }

          if (e.rowType === 'data' && e.column.name === 'nivel' && e.data.nivel === 1) {
            e.cellElement.style.color = '#035C96'
          }

          if (e.rowType === 'data' && e.column.name === 'nivel' && e.data.nivel === 2) {
            e.cellElement.style.color = '#2A9DF4'
          }

          if (e.rowType === 'data' && e.column.name === 'nivel' && e.data.nivel === 3) {
            e.cellElement.style.color = '#03204C'
          }
        },
        onRowPrepared: e => {
          if (e.rowType === 'data' && e.data.prioridade === 'ALTA') {
            e.rowElement.style.color = '#9B261E'
            e.rowElement.style.fontWeight = 600
          }

          if (e.rowType === 'data' && e.data.status === 'RESOLVIDO') {
            e.rowElement.style.color = '#4C9A2A'
            e.rowElement.style.fontWeight = 600
          }

          if (e.rowType === 'data' && e.data.status === 'PROXIMA_VERSAO') {
            e.rowElement.style.color = '#502D7F'
            e.rowElement.style.fontWeight = 600
          }
        },
        onEditorPreparing: e => {
          if (e.parentType === 'dataRow' && e.dataField === 'arquivos') {
            e.editorName = 'dxFileUploader'
            e.editorOptions.value = []
            e.editorOptions.multiple = true
            e.editorOptions.uploadMode = 'instantly'
            e.editorOptions.maxFileSize = '5000000'
            e.editorOptions.allowedFileExtensions = [
              '.jpg',
              '.jpeg',
              '.gif',
              '.png',
              '.xls',
              '.xlsx',
              '.doc',
              '.docx',
              '.pdf',
              '.rar',
              '.zip',
              '.7z',
              '.sql',
              '.mp4',
              '.xml'
            ]
            e.editorOptions.uploadFile = async (file, progressCallback) => {
              const item = new FormData()

              item.append('arquivo', file)
              item.append('usuario', this.$store.state.auth.user.id)

              progressCallback(100)

              const { data } = this.axios.post(
                '/chamados/anexos/',
                item,
                {
                  headers: {
                    'content-type': 'multipart/form-data'
                  }
                }
              ).then(
                res => {
                  progressCallback(200)
                  this.fileUpload.push(res.data.id)
                  return this.fileUploaded
                }
              )

              e.setValue(this.fileUpload)

              return data
            }
          }
        }
      }
      const gridService = new Grid(Ticket, custom, this.filtros)
      this.gridService = gridService
      return gridService.getProps()
    }
  }
}
</script>

<style>
#gridContainer {
  height: 450px;
}

.dx-row img {
  height: 100px;
}

#gridContainer tr.main-row td:not(:first-child) {
  height: 21px;
}

#gridContainer tr.notes-row {
  white-space: normal;
  vertical-align: top;
}

#gridContainer tr.notes-row td {
  height: 70px;
  color: #999;
}

.dark #gridContainer tr.notes-row td {
  color: #777;
}

#gridContainer tbody.dx-state-hover {
  background-color: #ebebeb;
}

.dark #gridContainer tbody.dx-state-hover {
  background-color: #484848;
}

#gridContainer tbody.dx-state-hover tr.main-row td {
  color: #000;
}

.dark #gridContainer tbody.dx-state-hover tr.main-row td {
  color: #ccc;
}

#gridContainer tbody.dx-state-hover tr.notes-row td {
  color: #888;
}
</style>
