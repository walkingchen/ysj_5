<template>
    <el-dialog
    title="Submit a Report"
    :visible="dialogVisible"
    :show-close="false"
    @close="handleClose"
    custom-class="flag-content"
    width="30%">
    <div class="main-content">
        <div style="margin-bottom: 10px;">
            Thanks for looking out for yourself and your friends by reporting things that break the rules. Let us know what's happening.and we'll look into it.
        </div>
        <div>
            <el-tag v-for="(item, key) in flagList" :key="key" style="margin-right: 10px; cursor: pointer;" @click="handleSelect(item)" :type="getIsSelect(item)">
                {{ item }}
            </el-tag>
        </div>
    </div>
    <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false" size="small">Cancel</el-button>
        <el-button type="primary" @click="handleSubmit" size="small">OK</el-button>
    </span>
    </el-dialog>
</template>

<script>
  export default {
    props: ['selectItem'],
    data() {
      return {
        dialogVisible: false,
        flagList: ['hate harassment', 'misinformation', 'other'],
        selectFlagList: []
      };
    },
    methods: {
        getIsSelect (item) {
            if (this.selectFlagList.includes(item)) {
                return ''
            } else {
                return 'info'
            }
        },
        handleSelect (item) {
            if (this.selectFlagList.includes(item)) {
                let index = this.selectFlagList.indexOf(item)
                this.selectFlagList.splice(index, 1)
            } else {
                this.selectFlagList.push(item)
            }
        },
        handleClose () {
            this.selectFlagList = []
        },
        handleSubmit () {
            this.dialogVisible = false
            this.selectFlagList = []
            this.$emit('handleSubmit', this.selectItem)
        }
    }
  };
</script>

<style lang="stylus" scoped>
>>>.flag-content
    .el-dialog__body 
        padding 10px 20px
</style>