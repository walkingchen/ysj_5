<template>
    <el-dialog
    title="Submit a Report"
    :visible="dialogVisible"
    :show-close="false"
    @close="handleClose"
    custom-class="flag-content"
    width="30%">
    <div class="main-content">
        <div style="margin-bottom: 10px; word-break: keep-all;">
            Thanks for looking out for yourself and your friends by reporting things that break the rules. Let us know what's happening.and we'll look into it.
        </div>
        <div>
            <el-tag 
                v-for="(item, key) in flagList" 
                :key="key" 
                style="margin-right: 10px; margin-bottom: 10px; cursor: pointer; border-radius: 20px;" 
                @click="handleSelect(item)" 
                :type="getIsSelect(item)">
                {{ item }}
            </el-tag>
            <div>
                <span>others: </span>
                <el-input
                    size="mini"
                    placeholder=""
                    style="width: 150px;"
                    v-model.trim="othersTag">
                </el-input>
            </div>
            <!-- <el-tag 
                style="margin-right: 10px; margin-bottom: 10px; cursor: pointer; border-radius: 20px;" 
                @click="handleSelect('others')" 
                :type="getIsSelect(othersTag)">
                <el-input
                    size="mini"
                    placeholder="others"
                    class="other-tag"
                    v-model.trim="othersTag">
                </el-input>
            </el-tag> -->
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
        flagList: ['hate', 'hate harassment', 'misinformation'],
        selectFlagList: [],
        othersTag: ''
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
            // 清除以前的自定义tag
            // let list = this.selectFlagList.filter(item => {
            //     return this.flagList.includes(item) || item === this.othersTag
            // })
            // this.selectFlagList = [].concat(list)
            if (item === 'others') {
                // if (this.selectFlagList.includes(this.othersTag)) {
                //     let index = this.selectFlagList.indexOf(this.othersTag)
                //     this.selectFlagList.splice(index, 1)
                // } else {
                //     if (this.othersTag.length === 0) {
                //         this.othersTag = 'others'
                //     }
                //     this.selectFlagList.push(this.othersTag)
                // }
            } else {
                if (this.selectFlagList.includes(item)) {
                    let index = this.selectFlagList.indexOf(item)
                    this.selectFlagList.splice(index, 1)
                } else {
                    this.selectFlagList.push(item)
                }
            }
            
        },
        handleClose () {
            this.selectFlagList = []
            this.othersTag = ''
        },
        handleSubmit () {
            this.dialogVisible = false
            if (this.othersTag.length) {
                this.selectFlagList.push(this.othersTag)
            }
            let params = {
                item: this.selectItem,
                selectTag: this.selectFlagList.join(',')
            }
            this.$emit('handleSubmit', params)
            this.selectFlagList = []
            this.othersTag = ''
        }
    }
  };
</script>

<style lang="stylus" scoped>
>>>.flag-content
    .el-dialog__body 
        padding 10px 20px

.other-tag
    padding 0 10px
    >>>.el-input__inner
        border: 0px;
        padding: 0px;
        background: none;
        width 60px
</style>