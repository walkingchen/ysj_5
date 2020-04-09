export const login = data => {
  return axios.post('/user/login', data)
}

export const getInfo = token => {
  return axios.get('/user/info', { params: { token } })
}

export const logout = () => {
  return axios.post('/user/logout')
}

// 用户注册
export const uesrRegister = data => {
  return axios.post('/register', data).then(res => res.data)
}

// 用户列表
export const getUserList = params => {
  return axios.get('/api/v1/users', { params: params }).then(res => res.data)
}
