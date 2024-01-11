import Model from '@/services/model'
import Usuarios from '@/api/usuario'
// import axios from '@/plugins/axios'

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
    dataField: 'contato',
    dataType: 'string'
  },
  {
    dataField: 'contato_telefone',
    dataType: 'string'
  },
  {
    dataField: 'ativo',
    dataType: 'boolean'
  },
  {
    dataField: 'codigo_cliente',
    dataType: 'number'
  },
  {
    dataField: 'versao',
    dataType: 'string'
  },
  {
    dataField: 'usuario_acesso',
    dataType: 'number',
    lookup: {
      dataSource: Usuarios.makeLookup(),
      displayExpr: 'username',
      valueExpr: 'id'
    }
  }
]

const formulario = {
  colCount: 3,
  items: [
    {
      dataField: 'codigo_cliente',
      colSpan: 1,
      validationRules: [
        {
          type: 'required',
          message: 'O código do cliente é obrigatório'
        }
      ]
    },
    {
      dataField: 'nome',
      colSpan: 2,
      validationRules: [
        {
          type: 'required',
          message: 'O nome é obrigatório'
        }
      ]
    },
    {
      dataField: 'email',
      colSpan: 3,
      validationRules: [
        {
          type: 'required',
          message: 'O Email é obrigatório'
        }
        // {
        //   type: 'async',
        //   message: 'Email já está cadastrado',
        //   reevaluate: false,
        //   validationCallback (params) {
        //     console.log(params)
        //     return new Promise((resolve, reject) => {
        //       axios.get('core/clientes/existe/', { params: { email: params.value } }).then(
        //         () => resolve()
        //       ).catch(
        //         err => reject(err.data)
        //       )
        //     })
        //   }
        // }
      ]
    },
    {
      dataField: 'contato'
    },
    {
      dataField: 'contato_telefone'
    },
    {
      dataField: 'ativo'
    }

  ]
}

export default new Model('core/clientes/', colunas, formulario)
