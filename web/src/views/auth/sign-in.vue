<template>
  <div class="login">
    <svg viewBox="0 0 400 150" preserveAspectRatio="none" style="height: 100%; width: 100%;">
      <path d="M0.00,92.10 C190.83,192.92 280.30,8.39 500.00,109.03 L500.00,0.00 L0.00,0.00 Z"
            style="stroke: none;fill: #555555;"></path>
    </svg>

    <div>
      <v-img src="@/assets/logo-i.png" alt="" :max-width="250" class="ma-10"/>
    </div>

    <form @submit.prevent="login" class="form">
      <dx-form
        :form-data.sync="credentials"
        v-bind="formConfig"
      />
    </form>
  </div>
</template>

<script>
import DxForm from 'devextreme-vue/form'
import notify from 'devextreme/ui/notify'
import bus from '@/plugins/bus'

export default {
  name: 'Sigin',
  components: {
    DxForm
  },
  data () {
    return {
      credentials: {},
      formConfig: {
        labelLocation: 'top',
        showColonAfterLabel: false,
        validationGroup: 'loginValidation',
        showValidationSummary: false,
        items: [
          {
            dataField: 'username',
            label: {
              text: 'Usuário / Email'
            },
            validationRules: [
              {
                type: 'required',
                message: 'Usuário ou email é obrigatório'
              }
            ]
          },
          {
            dataField: 'password',
            label: {
              text: 'Senha'
            },
            editorOptions: {
              mode: 'password'
            },
            validationRules: [
              {
                type: 'required',
                message: 'Senhá é obrigatório'
              }
            ]
          },
          {
            itemType: 'button',
            buttonOptions: {
              text: 'Login',
              icon: 'user',
              type: 'default',
              useSubmitBehavior: true,
              horizontalAlignment: 'Right',
              verticalAlignment: 'Bottom',
              width: '100%'
            }
          }

        ]
      }
    }
  },
  methods: {
    async login () {
      bus.$emit('loading')
      try {
        await this.$store.dispatch('auth/doSignIn', this.credentials)
        this.$router.push('/tickets')
      } catch (e) {
        notify(e.toString(), 'error', 300)
      }
      bus.$emit('loading')
    }
  }
}
</script>

<style lang="scss">
  svg {
    display: inline-block;
    position: absolute;
    top: 0;
    left: 0;
  }

  .login {
    display: flex;
    flex-direction: column; /* make main axis vertical */
    justify-content: center; /* center items vertically, in this case */
    align-items: center;
    width: 100%;
    height: 100vh;

    .form {
      width: 320px;
      height: auto;
      background: #fff;
      z-index: 1;
      padding: 20px;
      border-radius: 5px;
    }
  }
</style>
