<template>
  <div>
    <v-container>
      <v-row>
        <v-col v-for="i in Object.keys(resumo)" :key="i">
          <div class="h-[80px] border rounded text-primary text-center pt-2 text-4xl flex flex-column">
            {{ resumo[i] }}
            <small class="text-caption">{{ i }}</small>

          </div>
        </v-col>
      </v-row>

      <v-row class="mt-10">
        <v-col cols="12" md="3 mt-3">
          <v-row v-for="i in status" :key="i.status_display" class="border rounded mb-[1px]">
            <div class="text-caption flex justify-between items-center my-3 px-2">
              <div class="text-sm text-truncate">{{ i['status_display'] }}</div>
              <div class="text-xs h-[25px] w-[25px] rounded-full bg-primary">
                <div class="h-[100%] w-[100%] text-white flex items-center justify-center font-bold">
                  {{ i['total_ticktes'] }}
                </div>
              </div>
            </div>
          </v-row>

        </v-col>
        <v-col cols="12" md="9">

            <div class="border pa-3 rounded">
              <DxChart
                id="chart"
                v-bind="chartAtendenteConfig"
              />
            </div>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import axios from '@/plugins/axios'
import bus from '@/plugins/bus'
import DxChart from 'devextreme-vue/chart'

export default {
  name: 'Dashboard',
  components: {
    DxChart
  },
  data () {
    return {
      resumo: {},
      status: {},
      atendente: []
    }
  },
  computed: {
    chartAtendenteConfig () {
      return {
        rotated: true,
        onPointClick (e) {
          e.target.select()
        },
        legend: {
          visible: false
        },
        dataSource: this.atendente,
        series: [
          {
            argumentField: 'atendente_nome',
            valueField: 'total_ticktes',
            name: 'Atendentes',
            type: 'stackedBar',
            color: '#555555',
            hoverMode: 'allArgumentPoints',
            selectionMode: 'allArgumentPoints',
            label: {
              visible: true,
              format: {
                type: 'fixedPoint',
                precision: 0
              }
            }
          },
          {
            argumentField: 'atendente_nome',
            valueField: 'finalizados',
            name: 'Finalizados',
            type: 'stackedBar',
            color: '#008a02',
            hoverMode: 'allArgumentPoints',
            selectionMode: 'allArgumentPoints',
            label: {
              visible: true,
              format: {
                type: 'fixedPoint',
                precision: 0
              }
            }
          }
        ]
      }
    }
  },
  methods: {
    async loadData () {
      bus.$emit('loading')
      const { data } = await axios.get('/chamados/tickets/dashboard/')
      bus.$emit('loading')
      this.resumo = data.totais
      this.status = data.status
      this.atendente = data.totais_atendente
    }
  },
  created () {
    this.loadData()
  }

}
</script>

<style scoped>

</style>
