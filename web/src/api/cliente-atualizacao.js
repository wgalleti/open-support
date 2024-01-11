import Model from '@/services/model'
import Cliente from '@/api/cliente'

const colunas = [
  {
    dataField: 'id',
    dataType: 'number',
    caption: '#'
  },
  {
    dataField: 'cliente',
    dataType: 'number',
    lookup: {
      dataSource: Cliente.makeLookup(),
      displayExpr: 'username',
      valueExpr: 'id'
    }
  },
  {
    dataField: 'data',
    dataType: 'date'
  },
  {
    dataField: 'versao',
    dataType: 'string'
  },
  {
    dataField: 'observacao',
    dataType: 'string'
  }
]

const formulario = {
  colCount: 5,
  items: [
    {
      dataField: 'cliente',
      editorType: 'dxSelectBox',
      editorOptions: {
        dataSource: Cliente.makeLookup(),
        displayExpr: 'nome',
        valueExpr: 'id',
        showClearButton: true,
        searchEnabled: true
      },
      colSpan: 3,
      validationRules: [
        {
          type: 'required',
          message: 'O cliente é obrigatório'
        }
      ]
    },
    {
      dataField: 'versao',
      dataType: 'string',
      colSpan: 2,
      validationRules: [
        {
          type: 'required',
          message: 'A versão é obrigatória'
        }
      ]
    },
    {
      dataField: 'observacao',
      dataType: 'string',
      editorOptions: {
        height: '200'
      },
      colSpan: 5
    },
    {
      colSpan: 5,
      itemType: 'button',
      horizontalAlignment: 'right',
      buttonOptions: {
        text: 'Salvar',
        useSubmitBehavior: true
      }
    }
  ]
}

export default new Model('core/clientesatualizacoes/', colunas, formulario)
