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
import OrdemServicoItem from '@/api/ordem-servico-item'

export default {
  name: 'Finalizar',
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
        title: 'Finalizar OS',
        width: '600',
        height: 'auto'
      },
      loadConfig: {
        position: { of: 'body' },
        message: 'Finalizando...',
        showIndicator: true,
        showPane: true,
        shading: true,
        hideOnOutsideClick: false,
        shadingColor: 'rgba(0,0,0,0.7)'
      },
      formConfig: OrdemServicoItem.form
    }
  },
  methods: {
    async save () {
      try {
        await axios.post(`/servicos/ordens/${this.id}/finalizar/`, this.formData)
        this.modal = false
      } catch (err) {
        notify(err.message)
      }
    },
    show (data) {
      const {
        ordem_servico: ordemServico,
        servico,
        valor,
        tempo,
        descricao,
        data_encerramento: dataEncerramento,
        gerar_integracao: gerarIntegracao,
        desconto = 0
      } = data
      this.id = ordemServico

      const form = this.$refs.form.instance
      form.updateData('ordem_servico', ordemServico)
      form.updateData('servico', servico)
      form.updateData('valor', valor)
      form.updateData('tempo', tempo)
      form.updateData('descricao', descricao)
      form.updateData('desconto', desconto)
      form.updateData('data_encerramento', dataEncerramento)
      form.updateData('gerar_integracao', gerarIntegracao)

      this.modal = true
    }
  }
}
</script>

<style scoped>

</style>
