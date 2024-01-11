<template>
  <v-dialog v-model="modal" :fullscreen="true">
    <v-card>
      <v-card-title color="accent" dark>
        <a :href="`https://suporte.hifuzion.com.br/#/detalhes/${ticket.id}`" target="_blank">Ticket {{ ticket.id }} do
          cliente {{ ticket.cliente_display }}</a>
        <v-spacer/>
        <v-icon @click="modal = !modal">mdi-close</v-icon>
      </v-card-title>
      <v-card-text class="white text--primary pt-3">

        <v-timeline align-top :dense="$vuetify.breakpoint.smAndDown">
          <v-timeline-item
              left
              fill-dot
          >
            <span slot="opposite"
                  v-if="ticket.aberto_cliente">{{ ticket.cliente_display }} em {{ ticket.data_display }}</span>
            <span slot="opposite"
                  v-else>Aberto por <strong>{{ ticket.usuario_display }}</strong> para o cliente <strong>{{ ticket.cliente_display }}</strong> em <strong>{{ ticket.data_display }}</strong></span>
            <v-card
                color="primary"
                dark
            >
              <v-card-title class="title">{{ ticket.titulo }} em {{ ticket.data_display }}</v-card-title>
              <v-card-text class="white text--primary pt-3">
                <div :id="`html-ticket-${ticket.id}`" v-html="ticket.descricao"></div>

                <v-list dense light v-if="ticket.anexos_display.length > 0">
                  <v-subheader class="text--secondary">Anexos</v-subheader>
                  <v-list-item
                      v-for="i in ticket.anexos_display"
                      :key="i.id"
                  >
                    <v-list-item-icon>
                      <v-icon>mdi-file</v-icon>
                    </v-list-item-icon>
                    <v-list-item-content>
                      <v-list-item-title @click="openAnexo(i.arquivo)" v-text="i.nome"></v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card>
          </v-timeline-item>

          <v-timeline-item
              v-for="a in andamentos.filter(a => this.$store.state.auth.user.is_cliente ? a.interno === false : true)"
              :key="a.id"
              :right="a.cliente_atendente === 'atendente'"
              :left="a.cliente_atendente === 'cliente'"
              fill-dot
          >
            <span slot="opposite">{{ a.data_display }}</span>
            <v-card
                :color="a.cliente_atendente === 'cliente' ? 'primary' : 'secondary'"
                dark
            >
              <v-card-title class="title">{{ a.usuario_display }}</v-card-title>
              <v-card-text class="white text--primary pt-3">
                <div :key="`html-interacao-${a.id}`" v-html="a.descricao"></div>
                <v-list dense light v-if="a.anexos_display.length > 0">
                  <v-subheader class="text--secondary">Anexos</v-subheader>
                  <v-list-item
                      v-for="i in a.anexos_display"
                      :key="i.id"
                  >
                    <v-list-item-icon>
                      <v-icon>mdi-file</v-icon>
                    </v-list-item-icon>
                    <v-list-item-content>
                      <v-list-item-title @click="openAnexo(i.arquivo)" v-text="i.nome"></v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card>
          </v-timeline-item>
        </v-timeline>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
import Ticket from '@/api/ticket'

export default {
  name: 'ItemForm',
  watch: {},
  data () {
    return {
      ticket: {
        anexos_display: []
      },
      andamentos: [],
      modal: false,
      popupConfig: {
        dragEnabled: false,
        hideOnOutsideClick: false,
        title: 'Detalhes do Ticket',
        width: '95%',
        height: '95vh'
      },
      items: [
        {
          color: 'red lighten-2',
          icon: 'mdi-star'
        },
        {
          color: 'purple darken-1',
          icon: 'mdi-book-variant'
        },
        {
          color: 'green lighten-1',
          icon: 'mdi-airballoon'
        },
        {
          color: 'indigo',
          icon: 'mdi-buffer'
        }
      ]
    }
  },
  methods: {
    openAnexo (file) {
      const path = this.getFilePath(file)
      const w = window.screen.width / 2
      const h = window.screen.height / 2
      const l = (screen.width / 2) - (w / 2)
      const t = (screen.height / 2) - (h / 2)
      window.open(path, '_blank', `location=yes,height=${h},width=${w},top=${t},right=${l},scrollbars=yes,status=yes`)
    },
    getFilePath (file) {
      return `${process.env.VUE_APP_BASE_URL}${file}`
    },
    async show (data = null) {
      this.modal = true

      if (data !== null) {
        const ticket = await Ticket.find(data.id, 'detalhes/?all')
        const { andamentos = [] } = ticket
        this.ticket = ticket
        this.andamentos = andamentos
      }
    }
  }
}
</script>

<style scoped>

</style>
