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
      state.currentTopic = data[data.length - 1].topic
    },
    setCurrentTopic (state, data) {
      state.currentTopic = data
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
