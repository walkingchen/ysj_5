export const getPosts = params => axios.get('/post', { params })
export const createPost = params => axios.post('/post', params)
export const getPost = id => axios.get('/post/' + id)
export const likePost = params => axios.post('/post/like', params)
export const deleteLike = id => axios.delete('/post/like/' + id)
export const changeLike = (id, params) => axios.put('/post/like/' + id, params)
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
export const importPrivate = (params, config) => axios.post('/post/import_private_messages', params, config)
export const importAssignFile = (params, config) => axios.post('/post/import_members_with_messages', params, config)
