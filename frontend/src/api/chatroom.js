import axios from 'axios'

export const chatLogin = params => {
  return axios.post('/api/auth/login', params).then(res => res.data)
}

export const getRoomInf = id => {
  return axios.get(`/api/room/${id}`).then(res => res.data)
}

export const getPubTimeLine = params => {
  return axios.get('/api/post', { params }).then(res => res.data)
}
