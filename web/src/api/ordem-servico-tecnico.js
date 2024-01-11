import Model from '@/services/model'
import OSTipos from '@/api/ordem-servico-tipo'
import Atendentes from '@/api/atendente'

const colunas = [
  {
    dataField: 'ordem_servico',
    dataType: 'number',
    visible: false
  },
  {
    dataField: 'tipo',
    dataType: 'number',
    lookup: {
      dataSource: OSTipos.makeLookup(),
      displayExpr: 'descricao',
      valueExpr: 'id'
    },
    async setCellValue (rowData, value) {
      rowData.tipo = value
      const { valor = 0 } = await OSTipos.find(value)
      rowData.valor = valor
    }
  },
  {
    dataField: 'tecnico',
    dataType: 'number',
    lookup: {
      dataSource: Atendentes.makeLookup(),
      displayExpr: 'nome',
      valueExpr: 'id'
    }
  },
  {
    dataField: 'tempo',
    dataType: 'number',
    setCellValue (rowData, value, oldValue) {
      const { valor } = oldValue
      rowData.tempo = value
      rowData.valor = value * valor
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
    { dataField: 'tipo' },
    {
      dataField: 'tecnico',
      colSpan: 3,
      validationRules: [
        {
          type: 'required',
          message: 'O tecnico é obrigatório'
        }
      ]
    },
    {
      dataField: 'tempo',
      colSpan: 1,
      editorType: 'dxNumberBox',
      editorOptions: {
        format: {
          type: 'fixedPoint',
          precision: 2
        }
      },
      validationRules: [
        {
          type: 'required',
          message: 'O tempo é obrigatório'
        }
      ]
    },
    {
      dataField: 'valor',
      editorType: 'dxNumberBox',
      editorOptions: {
        format: {
          type: 'fixedPoint',
          precision: 2
        }
      },
      validationRules: [
        {
          type: 'required',
          message: 'O valor é obrigatório'
        }
      ]
    }
  ]
}

export default new Model('servicos/tecnicos/', colunas, formulario)
