<template>
  <dx-popup v-bind="popupConfig" :visible.sync="modal">
    <dx-load-panel v-bind="loadConfig" :visible.sync="loading"/>
    <dx-scroll-view width="100%" height="100%">
      <form @submit.prevent="save">
        <dx-form v-bind="formConfig" :form-data.sync="formData" ref="form"/>
      </form>
    </dx-scroll-view>
  </dx-popup>
</template>

<script>
import DxPopup from 'devextreme-vue/popup'
import DxScrollView from 'devextreme-vue/scroll-view'
import DxLoadPanel from 'devextreme-vue/load-panel'
import DxForm from 'devextreme-vue/form'
import notify from 'devextreme/ui/notify'
import axios from '@/plugins/axios'
import OrdemServicoCancelamento from '@/api/ordem-servico-cancelamento'
import { dataHoje } from '@/uteis/helpers'

export default {
  name: 'Cancelar',
  components: {
    DxPopup,
    DxScrollView,
    DxLoadPanel,
    DxForm
  },
  watch: {
    modal (value) {
      if (!value) {
        const form = this.$refs.form.instance
        form.resetValues()
        this.$emit('close')
      }
    }
  },
  data () {
    return {
      formData: {},
      loading: false,
      modal: false,
      id: null,
      popupConfig: {
        dragEnabled: false,
        hideOnOutsideClick: false,
        title: 'Cancelar OS',
        width: '400',
        height: 'auto'
      },
      loadConfig: {
        position: { of: 'body' },
        message: 'Cancelado...',
        showIndicator: true,
        showPane: true,
        shading: true,
        hideOnOutsideClick: false,
        shadingColor: 'rgba(0,0,0,0.7)'
      },
      formConfig: OrdemServicoCancelamento.form
    }
  },
  methods: {
    async save () {
      try {
        await axios.post(`/servicos/ordens/${this.id}/cancelar/`, this.formData)
        this.modal = false
      } catch (err) {
        notify(err.message)
      }
    },
    show (data) {
      const { id } = data
      this.id = id

      this.modal = true
    }
  }
}
</script>

<style scoped>

</style>
