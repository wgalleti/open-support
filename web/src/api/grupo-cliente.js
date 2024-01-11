import Model from '@/services/model'

const colunas = [
  {
    dataField: 'id',
    dataType: 'number',
    caption: '#'
  },
  {
    dataField: 'nome',
    dataType: 'string'
  },
  {
    dataField: 'quantidade',
    dataType: 'number',
    format: {
      type: 'fixedPoint'
    }
  }
]

const formulario = {
  colCount: 1,
  items: [
    {
      colSpan: 1,
      dataField: 'nome',
      validationRules: [
        {
          type: 'required',
          message: 'O nome é obrigatório'
        }
      ]
    }
  ]
}

export default new Model('core/grupos/', colunas, formulario)
