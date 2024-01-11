import Model from '@/services/model'
import Servico from '@/api/servico'

const colunas = [
  {
    dataField: 'ordem_servico',
    dataType: 'number',
    visible: false
  },
  {
    dataField: 'servico',
    dataType: 'number',
    lookup: {
      dataSource: Servico.makeLookup(),
      displayExpr: 'descricao',
      valueExpr: 'id'
    }
  },
  {
    dataField: 'valor',
    dataType: 'number',
    format: {
      type: 'fixedPoint',
      precision: 2
    }
  },
  {
    dataField: 'tempo',
    dataType: 'number'
  },
  {
    dataField: 'descricao',
    dataType: 'string'
  }
]

const formulario = {
  colCount: 4,
  labelLocation: 'top',
  focusStateEnabled: true,
  hoverStateEnabled: true,
  activeStateEnabled: true,
  scrollingEnabled: true,
  tabIndex: 0,
  showValidationSummary: true,
  showColonAfterLabel: false,
  items: [
    {
      colSpan: 3,
      dataField: 'servico',
      editorType: 'dxSelectBox',
      editorOptions: {
        dataSource: Servico.makeLookup(),
        displayExpr: 'descricao',
        valueExpr: 'id',
        showClearButton: true,
        searchEnabled: true
      },
      validationRules: [
        {
          type: 'required',
          message: 'O serviço é obrigatório'
        }
      ]
    },
    {
      dataField: 'gerar_integracao',
      editorType: 'dxCheckBox'
    },
    {
      dataField: 'data_encerramento',
      label: {
        text: 'Data'
      },
      editorType: 'dxDateBox',
      validationRules: [
        {
          type: 'required',
          message: 'A data do encerramento é obrigatória'
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
    },
    {
      dataField: 'desconto',
      editorType: 'dxNumberBox',
      editorOptions: {
        format: {
          type: 'fixedPoint',
          precision: 2
        }
      }
    },
    {
      dataField: 'tempo',
      editorType: 'dxNumberBox',
      editorOptions: {
        format: {
          type: 'fixedPoint',
          precision: 0
        }
      }
    },
    {
      colSpan: 4,
      dataField: 'descricao',
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
      colSpan: 4,
      itemType: 'button',
      horizontalAlignment: 'right',
      buttonOptions: {
        text: 'Salvar',
        useSubmitBehavior: true
      }
    }
  ]
}

export default new Model('servicos/tecnicos/', colunas, formulario)
