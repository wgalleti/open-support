import Model from '@/services/model'

const colunas = [
  {
    dataField: 'id',
    dataType: 'number',
    caption: '#'
  },
  {
    dataField: 'descricao',
    dataType: 'string'
  }
]

const formulario = {

}

export default new Model('servicos/ordens/status/', colunas, formulario)
