import Model from '@/services/model'
import OSStatus from '@/api/ordem-servico-status'
import Cliente from '@/api/cliente'

const colunas = [
  {
    dataField: 'id',
    dataType: 'number',
    caption: '#'
  },
  {
    dataField: 'data',
    dataType: 'date'
  },
  {
    dataField: 'status',
    dataType: 'number',
    lookup: {
      dataSource: OSStatus.makeLookup({},false, '', true, true),
      displayExpr: 'descricao',
      valueExpr: 'id'
    }
  },
  {
    dataField: 'cliente',
    lookup: {
      dataSource: Cliente.makeLookup(),
      displayExpr: 'nome',
      valueExpr: 'id'
    }
  },
  {
    dataField: 'descricao',
    caption: 'Descrição'
  },
  {
    dataField: 'observacoes',
    caption: 'Observações',
    visible: false
  },
  {
    dataField: 'valor_previsto',
    caption: 'Previsto',
    dataType: 'number',
    format: {
      type: 'fixedPoint',
      precision: 2
    }
  },
  {
    dataField: 'desconto',
    dataType: 'number',
    format: {
      type: 'fixedPoint',
      precision: 2
    }
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
  colCount: 6,
  items: [
    {
      colSpan: 1,
      dataField: 'status'
    },
    {
      colSpan: 1,
      dataField: 'data',
      editorType: 'dxDateBox',
      editorOptions: {
        dateSerializationFormat: 'yyyy-MM-dd'
      },
      validationRules: [
        {
          type: 'required',
          message: 'A data é obrigatório'
        }
      ]
    },
    {
      colSpan: 3,
      dataField: 'cliente',
      validationRules: [
        {
          type: 'required',
          message: 'O cliente é obrigatório'
        }
      ]
    },
    {
      colSpan: 1,
      dataField: 'desconto',
    },
    {
      colSpan: 6,
      dataField: 'descricao',
      caption: 'Descrição',
      editorType: 'dxTextArea',
      editorOptions: {
        height: 200
      },
      validationRules: [
        {
          type: 'required',
          message: 'A descrição é obrigatória'
        }
      ]
    },
    {
      colSpan: 6,
      dataField: 'observacoes',
      caption: 'Observações',
      editorType: 'dxTextArea',
      editorOptions: {
        height: 200
      },
      validationRules: [
        {
          type: 'required',
          message: 'A observação é obrigatória'
        }
      ]
    }
  ]
}

export default new Model('servicos/ordens/', colunas, formulario)
