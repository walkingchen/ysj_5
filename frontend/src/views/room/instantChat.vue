<template>
  <el-card shadow="never" class="instant-chat-layout" :style="{ right: show ? 0 : '-502px' }">
    <div slot="header" class="clearfix">
      <span>Charts</span>
      <el-button type="text" icon="el-icon-close" class="close-btn" @click="$emit('on-close')" />
    </div>
    <div class="instant-chat-body">
      <ul class="chat-list">
        <li
          v-for="item in chatList"
          :key="item.id"
          :title="item.nickname"
          :class="{ active: currentChatId === item.id }"
          @click="currentChatId = item.id">
          <el-badge :value="item.newCount" :max="99" :hidden="item.newCount === 0">
            <el-avatar :size="40" :src="item.avatar ? item.avatar : ''" shape="square">
              {{ item.avatar ? '' : item.nickname }}
            </el-avatar>
          </el-badge>
          <div class="right">
            <p>{{ item.nickname }}</p>
            <p class="lastMessage">{{ item.messages.length > 1 ? item.messages[item.messages.length - 1].content : '' }}</p>
          </div>
        </li>
      </ul>
      <div class="chat-content">
        <ul ref="messages" class="message-list">
          <li v-for="(item, index) in currentMessages" :key="index" :class="{ self: item.isMe }">
            <el-avatar :size="40" :src="item.avatar ? item.avatar : ''" shape="square">
              {{ item.avatar ? '' : item.nickname }}
            </el-avatar>
            <p>{{ item.content }}</p>
            <span class="time">{{ item.time }}</span>
          </li>
        </ul>
        <textarea v-model="messageContent" @keyup.enter="sendMessage" />
        <div class="send-btn-div">
          <el-button size="mini" class="send-btn" @click="sendMessage">Send</el-button>
        </div>
      </div>
    </div>
  </el-card>
</template>

<script>
import { formatDate } from '@assets/utils.js'

export default {
  props: ['show', 'startChatUser'],
  data() {
    return {
      chatList: [],
      currentChatId: 18,
      messageContent: ''
    }
  },
  computed: {
    user() {
      return this.$store.state.user
    },
    currentMessages() {
      const chat = this.chatList.find(ele => ele.id === this.currentChatId)
      return chat ? chat.messages.map(item => {
        const _item = {
          isMe: item.from === this.user.id,
          avatar: item.from === this.user.id ? chat.avatar : this.user.avatar,
          nickname: item.from === this.user.id ? chat.nickname : this.user.nickname
        }
        Object.assign(_item, item)
        _item.time = formatDate(item.time)
        return _item
      }) : []
    },
    currentChatAvatar() {
      const chat = this.chatList.find(ele => ele.id === this.currentChatId)
      return chat ? chat.avatar : null
    }
  },
  methods: {
    sendMessage() {
      if (this.messageContent) {
        this.$emit('send-chat-message', {
          to: this.currentChatId,
          content: this.messageContent
        })
        this.addMessage(this.currentChatId, this.user.id, this.messageContent, new Date())
        this.messageContent = ''
      }
    },
    addMessage(id, from, content, time) {
      const chat = this.chatList.find(ele => ele.id === id)
      chat.messages.push({ from, content, time })
      if (id !== this.currentChatId) {
        chat.newCount++
      }
    }
  },
  watch: {
    startChatUser(val) {
      const index = this.chatList.findIndex(ele => ele.id === val.id)
      if (index === -1) {
        const chat = {
          messages: [],
          newCount: 0
        }
        Object.assign(chat, val)
        this.chatList.push(chat)
      }
      this.currentChatId = val.id
    },
    currentMessages() {
      this.$refs.messages.scrollTop = this.$refs.messages.scrollHeight
    },
    currentChatId(val) {
      this.chatList.find(ele => ele.id === val).newCount = 0
    }
  }
}
</script>

<style lang="stylus" scoped>
.instant-chat
  &-layout
    position fixed
    bottom 0
    width 500px
    height 400px
    animation right .3s

    .close-btn
      float right
      padding 3px 0

  &-body
    height 342px
    display flex

    .chat-list
      width 150px
      height 100%
      border-right 1px solid #ebeef5
      overflow auto

      &::-webkit-scrollbar
        width 0

      li
        display flex
        padding 10px
        cursor default

        &.active
          background-color #f2f2f2

        .right
          flex 1
          padding-left 5px
          overflow hidden

          .lastMessage
            color #999
            font-size 14px

    .chat-content
      flex 1
      height 100%
      display flex
      flex-direction column

      .message-list
        flex 1
        border-bottom 1px solid #ebeef5
        overflow auto

        &::-webkit-scrollbar
          width 0

        li
          display flex
          position relative
          padding 5px 8px 16px 8px

          p
            margin-left 8px
            flex 1

          .time
            position absolute
            color #999
            bottom 0
            left 55px
            font-size 12px
            display none

          &:hover .time
            display block

          &.self
            flex-direction row-reverse

            p
              margin-left 0
              margin-right 8px
              text-align right

            .time
              left auto
              right 55px

      textarea
        height 65px
        resize none
        border 0
        outline none
        padding 5px

        &::-webkit-scrollbar
          width 0

      .send-btn-div
        height 28px
        padding 0 10px 5px 0

      .send-btn
        float right
</style>
