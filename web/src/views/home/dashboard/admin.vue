<template>
  <div class="admin-dashboard">
    <h1>Dashboard</h1>
  </div>
</template>

<script>
import bus from '@/plugins/bus'

export default {
  name: 'Dashboard',
  data () {
    return {}
  },
  methods: {
    async loadData () {}
  },

  mounted () {
    bus.$emit('loading')
    this.loadData()
    bus.$emit('loading')
  }
}
</script>
