<template>
  <dx-popup v-bind="popupConfigpopupConfig" :visible.sync="modal">
    <dx-load-panel v-bind="loadConfig" :visible.sync="loading"/>
    <dx-scroll-view width="100%" height="100%">
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
import OrdemServicoTecnico from '@/api/ordem-servico-tecnico'

export default {
  name: 'Tecnico',
  components: {
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
        title: 'Gestão de técnicos na OS',
        width: '80%',
        height: '50vh'
      },
      loadConfig: {
        position: { of: 'body' },
        message: 'Carregando técnicos',
        showIndicator: true,
        showPane: true,
        shading: true,
        hideOnOutsideClick: false,
        shadingColor: 'rgba(0,0,0,0.7)'
      }
    }
  },
  methods: {
    show (data) {
      this.data = data
      const custom = {
        editing: {
          mode: 'popup',
          allowDeleting: false,
          popup: {
            showTitle: true,
            title: 'Formulário do técnico',
            height: 'auto',
            width: 'auto'
          }
        },
        onInitNewRow: e => {
          e.data.ordem_servico = data.id
          e.data.tempo = 1
        }
      }

      const gridService = new Grid(OrdemServicoTecnico, custom, { ordem_servico: data.id })
      this.gridOptions = gridService.getProps()

      this.modal = true
    }
  }
}
</script>
