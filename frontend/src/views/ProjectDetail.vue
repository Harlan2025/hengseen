<template>
  <div class="project-detail">
    <el-page-header @back="router.push('/projects')" :title="'返回项目列表'">
      <template #content>
        <span class="page-title">{{ project?.name }}</span>
      </template>
    </el-page-header>

    <el-divider />

    <el-row :gutter="20">
      <el-col :span="16">
        <el-card>
          <template #header>项目信息</template>
          <el-descriptions :column="2" border>
            <el-descriptions-item label="项目编号">{{ project?.project_id?.slice(0, 8) }}...</el-descriptions-item>
            <el-descriptions-item label="状态">
              <el-tag :type="statusType(project?.status)">
                {{ statusText(project?.status) }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="主类型">{{ typeText(project?.primary_type) }}</el-descriptions-item>
            <el-descriptions-item label="附属类型">
              {{ project?.secondary_types?.map(t => typeText(t)).join(' + ') || '无' }}
            </el-descriptions-item>
            <el-descriptions-item label="创建时间">{{ formatDate(project?.created_at) }}</el-descriptions-item>
            <el-descriptions-item label="更新时间">{{ formatDate(project?.updated_at) }}</el-descriptions-item>
          </el-descriptions>
        </el-card>

        <el-card style="margin-top: 20px">
          <template #header>操作</template>
          <el-space wrap>
            <el-button 
              type="primary" 
              :disabled="!canInterview"
              @click="startInterview"
            >
              开始访谈
            </el-button>
            <el-button 
              type="success" 
              :disabled="!canOutline"
              @click="generateOutline"
            >
              生成大纲
            </el-button>
            <el-button 
              type="warning" 
              :disabled="!canContract"
              @click="generateContract"
            >
              生成合同
            </el-button>
          </el-space>
        </el-card>
      </el-col>

      <el-col :span="8">
        <el-card>
          <template #header>当前进度</template>
          <el-steps :active="currentStep" finish-status="success">
            <el-step title="创建项目" />
            <el-step title="AI访谈" />
            <el-step title="确认大纲" />
            <el-step title="生成合同" />
            <el-step title="导出文档" />
          </el-steps>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useProjectStore } from '@/stores/project'
import { ElMessage } from 'element-plus'

const router = useRouter()
const route = useRoute()
const projectStore = useProjectStore()

const project = ref<any>(null)
const currentStep = ref(0)

const projectId = computed(() => route.params.id as string)

const canInterview = computed(() => project.value?.status === 'init' || project.value?.status === 'interviewing')
const canOutline = computed(() => project.value?.status === 'interviewing')
const canContract = computed(() => project.value?.status === 'outline_generated' || project.value?.status === 'contract_generated')

function statusType(status: string) {
  const types: Record<string, string> = {
    init: 'info',
    interviewing: 'warning',
    outline_generated: 'primary',
    contract_generated: 'success',
    ready_export: 'success'
  }
  return types[status] || 'info'
}

function statusText(status: string) {
  const texts: Record<string, string> = {
    init: '初始化',
    interviewing: '访谈中',
    outline_generated: '大纲已生成',
    contract_generated: '合同已生成',
    ready_export: '可导出'
  }
  return texts[status] || status
}

function typeText(code: string) {
  const types: Record<string, string> = {
    A: '买卖', B: '备忘录', C: '股权转让', D: '合作',
    E: '劳动', F: '知识产权', G: '担保', H: '债权',
    I: '居间', J: '终止'
  }
  return types[code] || code
}

function formatDate(dateStr: string) {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleDateString('zh-CN')
}

function updateStep() {
  const status = project.value?.status
  const steps: Record<string, number> = {
    init: 0,
    interviewing: 1,
    outline_generated: 2,
    contract_generated: 3,
    ready_export: 4
  }
  currentStep.value = steps[status] || 0
}

function startInterview() {
  router.push(`/interview/${projectId.value}`)
}

function generateOutline() {
  // TODO: 调用API生成大纲
  ElMessage.info('正在生成大纲...')
}

function generateContract() {
  router.push(`/contract/${projectId.value}`)
}

onMounted(async () => {
  project.value = await projectStore.fetchProject(projectId.value)
  updateStep()
})
</script>

<style scoped>
.project-detail {
  padding: 20px 0;
}

.page-title {
  font-size: 20px;
  font-weight: bold;
}
</style>
