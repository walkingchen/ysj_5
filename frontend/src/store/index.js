import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    userid: null,
    room_members: []
  },
  mutations: {
    setRoomMembers(state, data) {
      state.userid = data[0].id
      state.room_members = data
    }
  },
  actions: {
  },
  modules: {
  }
})
