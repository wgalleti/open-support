<template>
  <dx-popup v-bind="popupConfig" :visible.sync="modal">
    <dx-load-panel v-bind="loadConfig" :visible.sync="loading"/>
      <dx-scroll-view width="100%" height="100%">
        <form @submit.prevent="save">
          <dx-form v-bind="formConfig" :form-data.sync="formData" ref="form" />
        </form>
      </dx-scroll-view>
  </dx-popup>
</template>

<script>
import DxPopup from 'devextreme-vue/popup'
import DxScrollView from 'devextreme-vue/scroll-view'
import DxLoadPanel from 'devextreme-vue/load-panel'
import DxForm from 'devextreme-vue/form'
import TicketInteracao from '@/api/ticket-interacao'
import notify from 'devextreme/ui/notify'

export default {
  name: 'ItemForm',
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
      popupConfig: {
        dragEnabled: false,
        hideOnOutsideClick: false,
        title: 'Interação do Ticket',
        width: '80%',
        height: 'auto'
      },
      loadConfig: {
        position: { of: 'body' },
        message: 'Interando o ticket',
        showIndicator: true,
        showPane: true,
        shading: true,
        hideOnOutsideClick: false,
        shadingColor: 'rgba(0,0,0,0.7)'
      },
      formConfig: TicketInteracao.form
    }
  },
  methods: {
    async save () {
      try {
        await TicketInteracao.save(this.formData)
        this.modal = false
      } catch (err) {
        notify(err.message)
      }
    },
    show (data) {
      const {
        id,
        atendente
      } = data

      const form = this.$refs.form.instance
      form.updateData('ticket', id)
      form.updateData('interno', false)
      if (!this.$store.getters['auth/isCliente']) {
        form.updateData('atendente', atendente)
      }
      this.modal = true
    }
  }
}
</script>

<style scoped>

</style>
