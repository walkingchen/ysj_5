<template>
  <el-card class="post-create-layout">
    <textarea
      rows="5"
      class="post-create-content"
      placeholder="What's on your mind?"
      v-model="postContent"
    />

    <div v-if="showPostImage" class="img-box" v-loading="postImageLoading">
      <span class="delete-btn" @click="deletePostImage">&times;</span>
      <img v-if="postImageUri" :src="postImageUri" />
    </div>

    <el-button type="text" size="mini" @click="selectFile">
      <v-icon name="images" />
    </el-button>
    <input
      ref="fileInput"
      type="file"
      hidden
      accept="image/*"
      @change="selectedImage"
    />

    <el-button
      class="post-create-btn"
      type="primary"
      size="mini"
      :loading="submitPostLoading"
      @click="submitPost"
    >Post</el-button>
  </el-card>
</template>

<script>
import { mapState } from 'vuex'
import 'vue-awesome/icons/images'
import {
  postPhoto,
  createPost
} from '@api/post'

export default {
  data () {
    return {
      postContent: '',
      showPostImage: false,
      postImageLoading: false,
      postImageUri: '',
      postImageFileName: '',
      submitPostLoading: false
    }
  },
  computed: mapState([
    'sid',
    'currentTopic'
  ]),
  methods: {
    selectFile () {
      this.$refs.fileInput.click()
    },
    selectedImage (e) {
      const file = e.target.files[0]
      const fileExt = file.name.split('.').pop().toLocaleLowerCase()
      if (['png', 'jpg', 'jpeg', 'bmp', 'gif', 'webp', 'psd', 'svg', 'tiff'].includes(fileExt)) {
        this.showPostImage = true
        this.postImageLoading = true

        const fileForm = new FormData()
        fileForm.append('file', file)
        postPhoto(fileForm).then(({ data }) => {
          if (data.result_code === 2000) {
            this.postImageLoading = false
            this.postImageUri = data.data.upload_path + data.data.filename_s
            this.postImageFileName = data.data.filename
          }
        })
      } else {
        this.$message.warning('Please select a image.')
      }

      this.$refs.fileInput.value = ''
    },
    deletePostImage () {
      this.postImageUri = ''
      this.postImageFileName = ''
      this.showPostImage = false
    },
    async submitPost() {
      if (this.postContent) {
        this.submitPostLoading = true

        const params = {
          post_content: this.postContent,
          timeline_type: 0,
          post_type: 1,
          topic: this.currentTopic,
          sid: this.sid,
          room_id: Number(localStorage.getItem('roomid'))
        }
        if (this.postImageFileName) {
          params.photo_uri = this.postImageFileName
        }

        await createPost(params).then(res => {
          this.postContent = ''
          this.$message.success('Post successfully!')
          this.$emit('on-success', res.data.data.id)
        })
        this.submitPostLoading = false
      } else {
        this.$message({
          message: 'Please enter the content.',
          type: 'warning'
        })
      }
    }
  }
}
</script>

<style lang="stylus" scoped>
.post-create-layout
  border 0
  padding 15px 10px 10px
  margin-bottom 20px

  .post-create-content
    width 100%
    border 0
    resize none
    outline none

  .img-box
    width 100px
    height 100px
    display flex
    justify-content center
    align-items center
    border 1px solid #ebeef5
    border-radius 4px
    padding 3px
    position relative

    .delete-btn
      display none
      position absolute
      top -5px
      right -5px
      width 16px
      height 16px
      border-radius 8px
      border 1px solid #eee
      background-color #fff
      line-height 16px
      text-align center
      cursor pointer
      color #777

      &:hover
        color #444

    &:hover .delete-btn
      display block

    img
      max-width 100%
      max-height 100%

  .post-create-btn
    float right
</style>
