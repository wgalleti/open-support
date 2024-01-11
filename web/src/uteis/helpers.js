const dataHoje = () => {
  const nowDate = new Date()
  return new Date(nowDate.getTime() - (nowDate.getTimezoneOffset() * 60000)).toISOString().split('T')[0]
}

export {
  dataHoje
}
