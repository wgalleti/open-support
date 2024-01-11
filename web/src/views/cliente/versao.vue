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
import ClienteAtualizacao from '@/api/cliente-atualizacao'
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
        title: 'Atualizar Versão do Cliente',
        width: '50%',
        height: '380'
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
      formConfig: ClienteAtualizacao.form
    }
  },
  methods: {
    async save () {
      try {
        await ClienteAtualizacao.save(this.formData)
        this.modal = false
      } catch (err) {
        notify(err.message)
      }
    },
    show (data) {
      const {
        id
      } = data

      const form = this.$refs.form.instance
      form.updateData('cliente', id)
      form.getEditor('cliente').option('disabled', true)
      this.modal = true
    }
  }
}
</script>

<style scoped>

</style>
