<template>
  <div>
    <input ref="excel-upload-input" class="excel-upload-input" type="file" accept=".csv" @change="handleClick">
    <div class="drop" @drop="handleDrop" @dragover="handleDragover" @dragenter="handleDragover">
      <p>Drop csv file here</p>
      <div>
        <el-tag
          v-if="fileName !== null"
          type="success"
          closable
          @close="removeFile"
        >
          {{ fileName }}
        </el-tag>
        <el-button v-if="fileName !== null" type="success" size="mini" style="margin-left:15px;" @click="$emit('upload')">Upload</el-button>
        <el-button :loading="loading" size="mini" type="primary" style="margin-left:15px;" @click="handleUpload">Browse</el-button>
        <el-button :loading="loading" size="mini" type="warning" @click="downloadTemplate">Download Template</el-button>
      </div>
    </div>
  </div>
</template>

<script>
import XLSX from 'xlsx'

export default {
  data() {
    return {
      fileName: null,
      prototype_name: '',
      loading: false
    }
  },
  methods: {
    downloadTemplate() {
      const a = document.createElement('a')
      a.href = 'http://ysj_5.soulfar.com/static/prototype_demo.csv'
      a.click()
    },
    generateData(data) {
      this.$emit('on-success', data)
    },
    handleDrop(e) {
      e.stopPropagation()
      e.preventDefault()
      if (!this.loading) {
        const files = e.dataTransfer.files
        if (files.length !== 1) {
          this.$message.error('Only support uploading one file!')
          return
        }
        const rawFile = files[0]

        if (!this.isExcel(rawFile)) {
          this.$message.error('Only supports upload .xlsx, .xls, .csv suffix files.')
          return false
        }
        this.upload(rawFile)
      }
    },
    handleDragover(e) {
      e.stopPropagation()
      e.preventDefault()
      e.dataTransfer.dropEffect = 'copy'
    },
    handleUpload() {
      this.$refs['excel-upload-input'].click()
    },
    handleClick(e) {
      const rawFile = e.target.files[0]
      if (rawFile) {
        this.upload(rawFile)
      }
    },
    upload(rawFile) {
      this.$refs['excel-upload-input'].value = null

      if (rawFile.size < 1024 * 1024) {
        this.readerData(rawFile)
      } else {
        this.$message.warning('Please do not upload files larger than 1M in size.')
      }
    },
    readerData(rawFile) {
      const place = rawFile.name.indexOf('.')
      this.prototype_name = rawFile.name.substring(0, place)
      this.fileName = rawFile.name
      this.loading = true
      return new Promise((resolve, reject) => {
        const reader = new FileReader()
        reader.onload = e => {
          const data = e.target.result
          const workbook = XLSX.read(data, { type: 'array' })
          const firstSheetName = workbook.SheetNames[0]
          const worksheet = workbook.Sheets[firstSheetName]
          const header = this.getHeaderRow(worksheet)
          const results = XLSX.utils.sheet_to_json(worksheet)
          this.generateData({ header, results })
          this.loading = false
          resolve()
        }
        reader.readAsArrayBuffer(rawFile)
      })
    },
    getHeaderRow(sheet) {
      const headers = []
      const range = XLSX.utils.decode_range(sheet['!ref'])
      let C
      const R = range.s.r
      /* start in the first row */
      for (C = range.s.c; C <= range.e.c; ++C) { /* walk every column in the range */
        const cell = sheet[XLSX.utils.encode_cell({ c: C, r: R })]
        /* find the cell in the first row */
        let hdr = 'UNKNOWN ' + C // <-- replace with your desired default
        if (cell && cell.t) hdr = XLSX.utils.format_cell(cell)
        headers.push(hdr)
      }
      return headers
    },
    isExcel(file) {
      return /\.(xlsx|xls|csv)$/.test(file.name)
    },
    removeFile() {
      this.fileName = null
    }
  }
}
</script>

<style lang="stylus" scoped>
.excel-upload-input
  display none
  z-index -9999

.drop
  border 2px dashed #bbb
  height 160px
  margin 0 auto
  font-size 24px
  border-radius 5px
  text-align center
  color #bbb
  display flex
  flex-direction column
  justify-content center

  p
    line-height 45px
</style>
