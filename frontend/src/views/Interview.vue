<template>
  <div class="interview">
    <el-page-header @back="router.push(`/project/${projectId}`)" title="返回">
      <template #content>
        <span class="page-title">AI访谈</span>
      </template>
    </el-page-header>

    <el-divider />

    <div class="interview-container">
      <!-- 进度条 -->
      <el-progress :percentage="progress" :status="progress >= 100 ? 'success' : ''" />

      <!-- 问题卡片 -->
      <el-card class="question-card" v-if="currentQuestion">
        <template #header>
          <div class="question-header">
            <span class="question-label">问题 {{ currentStep }} / {{ totalSteps }}</span>
            <el-tag v-if="currentQuestion.required" type="danger" size="small">必填</el-tag>
          </div>
        </template>
        
        <div class="question-text">{{ currentQuestion.text }}</div>
        
        <el-input
          v-model="answer"
          type="textarea"
          :rows="4"
          placeholder="请输入您的回答..."
          class="answer-input"
        />
        
        <div class="question-actions">
          <el-button @click="skipQuestion">跳过</el-button>
          <el-button type="primary" @click="submitAnswer" :loading="submitting">
            提交
          </el-button>
        </div>
      </el-card>

      <!-- 已确认要素 -->
      <el-card class="confirmed-card" v-if="confirmedElements.length > 0">
        <template #header>已确认要素</template>
        <el-tag 
          v-for="elem in confirmedElements" 
          :key="elem.element"
          class="elem-tag"
          type="success"
        >
          {{ elem.element }}: {{ elem.value }}
        </el-tag>
      </el-card>

      <!-- 风险提醒 -->
      <el-card class="risk-card" v-if="risks.length > 0">
        <template #header>风险提醒</template>
        <el-alert
          v-for="(risk, index) in risks"
          :key="index"
          :title="risk.description"
          :type="risk.level === 'high' ? 'error' : risk.level === 'medium' ? 'warning' : 'info'"
          :closable="false"
          show-icon
          style="margin-bottom: 10px"
        />
      </el-card>
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
const currentQuestion = ref<any>(null)
const answer = ref('')
const submitting = ref(false)
const currentStep = ref(1)
const totalSteps = ref(5)
const confirmedElements = ref<any[]>([])
const risks = ref<any[]>([])
const snapshot = ref<any>(null)

const progress = computed(() => Math.round((currentStep.value / totalSteps.value) * 100))

async function fetchQuestion() {
  try {
    const res = await api.get(`/interview/${projectId.value}/question`)
    currentQuestion.value = res.data
  } catch (e) {
    ElMessage.error('获取问题失败')
  }
}

async function submitAnswer() {
  if (!answer.value.trim()) {
    ElMessage.warning('请输入回答')
    return
  }
  
  submitting.value = true
  try {
    const res = await api.post(`/interview/${projectId.value}/answer`, {
      answer: answer.value
    })
    
    snapshot.value = res.data.snapshot
    confirmedElements.value = res.data.confirmed_elements || []
    risks.value = res.data.risks || []
    
    if (res.data.next_question) {
      currentStep.value++
      currentQuestion.value = res.data.next_question
    } else {
      ElMessage.success('访谈完成！')
      router.push(`/project/${projectId.value}`)
    }
    answer.value = ''
  } catch (e: any) {
    ElMessage.error(e.response?.data?.detail?.msg || '提交失败')
  } finally {
    submitting.value = false
  }
}

function skipQuestion() {
  submitAnswer()
}

onMounted(fetchQuestion)
</script>

<style scoped>
.interview {
  padding: 20px 0;
}

.page-title {
  font-size: 20px;
  font-weight: bold;
}

.interview-container {
  max-width: 800px;
  margin: 0 auto;
}

.question-card {
  margin-top: 20px;
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.question-text {
  font-size: 18px;
  font-weight: 500;
  margin-bottom: 20px;
  line-height: 1.6;
}

.answer-input {
  margin-bottom: 20px;
}

.question-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.confirmed-card, .risk-card {
  margin-top: 20px;
}

.elem-tag {
  margin-right: 10px;
  margin-bottom: 10px;
}
</style>
