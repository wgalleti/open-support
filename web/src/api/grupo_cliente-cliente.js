import Clientes from '@/api/cliente'

export const colunas = [
  {
    dataField: 'id',
    caption: '#',
    lookup: {
      dataSource: Clientes.makeLookup(),
      displayExpr: 'nome',
      valueExpr: 'id'
    },
    visible: false
  },
  {
    dataField: 'codigo_cliente',
    caption: 'Código'
  },
  {
    dataField: 'nome'
  }
]

export const formulario = {
  colCount: 2,
  focusStateEnabled: true,
  hoverStateEnabled: true,
  activeStateEnabled: true,
  scrollingEnabled: true,
  tabIndex: 0,
  labelLocation: 'top',
  showValidationSummary: true,
  showColonAfterLabel: false,
  items: [
    {
      colSpan: 2,
      dataField: 'id',
      validationRules: [
        {
          type: 'required',
          message: 'O cliente é obrigatório'
        }
      ]
    }
  ]
}
