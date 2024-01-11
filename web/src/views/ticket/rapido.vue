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
import TicketRapido from '@/api/ticket-rapido'

export default {
  name: 'Rapido',
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
        title: 'Atendimento Rápido',
        width: '60%',
        height: 'auto'
      },
      loadConfig: {
        position: { of: 'body' },
        message: 'Atendimento...',
        showIndicator: true,
        showPane: true,
        shading: true,
        hideOnOutsideClick: false,
        shadingColor: 'rgba(0,0,0,0.7)'
      },
      formConfig: TicketRapido.form
    }
  },
  methods: {
    async save () {
      try {
        const { id } = await TicketRapido.save(this.formData)
        this.modal = false
        notify(`Atendimento ${id} registrado e finalizado com sucesso`, 'success')
      } catch (err) {
        notify(err.message, 'error')
      }
    },
    show () {
      const form = this.$refs.form.instance
      form.updateData('nivel', 1)
      this.modal = true
    }
  }
}
</script>

<style scoped>

</style>
