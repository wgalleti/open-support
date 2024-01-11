import Model from '@/services/model'

const colunas = [
  {
    dataField: 'id',
    dataType: 'number',
    caption: '#'
  },
  {
    dataField: 'descricao',
    caption: 'Descrição',
    dataType: 'string'
  },
  {
    dataField: 'codigo_erp',
    caption: 'Código ERP',
    dataType: 'string'
  }
]

const formulario = {
  colCount: 3,
  items: [
    {
      dataField: 'descricao',
      colSpan: 2,
      validationRules: [
        {
          type: 'required',
          message: 'A descrição é obrigatória'
        }
      ]
    },
    {
      dataField: 'codigo_erp',
      colSpan: 1,
      validationRules: [
        {
          type: 'required',
          message: 'O código do ERP é obrigatório'
        }
      ]
    }
  ]
}

export default new Model('servicos/servicos/', colunas, formulario)
