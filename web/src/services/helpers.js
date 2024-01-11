/**
 * Apply default set on store
 * @param property
 * @param save
 * @returns {function(*, *): *}
 */
const set = (property, save = false) => (state, payload) => {
  state[property] = payload
  if (localStorage) {
    localStorage.setItem(property, payload)
  }
}

const dataHoje = () => {
  const nowDate = new Date()
  return new Date(nowDate.getTime() - (nowDate.getTimezoneOffset() * 60000)).toISOString().split('T')[0]
}

export {
  set,
  dataHoje
}
