
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
  },
  {
    dataField: 'valor',
    dataType: 'number',
    format: {
      type: 'fixedPoint',
      precision: 2
    }
  }
]

const formulario = {
  colCount: 4,
  items: [
    {
      colSpan: 3,
      dataField: 'descricao'
    },
    {
      dataField: 'valor'
    }
  ]
}

export default new Model('servicos/tipos/', colunas, formulario)
