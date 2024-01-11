<template>
  <div class="home">
    <dashboard/>
  </div>
</template>

<script>
import notify from 'devextreme/ui/notify'
import Dashboard from '@/views/home/dashboard/index'

export default {
  name: 'Home',
  components: {
    Dashboard
  },
  mounted () {
    notify(`Bem vindo ${this.$store.state.auth.user.username}`, 'success', 5000)
  }
}
</script>
