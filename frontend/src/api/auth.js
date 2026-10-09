import axios from 'axios'

export const login = params => axios.post('/auth/login', params)
export const logout = () => axios.get('/auth/logout')
export const register = params => axios.post('/auth/register', params)
export const requestPasswordReset = email => axios.post('/auth/password-reset/request', { email })
export const confirmPasswordReset = (token, password) => axios.post('/auth/password-reset/confirm', { token, password })
