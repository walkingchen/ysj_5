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
export const getTopicContent = (room_id, topic) => axios.get('/post/system_post', {
  params: {
    room_id,
    topic
  }
})
export const getDailyPoll = (room_id, topic) => axios.get('/post/daily_poll', {
  params: {
    room_id,
    topic
  }
})
export const importPrivateMessage = (params, config) => axios.post('/post/import_private_messages_pool', params, config)
export const importPrivateMessagePictures = (params, config) => axios.post('/post/photo/import_private_messages_pool_pics', params, config)
export const importPrivateMessageAssign = (params, config) => axios.post('/post/photo/import_private_messages_assign', params, config)
export const importSystemMessage = (params, config) => axios.post('/post/import_system_message_pool', params, config)
export const importSystemMessagePictures = (params, config) => axios.post('/post/photo/import_system_messages_pool_pics', params, config)
export const importSystemMessageAssign = (params, config) => axios.post('/post/photo/import_system_message_assign', params, config)
export const importDailyPictures = (params, config) => axios.post('/post/photo/import_daily_poll_pool_pics', params, config)
export const importDailyAssign = (params, config) => axios.post('/post/photo/import_daily_poll_assign', params, config)
