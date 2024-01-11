<template>
  <v-app id="app">
    <AppBar />

    <v-main>
      <v-container fluid grid-list-lg>
        <slot />
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import AppBar from '@/components/app/navbar.vue'

export default {
  components: {
    AppBar
  }
}
</script>
