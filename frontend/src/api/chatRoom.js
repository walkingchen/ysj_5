import request from '@/utils/request'

// 创建聊天室
export function createChatRoom(data) {
  return request({
    url: 'room',
    method: 'post',
    data
  })
}

// 获取聊天室列表
export function getChatRoomList() {
  return request({
    url: 'room',
    method: 'get'
  })
}
