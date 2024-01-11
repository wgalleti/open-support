import Model from '@/services/model'

const colunas = [

]

const formulario = {
  colCount: 1,
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
      dataField: 'motivo_cancelamento',
      editorType: 'dxTextArea',
      editorOptions: {
        height: 400
      },
      validationRules: [
        {
          type: 'required',
          message: 'O motivo é obrigatório'
        }
      ]
    },
    {
      itemType: 'button',
      horizontalAlignment: 'right',
      buttonOptions: {
        text: 'Salvar',
        useSubmitBehavior: true
      }
    }
  ]
}

export default new Model('servicos/ordens/', colunas, formulario)
