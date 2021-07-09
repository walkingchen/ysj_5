import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    user: {},
    friends: [],
    topic: [],
    currentTopic: null
  },
  mutations: {
    setUser(state, data) {
      state.user = data
    },
    setFriends(state, data) {
      state.friends = data
    },
    setTopic (state, data) {
      state.topic = data
      state.currentTopic = data[data.length - 1]
    },
    setCurrentTopic (state, data) {
      state.currentTopic = data
    }
  },
  actions: {
  },
  modules: {
  }
})
