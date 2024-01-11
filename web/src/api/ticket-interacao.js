import Model from '@/services/model'
import Atendentes from '@/api/atendente'
import Status from '@/api/status'
import Departamentos from '@/api/departamento'
import Tickets from '@/api/ticket'
import axios from '@/plugins/axios'
import store from '@/store'

let fileUploaded
let formInstance

const colunas = [
  {
    dataField: 'id',
    dataType: 'number',
    caption: '#'
  },
  {
    dataField: 'ticket',
    dataType: 'number',
    lookup: {
      dataSource: Tickets.makeLookup(),
      displayExpr: 'id',
      valueExpr: 'id'
    }
  },
  {
    dataField: 'atendente',
    dataType: 'number',
    lookup: {
      dataSource: Atendentes.makeLookup(),
      displayExpr: 'nome',
      valueExpr: 'id'
    }
  },
  {
    dataField: 'data',
    dataType: 'datetime'
  },
  {
    dataField: 'descricao',
    dataType: 'string',
    visible: false
  },
  {
    dataField: 'interno',
    dataType: 'boolean'
  },
  {
    dataField: 'status',
    dataType: 'string',
    lookup: {
      dataSource: Status.makeLookup(),
      displayExpr: 'descricao',
      valueExpr: 'id'
    }
  },
  {
    dataField: 'departamento',
    dataType: 'string',
    lookup: {
      dataSource: Departamentos.makeLookup(),
      displayExpr: 'descricao',
      valueExpr: 'id'
    }
  },
  {
    dataField: 'arquivo',
    dataType: 'number',
    visible: false
  }
]

const formulario = {
  onContentReady: e => {
    formInstance = e.component
    fileUploaded = []
  },
  colCount: 10,
  labelLocation: 'top',
  height: 'auto',
  items: [
    {
      colSpan: 3,
      dataField: 'atendente',
      editorType: 'dxSelectBox',
      editorOptions: {
        dataSource: Atendentes.makeLookup(),
        displayExpr: 'nome',
        valueExpr: 'id',
        showClearButton: true,
        searchEnabled: true
      },
      visible: !store.state.auth.user.is_cliente,
      validationRules: [
        {
          type: 'required',
          message: 'O atendente é obrigatório'
        }
      ]
    },
    {
      colSpan: 3,
      dataField: 'status',
      editorType: 'dxSelectBox',
      editorOptions: {
        dataSource: Status.makeLookup(),
        displayExpr: 'descricao',
        valueExpr: 'id',
        showClearButton: true,
        searchEnabled: true
      },
      visible: !store.state.auth.user.is_cliente,
      validationRules: [
        {
          type: 'required',
          message: 'O status é obrigatório'
        }
      ]
    },
    {
      colSpan: 3,
      dataField: 'departamento',
      editorType: 'dxSelectBox',
      editorOptions: {
        dataSource: Departamentos.makeLookup(),
        displayExpr: 'descricao',
        valueExpr: 'id',
        showClearButton: true,
        searchEnabled: true
      },
      visible: !store.state.auth.user.is_cliente,
      validationRules: [
        {
          type: 'required',
          message: 'O departamento é obrigatório'
        }
      ]
    },
    {
      dataField: 'interno',
      editorType: 'dxCheckBox',
      visible: !store.state.auth.user.is_cliente
    },
    {
      colSpan: 10,
      validationRules: [
        {
          type: 'required',
          message: 'A descrição é obrigatória'
        }
      ],
      dataField: 'descricao',
      editorType: 'dxHtmlEditor',
      editorOptions: {
        height: '30vh',
        mediaResizing: {
          enabled: true
        }
      }
    },
    {
      colSpan: 7,
      dataField: 'arquivo',
      editorType: 'dxFileUploader',
      editorOptions: {
        multiple: true,
        files: [],
        accept: '*',
        value: [],
        uploadMode: 'instantly',
        maxFileSize: '1e+8',
        allowedFileExtensions: [
          '.jpg',
          '.jpeg',
          '.gif',
          '.png',
          '.xls',
          '.xlsx',
          '.doc',
          '.docx',
          '.pdf',
          '.rar',
          '.zip',
          '.7z',
          '.sql',
          '.mp4',
          '.xml'
        ],
        uploadFile: function (file, progressCallback) {
          const item = new FormData()

          item.append('arquivo', file)
          item.append('usuario', store.state.auth.user.id)

          progressCallback(100)

          return axios.post(
            '/chamados/anexos/',
            item,
            {
              headers: {
                'content-type': 'multipart/form-data'
              }
            }
          ).then(
            res => {
              progressCallback(200)
              fileUploaded.push(res.data.id)
              formInstance.updateData('arquivos', fileUploaded)
              return fileUploaded
            }
          )
        }
      }
    },
    {
      colSpan: 3,
      itemType: 'button',
      horizontalAlignment: 'right',
      buttonOptions: {
        text: 'Salvar',
        useSubmitBehavior: true
      }
    }
  ]
}

export default new Model('chamados/ticketsinteracoes/', colunas, formulario)
