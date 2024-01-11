<template>
  <info ref="formInfo"/>
</template>

<script>
import Info from '@/views/ticket/info.vue'

export default {
  components: {
    Info
  },
  name: 'detalhes',
  data () {
    return {
      data: null
    }
  },
  methods: {
    show (id) {
      this.data = { id }
      this.$refs.formInfo.show(this.data)
    }
  },
  mounted () {
    this.show(this.$route.params.id)
  }
}
</script>

<style scoped>

</style>
