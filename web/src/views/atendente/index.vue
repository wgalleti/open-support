<template>
  <div class="atendentes">
    <dx-data-grid v-bind="gridOptions"/>
  </div>
</template>

<script>
import DxDataGrid from 'devextreme-vue/data-grid'

import Grid from '@/services/grid'
import Atendente from '@/api/atendente'

export default {
  name: 'Atendente',
  components: {
    DxDataGrid
  },
  data () {
    return {
      gridOptions: null
    }
  },
  created () {
    const custom = {
      onRowInserted: e => {
        e.component.refresh()
      },
      onRowUpdated: e => {
        e.component.refresh()
      },
      onInitNewRow: e => {
        e.data.ativo = true
      }
    }
    const gridService = new Grid(Atendente, custom)
    this.gridOptions = gridService.getProps()
  }
}
</script>
