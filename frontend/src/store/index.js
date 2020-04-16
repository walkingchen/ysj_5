import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    user: {},
    room_members: []
  },
  mutations: {
    setRoomMembers(state, data) {
      state.user = data[0]
      state.room_members = data
    }
  },
  actions: {
  },
  modules: {
  }
})
