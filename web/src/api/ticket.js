import Model from '@/services/model'
import Clientes from '@/api/cliente'
import Atendentes from '@/api/atendente'
import Prioridades from '@/api/prioridade'
import Niveis from '@/api/niveis'
import Status from '@/api/status'
import Departamentos from '@/api/departamento'
import store from '@/store'

const colunas = [
  {
    dataField: 'id',
    dataType: 'number',
    caption: '#'
  },
  {
    dataField: 'cliente_display',
    caption: 'Cliente'
  },
  {
    dataField: 'cliente',
    dataType: 'number',
    lookup: {
      dataSource: Clientes.makeLookup(),
      displayExpr: 'nome',
      valueExpr: 'id'
    },
    async setCellValue (rowData, value) {
      rowData.cliente = value
      const { versao = '' } = await Clientes.find(value)
      rowData.versao = versao
    },
    visible: false
  },
  {
    dataField: 'titulo',
    dataType: 'string',
    width: 'auto',
    visible: false
  },
  {
    dataField: 'telefone_cliente',
    dataType: 'string',
    caption: 'Telefone',
    visible: false
  },
  {
    dataField: 'inicio',
    dataType: 'datetime'
  },
  {
    dataField: 'termino',
    dataType: 'datetime',
    visible: false
  },
  {
    dataField: 'prioridade',
    dataType: 'string',
    lookup: {
      dataSource: Prioridades.makeLookup(),
      displayExpr: 'descricao',
      valueExpr: 'id'
    },
    visible: false
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
    dataField: 'nivel',
    dataType: 'number',
    lookup: {
      dataSource: Niveis.makeLookup(),
      displayExpr: 'descricao',
      valueExpr: 'id'
    }
  },
  {
    dataField: 'descricao',
    dataType: 'string',
    visible: false
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
    dataField: 'arquivos',
    dataType: 'integer',
    visible: false
  },
  {
    dataField: 'versao',
    dataType: 'string',
    visible: false
  }
]

const formulario = {
  colCount: 7,
  items: [
    {
      colSpan: 4,
      dataField: 'cliente',
      validationRules: [
        {
          type: 'required',
          message: 'O cliente é obrigatório'
        }
      ]
    },
    {
      colSpan: 2,
      dataField: 'prioridade',
      validationRules: [
        {
          type: 'required',
          message: 'A prioridade é obrigatória'
        }
      ]
    },
    {
      colSpan: 1,
      dataField: 'versao',
      validationRules: [
        {
          type: 'required',
          message: 'A versão é obrigatória'
        }
      ]
    },
    {
      colSpan: 7,
      dataField: 'titulo',
      validationRules: [
        {
          type: 'required',
          message: 'O titulo é obrigatório'
        }
      ]
    },
    {
      colSpan: 7,
      dataField: 'descricao',
      validationRules: [
        {
          type: 'required',
          message: 'A descrição é obrigatória'
        }
      ],
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
      dataField: 'arquivos'
    }
  ]
}

export default new Model('chamados/tickets/', colunas, formulario)
