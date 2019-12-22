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

// 修改聊天室信息
export const editChatRoom = data => {
  return axios.put(`/api/v1/rooms/${data.id}`, data).then(res => res.data)
}

// 删除聊天室信息
export const delChatRoom = data => {
  return axios.delete(`/api/v1/rooms/${data.id}`, data).then(res => res.data)
}

// 新增聊天室原型
export const addPrototype = data => {
  return axios.post('/api/v1/room_prototypes', data).then(res => res.data)
}

// 获取聊天室原型列表
export const getPrototypeList = () => {
  return axios.get('/api/v1/room_prototypes').then(res => res.data)
}

// 删除聊天室原型
export const delPrototypeDetail = id => {
  return axios.delete(`/api/v1/room_prototypes/${id}`).then(res => res.data)
}

