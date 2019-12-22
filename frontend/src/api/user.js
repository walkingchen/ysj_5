import request from '@/utils/request'
import axios from 'axios'

export function login(data) {
  return request({
    url: '/user/login',
    method: 'post',
    data
  })
}

export function getInfo(token) {
  return request({
    url: '/user/info',
    method: 'get',
    params: { token }
  })
}

export function logout() {
  return request({
    url: '/user/logout',
    method: 'post'
  })
}

// 用户注册
export const uesrRegister = data => {
  return axios.post('/register', data).then(res => res.data)
}
