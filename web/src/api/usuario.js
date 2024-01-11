import Model from '@/services/model'

const colunas = [
  {
    dataField: 'id',
    dataType: 'number',
    caption: '#'
  },
  {
    dataField: 'username',
    dataType: 'string'
  },
  {
    dataField: 'first_name',
    dataType: 'string'
  },
  {
    dataField: 'last_name',
    dataType: 'string'
  }
]

const formulario = {

}

export default new Model('core/users/', colunas, formulario)
