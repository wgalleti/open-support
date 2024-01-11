<template>
  <v-dialog
    v-model="dialog"
    persistent
    width="250"
    overlay-opacity="0.8"
  >
    <v-card color="primary" dark>
      <v-card-title>
        <v-img src="@/assets/logo-i.png" alt="" :max-width="200" class="mr-4"/>
      </v-card-title>
      <v-card-text>
        <v-progress-linear
          indeterminate
          color="white"
          class="mb-0"
        />
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
import bus from '@/plugins/bus'

export default {
  data () {
    return {
      dialog: false
    }
  },
  mounted () {
    bus.$on('loading', () => {
      this.dialog = !this.dialog
    })
  }
}
</script>
