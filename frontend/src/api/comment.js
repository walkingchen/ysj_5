import axios from 'axios'

export const addComment = params => axios.post('/post/comment', params)
export const likeComment = params => axios.post('/post/comment/like', params)
export const deleteLike = id => axios.delete('/post/comment/like/' + id)
export const flagComment = params => axios.post('/post/comment/flag', params)
export const deleteFlag = id => axios.delete('/post/comment/flag/' + id)
