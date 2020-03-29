import axios from 'axios'

export const getRoomInf = id => {
  return axios.get(`/room/${id}`).then(res => res.data)
}
