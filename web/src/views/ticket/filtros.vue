<template>
  <v-card flat class="my-2" v-if="showing">
    <form @submit.prevent="filtrar">
      <DxForm ref="formFilter" v-bind="formOptions" :formData.sync="formData"/>
    </form>
  </v-card>
</template>

<script>
import DxForm from 'devextreme-vue/form'
import Status from '@/api/status'
import Prioridade from '@/api/prioridade'
import Atendente from '@/api/atendente'
import Departamento from '@/api/departamento'

export default {
  name: 'filtros',
  props: {
    visible: {
      type: Boolean,
      default: false
    }
  },
  components: {
    DxForm
  },
  data () {
    return {
      formData: {},
      showing: false
    }
  },
  watch: {
    visible (value) {
      this.showing = value
    }
  },
  methods: {
    filtrar () {
      this.$emit('filter', this.formData)
    }
  },
  computed: {
    formOptions () {
      return {
        focusStateEnabled: true,
        hoverStateEnabled: true,
        activeStateEnabled: true,
        scrollingEnabled: true,
        tabIndex: 0,
        labelLocation: 'top',
        showValidationSummary: true,
        showColonAfterLabel: false,
        colCount: 12,
        items: [
          { dataField: 'id' },
          {
            colSpan: 2,
            dataField: 'status',
            editorType: 'dxSelectBox',
            editorOptions: {
              dataSource: Status.makeLookup(),
              displayExpr: 'descricao',
              valueExpr: 'id',
              showClearButton: true,
              searchEnabled: true
            }
          },
          {
            colSpan: 2,
            dataField: 'prioridade',
            editorType: 'dxSelectBox',
            editorOptions: {
              dataSource: Prioridade.makeLookup(),
              displayExpr: 'descricao',
              valueExpr: 'id',
              showClearButton: true,
              searchEnabled: true
            }
          },
          {
            colSpan: 2,
            dataField: 'atendente',
            editorType: 'dxSelectBox',
            editorOptions: {
              dataSource: Atendente.makeLookup(),
              displayExpr: 'nome',
              valueExpr: 'id',
              showClearButton: true,
              searchEnabled: true
            }
          },
          {
            dataField: 'departamento',
            colSpan: 2,
            editorType: 'dxSelectBox',
            editorOptions: {
              dataSource: Departamento.makeLookup(),
              displayExpr: 'descricao',
              valueExpr: 'id',
              showClearButton: true,
              searchEnabled: true
            }
          },
          {
            colSpan: 1,
            dataField: 'de',
            editorType: 'dxDateBox',
            editorOptions: {
              dateSerializationFormat: 'yyyy-MM-dd'
            }
          },
          {
            colSpan: 1,
            dataField: 'ate',
            editorType: 'dxDateBox',
            editorOptions: {
              dateSerializationFormat: 'yyyy-MM-dd'
            }
          },
          {
            itemType: 'button',
            verticalAlignment: 'bottom',
            horizontalAlignment: 'center',
            buttonOptions: {
              text: 'Pesquisar',
              useSubmitBehavior: true
            }
          }
        ]
      }
    }
  }
}
</script>
