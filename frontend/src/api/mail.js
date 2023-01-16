import axios from 'axios'

export const getMails = () => axios.get('/mail')
export const deleteMail = id => axios.delete('/mail/' + id)
export const createMail = params => axios.post('/mail', params)
export const editMail = (id, params) => axios.put('/mail/' + id, params)
