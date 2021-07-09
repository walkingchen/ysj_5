export const getPosts = params => axios.get('/post', { params })
export const createPost = params => axios.post('/post', params)
export const getPost = id => axios.get('/post/' + id)
export const likePost = params => axios.post('/post/like', params)
export const deleteLike = id => axios.delete('/post/like/' + id)
export const changeLike = (id, params) => axios.put('/post/like/' + id, params)
export const commentPost = params => axios.post('/post/comment', params)
export const deleteComment = id => axios.delete('/post/comment/' + id)
export const checkPost = params => axios.post('/post/factcheck', params)
export const deleteCheck = id => axios.delete('/post/factcheck/' + id)
export const flagPost = post_id => axios.post('/post/flag', { post_id })
export const deleteFlag = id => axios.delete('/post/flag/' + id)
export const postPhoto = params => axios.post('/post/photo', params)
export const getTopic = rid => axios.get('/post/topic?room_id=' + rid)
export const getTopicContent = (room_id, topic) => axios.get('/post/daily', {
  params: {
    room_id,
    topic
  }
})
