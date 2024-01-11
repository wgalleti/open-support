import Model from '@/services/model'
import Usuarios from '@/api/usuario'
import Niveis from '@/api/niveis'

const colunas = [
  {
    dataField: 'id',
    dataType: 'number',
    caption: '#'
  },
  {
    dataField: 'nome',
    dataType: 'string'
  },
  {
    dataField: 'email',
    dataType: 'string'
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
    dataField: 'ativo',
    dataType: 'boolean'
  },
  {
    dataField: 'usuario_acesso',
    dataType: 'number',
    lookup: {
      dataSource: Usuarios.makeLookup({}, false, '', true),
      displayExpr: 'username',
      valueExpr: 'id'
    }
  }
]

const formulario = {
  colCount: 3,
  items: [
    {
      dataField: 'nome',
      colSpan: 1,
      validationRules: [
        {
          type: 'required',
          message: 'O nome é obrigatório'
        }
      ]
    },
    {
      dataField: 'email',
      colSpan: 2,
      validationRules: [
        {
          type: 'required',
          message: 'O email é obrigatório'
        }
      ]
    },
    {
      dataField: 'nivel',
      colSpan: 2,
      validationRules: [
        {
          type: 'required',
          message: 'O nível é obrigatório '
        }
      ]
    },
    {
      dataField: 'ativo'
    }
  ]
}

export default new Model('core/atendentes/', colunas, formulario)
