import axios from 'axios'
// import { relative } from 'path'
// import request from '@/utils/request'

// 创建聊天室
export const createChatRoom = data => {
  return axios.post('/api/v1/rooms', data).then(res => res.data)
}

// 获取聊天室列表
export const getChatRoomList = () => {
  return axios.get('/api/v1/rooms').then(res => res.data)
}
