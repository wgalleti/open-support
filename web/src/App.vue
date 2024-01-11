<template>
  <v-app id="app">
    <component :is="layout">
      <router-view :key="$route.fullPath"></router-view>
    </component>
  </v-app>
</template>

<script>

export default {
  computed: {
    layout () {
      return this.$route.meta.layout || 'layout-default'
    }
  }
}
</script>
