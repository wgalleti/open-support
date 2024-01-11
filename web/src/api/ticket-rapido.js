import Model from '@/services/model'
import Cliente from '@/api/cliente'
import Niveis from '@/api/niveis'

const colunas = [
]

const formulario = {
  focusStateEnabled: true,
  hoverStateEnabled: true,
  activeStateEnabled: true,
  scrollingEnabled: true,
  tabIndex: 0,
  labelLocation: 'top',
  showValidationSummary: true,
  showColonAfterLabel: false,
  colCount: 5,
  onFieldDataChanged: async (e) => {
    if (e.dataField === 'cliente') {
      const { versao = '' } = await Cliente.find(e.value)
      e.component.updateData('versao', versao)
    }
  },
  items: [
    {
      colSpan: 3,
      dataField: 'cliente',
      editorType: 'dxSelectBox',
      editorOptions: {
        dataSource: Cliente.makeLookup(),
        displayExpr: 'nome',
        valueExpr: 'id',
        showClearButton: true,
        searchEnabled: true
      },
      validationRules: [
        {
          type: 'required',
          message: 'O cliente é obrigatório'
        }
      ]
    },
    {
      dataField: 'versao',
      label: {
        text: 'Versão'
      }
    },
    {
      dataField: 'nivel',
      label: {
        text: 'Nível'
      },
      editorType: 'dxSelectBox',
      editorOptions: {
        dataSource: Niveis.makeLookup({},false, '', true, true),
        displayExpr: 'descricao',
        valueExpr: 'id',
        showClearButton: true,
        searchEnabled: true
      },
      validationRules: [
        {
          type: 'required',
          message: 'O nível é obrigatório'
        }
      ]
    },
    {
      colSpan: 5,
      dataField: 'descricao',
      label: {
        text: 'Descrição'
      },
      validationRules: [
        {
          type: 'required',
          message: 'A descrição é obrigatória'
        }
      ],
      editorType: 'dxHtmlEditor',
      editorOptions: {
        height: '20vh',
        mediaResizing: {
          enabled: true
        }
      }
    },
    {
      colSpan: 5,
      dataField: 'solucao',
      label: {
        text: 'Solução'
      },
      validationRules: [
        {
          type: 'required',
          message: 'A Solução é obrigatória'
        }
      ],
      editorType: 'dxHtmlEditor',
      editorOptions: {
        height: '20vh',
        mediaResizing: {
          enabled: true
        }
      }
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

export default new Model('chamados/tickets/rapido/', colunas, formulario)
