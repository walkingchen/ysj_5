import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    sid: '',
    user: {},
    friends: [],
    topics: [],
    currentTopic: null,
    searchKey: '',
    getPostDetailLoading: false,
    postDetailData: {}
  },
  mutations: {
    setSid (state, data) {
      state.sid = data
    },
    setUser (state, data) {
      state.user = data
    },
    setFriends (state, data) {
      state.friends = data
    },
    setTopic (state, data) {
      state.topics = data

      const localTopic = Number(localStorage.getItem('currentTopic'))
      if (localTopic && data.findIndex(ele => ele.topic === localTopic) > -1) {
        state.currentTopic = localTopic
      } else {
        state.currentTopic = data[data.length - 1].topic
      }
      localStorage.setItem('currentTopic', state.currentTopic)
    },
    setCurrentTopic (state, data) {
      state.currentTopic = data
      localStorage.setItem('currentTopic', data)
    },
    setSearchKey (state, data) {
      state.searchKey = data
    },
    setGetPostDetailLoading (state, value) {
      state.getPostDetailLoading = value
    },
    setPostDetail (state, data) {
      state.postDetailData = data
    }
  },
  actions: {
  },
  modules: {
  }
})
