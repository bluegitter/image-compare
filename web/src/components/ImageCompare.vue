<!-- App.vue -->
<template>
  <div class="container">
    <h1>图片相似度比较</h1>
    <div class="image-upload-container">
      <!-- 左边图片上传 -->
      <div class="upload-box">
        <el-upload
          class="upload-demo"
          drag
          :auto-upload="false"
          :on-change="handleLeftImageUpload"
          :on-remove="handleLeftImageRemove"
          :file-list="leftFileList"
          accept="image/*"
          :limit="1"
        >
          <i class="el-icon-upload"></i>
          <div class="el-upload__text">拖拽至此或<em>点击上传</em>左图,只能上传jpg/png文件</div>
        </el-upload>
        <div class="preview" v-if="leftImage">
          <img :src="leftImage" alt="Left Image">
        </div>
      </div>

      <!-- 右边图片上传 -->
      <div class="upload-box">
        <el-upload
          class="upload-demo"
          drag
          :auto-upload="false"
          :on-change="handleRightImageUpload"
          :on-remove="handleRightImageRemove"
          :file-list="rightFileList"
          accept="image/*"
          :limit="1"
        >
          <i class="el-icon-upload"></i>
          <div class="el-upload__text">拖拽至此或<em>点击上传</em>右图,只能上传jpg/png文件</div>
        </el-upload>
        <div class="preview" v-if="rightImage">
          <img :src="rightImage" alt="Right Image">
        </div>
      </div>
    </div>

    <!-- 相似度结果 -->
    <div class="result-box" v-if="similarity !== null">
      <p>相似度: {{ similarity.toFixed(3) }}</p>
      <p>{{ similarity > 0.3 ? '两张图片相似' : '两张图片不相似' }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      leftImage: null,
      rightImage: null,
      leftFile: null,
      rightFile: null,
      similarity: null,
      leftFileList: [],
      rightFileList: []
    }
  },
  watch: {
    leftFile(newVal) {
      if (newVal && this.rightFile) {
        this.calculateSimilarity()
      }
    },
    rightFile(newVal) {
      if (newVal && this.leftFile) {
        this.calculateSimilarity()
      }
    }
  },
  methods: {
    // 处理左图上传
    handleLeftImageUpload(file) {
      this.leftFile = file.raw
      this.leftFileList = [file]
      const reader = new FileReader()
      reader.onload = (e) => {
        this.leftImage = e.target.result
      }
      reader.readAsDataURL(file.raw)
    },

    // 处理右图上传
    handleRightImageUpload(file) {
      this.rightFile = file.raw
      this.rightFileList = [file]
      const reader = new FileReader()
      reader.onload = (e) => {
        this.rightImage = e.target.result
      }
      reader.readAsDataURL(file.raw)
    },

    // 清除左图
    handleLeftImageRemove() {
      this.leftFile = null
      this.leftImage = null
      this.leftFileList = []
      this.similarity = null
    },

    // 清除右图
    handleRightImageRemove() {
      this.rightFile = null
      this.rightImage = null
      this.rightFileList = []
      this.similarity = null
    },

    // 计算相似度
    async calculateSimilarity() {
      if (!this.leftFile || !this.rightFile) return

      const formData = new FormData()
      formData.append('img1', this.leftFile)
      formData.append('img2', this.rightFile)

      try {
        const response = await fetch('http://127.0.0.1:7860/api/predict', {
          method: 'POST',
          body: formData
        })
        
        const result = await response.json()
        this.similarity = result.similarity
      } catch (error) {
        console.error('计算相似度失败:', error)
        this.similarity = null
      }
    }
  }
}
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  text-align: center;
}

.image-upload-container {
  display: flex;
  justify-content: space-between;
  margin: 20px 0;
}

.upload-box {
  width: 45%;
}

.upload-demo {
  width: 100%;
}

.preview {
  margin-top: 10px;
}

.preview img {
  max-width: 100%;
  max-height: 300px;
}

.result-box {
  margin-top: 20px;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 4px;
}
</style>