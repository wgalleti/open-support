<template>
  <div class="profile">
    <v-card width="80%" class="mx-auto elevation-0">
      <v-card-text>
        <v-row>
          <v-col cols="4">
            <v-avatar :size="300" class="mx-auto">
              <v-img
                :src="imgProfile"
                :alt="$store.state.auth.user.username"
              />
            </v-avatar>
            <DxFileUploader v-bind="uploadConfig"/>
          </v-col>
          <v-col>
            <v-form @submit.prevent="salvarPerfil">
              <dx-form v-bind="config"/>
            </v-form>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import DxForm from 'devextreme-vue/form'
import DxFileUploader from 'devextreme-vue/file-uploader'
import bus from '@/plugins/bus'
import notify from 'devextreme/ui/notify'
import Usuario from '@/api/usuario'

export default {
  components: {
    DxForm,
    DxFileUploader
  },
  data () {
    return {
      formInstance: null,
      imgProfile: null,
      foto: null,
      uploadConfig: {
        multiple: false,
        files: [],
        accept: '*',
        value: [],
        uploadMode: 'instantly',
        maxFileSize: 5000000,
        uploadUrl: '/core/users/',
        allowedFileExtensions: [
          '.jpg',
          '.jpeg',
          '.png',
          '.gif'
        ],
        uploadFile: (file, progressCallback) => {
          console.log('passouw')
          const item = new FormData()

          item.append('foto', file)

          progressCallback(100)

          return this.axios.patch(
            `/core/users/${this.userID}/`,
            item,
            {
              headers: {
                'content-type': 'multipart/form-data'
              }
            }
          ).then(
            async res => {
              const { foto } = res.data
              this.imgProfile = foto
              this.$store.commit('auth/SET_USER', res.data)
              bus.$emit('updateImg')
              progressCallback(200)
            }
          )
        }
      },
      config: {
        onContentReady: e => {
          this.formInstance = e.component
        },
        colCount: 6,
        labelLocation: 'top',
        items: [
          {
            colSpan: 1,
            dataField: 'id',
            dataType: 'number',
            label: {
              text: '#'
            },
            editorOptions: {
              readOnly: true
            }
          },
          {
            colSpan: 3,
            dataField: 'username',
            dataType: 'string',
            label: {
              text: 'Usuário'
            },
            editorOptions: {
              readOnly: true
            }
          },

          {
            colSpan: 2,
            dataField: 'last_login',
            dataType: 'datetime',
            label: {
              text: 'Ultimo Acesso'
            },
            editorType: 'dxDateBox',
            editorOptions: {
              readOnly: true
            }
          },
          {
            colSpan: 3,
            dataField: 'first_name',
            dataType: 'string',
            label: {
              text: 'Nome'
            }
          },
          {
            colSpan: 3,
            dataField: 'last_name',
            dataType: 'string',
            label: {
              text: 'Sobrenome'
            }
          },
          {
            colSpan: 6,
            dataField: 'email',
            dataType: 'string',
            label: {
              text: 'Email'
            }
          },
          {
            colSpan: 6,
            itemType: 'button',
            horizontalAlignment: 'right',
            buttonOptions: {
              text: 'Salvar',
              useSubmitBehavior: true
            }
          }]
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
      bus.$emit('loading')
      await this.axios.patch(
        `/core/users/${this.userID}/`,
        this.formInstance.option('formData')
      )
      bus.$emit('loading')
      notify('Perfil atualizado com sucesso!')
    },
    async loadProfile () {
      const data = await Usuario.find(this.userID)
      const { foto = null } = data
      delete data.foto
      /* eslint-disable camelcase */
      const { id, username, last_login, first_name, last_name, email } = data
      /* eslint-disable camelcase */
      const form = { id, username, last_login, first_name, last_name, email }
      this.imgProfile = foto
      this.formInstance.option('formData', form)
    }
  },
  mounted () {
    this.imgProfile = '@/assets/user.jpg'
    this.loadProfile()
  }
}
</script>
