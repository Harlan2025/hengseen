<template>
  <div class="contract">
    <el-page-header @back="router.push(`/project/${projectId}`)" title="返回">
      <template #content>
        <span class="page-title">合同生成</span>
      </template>
    </el-page-header>

    <el-divider />

    <div class="contract-container">
      <!-- 合同文本 -->
      <el-card class="contract-card">
        <template #header>
          <div class="card-header">
            <span>合同文本</span>
            <el-space>
              <el-button size="small" @click="copyContract">复制</el-button>
              <el-button size="small" type="success" @click="exportContract">导出</el-button>
            </el-space>
          </div>
        </template>
        
        <div class="contract-content" v-html="formattedContract"></div>
      </el-card>

      <!-- 风险提示 -->
      <el-card class="risk-card" v-if="riskNotes.length > 0">
        <template #header>风险提示</template>
        <el-alert
          v-for="(note, index) in riskNotes"
          :key="index"
          :title="note"
          type="warning"
          :closable="false"
          show-icon
          style="margin-bottom: 10px"
        />
      </el-card>

      <!-- 生成按钮 -->
      <div class="actions">
        <el-button type="primary" size="large" @click="generateContract" :loading="generating">
          重新生成
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import api from '@/utils/api'
import { ElMessage } from 'element-plus'

const router = useRouter()
const route = useRoute()

const projectId = computed(() => route.params.id as string)
const contractText = ref('')
const riskNotes = ref<string[]>([])
const generating = ref(false)

const formattedContract = computed(() => {
  return contractText.value
    .split('\n')
    .map(line => {
      if (line.startsWith('#')) return `<h1>${line.replace(/^#+\s*/, '')}</h1>`
      if (line.startsWith('##')) return `<h2>${line.replace(/^#+\s*/, '')}</h2>`
      if (line.startsWith('###')) return `<h3>${line.replace(/^#+\s*/, '')}</h3>`
      if (line.startsWith('- ')) return `<li>${line.substring(2)}</li>`
      return `<p>${line}</p>`
    })
    .join('')
})

async function generateContract() {
  generating.value = true
  try {
    const res = await api.post('/contract/generate', {
      project_id: projectId.value
    })
    contractText.value = res.data.contract_text
    riskNotes.value = res.data.risk_notes || []
    ElMessage.success('合同生成成功')
  } catch (e: any) {
    ElMessage.error(e.response?.data?.detail?.msg || '生成失败')
  } finally {
    generating.value = false
  }
}

function copyContract() {
  navigator.clipboard.writeText(contractText.value)
  ElMessage.success('已复制到剪贴板')
}

async function exportContract() {
  try {
    const res = await api.post('/export', {
      project_id: projectId.value,
      format: 'word'
    })
    // 下载文件
    const url = window.URL.createObjectURL(new Blob([res.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `合同_${projectId.value}.docx`)
    document.body.appendChild(link)
    link.click()
    link.remove()
  } catch (e: any) {
    ElMessage.error(e.response?.data?.detail?.msg || '导出失败')
  }
}

onMounted(async () => {
  if (!contractText.value) {
    await generateContract()
  }
})
</script>

<style scoped>
.contract {
  padding: 20px 0;
}

.page-title {
  font-size: 20px;
  font-weight: bold;
}

.contract-container {
  max-width: 900px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.contract-content {
  line-height: 1.8;
  padding: 20px;
  background: #fafafa;
  border-radius: 8px;
}

.contract-content h1, .contract-content h2, .contract-content h3 {
  margin: 16px 0 8px;
}

.contract-content p {
  margin: 8px 0;
}

.risk-card {
  margin-top: 20px;
}

.actions {
  margin-top: 20px;
  text-align: center;
}
</style>
