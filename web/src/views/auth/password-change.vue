<template>
  <div class="password-change">
    <v-card width="250px" class="mx-auto elevation-0">
      <v-form @submit.prevent="salvarPerfil" class="mt-10">
        <dx-form v-bind="config"/>
      </v-form>
    </v-card>
  </div>
</template>

<script>
import DxForm from 'devextreme-vue/form'
import bus from '@/plugins/bus'
import notify from 'devextreme/ui/notify'

export default {
  components: {
    DxForm
  },
  data () {
    return {
      formInstance: null,
      config: {
        onContentReady: e => {
          this.formInstance = e.component
        },
        labelLocation: 'top',
        items: [
          {
            dataField: 'new_password1',
            dataType: 'string',
            label: {
              text: 'Nova Senha'
            },
            editorOptions: {
              mode: 'password'
            },
            validationRules: [
              {
                type: 'required',
                message: 'Nova senha é obrigatório'
              }
            ]
          },
          {
            dataField: 'new_password2',
            dataType: 'string',
            label: {
              text: 'Confirmar'
            },
            editorOptions: {
              mode: 'password'
            },
            validationRules: [
              {
                type: 'required',
                message: 'Confirmar é obrigatório'
              }
            ]
          },
          {
            itemType: 'button',
            horizontalAlignment: 'right',
            buttonOptions: {
              text: 'Alterar',
              useSubmitBehavior: true
            }
          }
        ]
      }
    }
  },
  computed: {
    userID () {
      return this.$store.state.auth.user.id
    }
  },
  methods: {
    async salvarPerfil () {
      console.log('Alterando')
      bus.$emit('loading')
      try {
        await this.axios.post(
          'auth/password/change/',
          this.formInstance.option('formData')
        )
        notify('Perfil atualizado com sucesso!')
      } catch (e) {
        console.log(e)
      }

      bus.$emit('loading')
    }
  }
}
</script>
