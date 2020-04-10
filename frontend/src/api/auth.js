export const login = params => axios.post('/auth/login', params)
export const logout = () => axios.get('/auth/logout')
export const register = params => axios.post('/auth/register', params)
