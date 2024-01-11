<template>
  <div>
    <app-loader/>

    <v-navigation-drawer
      v-model="drawer"
      color="primary"
      :clipped="$vuetify.breakpoint.lgAndUp"
      width="180"
      dark
      app
    >
      <v-list
        dense
        nav
      >
        <v-list-item
          v-for="item in items.filter(f => f.hasOwnProperty('isAdmin') ? f.isAdmin : true)"
          :key="item.title"
          :to="item.to"
          link
        >
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar
      app
      color="primary"
      dark
      flat
      dense
      :clipped-left="$vuetify.breakpoint.lgAndUp"
      v-if="$store.state.auth.user"
    >
      <!--      <v-app-bar-nav-icon @click.stop="drawer = !drawer" v-if="!$vuetify.breakpoint.lgAndUp"></v-app-bar-nav-icon>-->
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
      <div style="width: 140px">
        <v-img src="@/assets/logo.svg" alt="" class="mr-4" style="max-width: 100%;"/>
      </div>

      <v-spacer/>
      <v-btn text v-if="$store.getters['auth/isAdmin']" @click="backup">Backup
        <v-icon>mdi-eject</v-icon>
      </v-btn>
      <v-menu open-on-hover offset-y>
        <template v-slot:activator="{ on, attrs }">
          <v-btn v-on="on" text tile>
            <span class="mr-3">{{ $store.state.auth.user.username }}</span>
            <v-avatar
              v-bind="attrs"
              size="36"
              dark
            >
              <v-img
                :src="$store.getters['auth/profileImg']"
                :alt="$store.state.auth.user.username"
                :key="idx"
                :eager="true"
              />
            </v-avatar>
          </v-btn>

        </template>

        <v-list>
          <v-list-item
            v-for="(item, index) in menu"
            :key="index"
            :to="item.to"
            link
          >
            <v-list-item-title>{{ item.title }}</v-list-item-title>
            <v-list-item-icon v-if="item.icone">
              <v-icon :color="item.iconeCor">{{ item.icone }}</v-icon>
            </v-list-item-icon>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>
  </div>
</template>

<script>
import AppLoader from '@/components/app/loader.vue'
import bus from '@/plugins/bus'
import { saveAs } from 'file-saver'

export default {
  components: {
    AppLoader
  },
  data () {
    return {
      drawer: true,
      idx: 0,
      menu: [
        {
          title: 'Perfil',
          to: '/profile'
        },
        {
          title: 'Alterar Senha',
          to: '/change-password'
        },
        {
          title: 'Sair',
          to: '/sign-out',
          icone: 'mdi-close',
          iconeCor: 'red'
        }
      ]
    }
  },
  computed: {
    items () {
      const isAdmin = this.$store.getters['auth/isAdmin']
      const isAtendente = this.$store.getters['auth/isAtendente']

      return [
        {
          title: 'Dashboard',
          icon: 'mdi-poll-box',
          to: '/'
        },
        {
          title: 'Atendentes',
          icon: 'mdi-account-check',
          to: '/atendentes',
          isAdmin
        },
        {
          title: 'Clientes',
          icon: 'mdi-account-circle',
          to: '/clientes',
          isAdmin: (isAdmin || isAtendente)
        },
        {
          title: 'OS',
          icon: 'mdi-bookmark-outline',
          to: '/os',
          isAdmin: isAdmin
        },
        {
          title: 'Tickets',
          icon: 'mdi-comment-check',
          to: '/tickets'
        }
      ]
    }
  },
  methods: {
    async backup () {
      const { data } = await this.axios.get('/core/users/backup/', {
        responseType: 'blob'
      })
      const rightNow = new Date()
      const res = rightNow.toISOString().slice(0, 10).replace(/-/g, '')
      saveAs(new Blob([data], { type: 'application/zip' }), `${res}_backup.psql.zip`)
    }
  },
  watch: {
    $route (to, from) {
      this.drawer = false
    }
  },
  mounted () {
    bus.$on('updateImg', () => {
      this.idx += 1
    })
  }
}
</script>
