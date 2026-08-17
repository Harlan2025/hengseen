<template>
  <div class="project-list">
    <div class="header">
      <h2>我的项目</h2>
      <el-button type="primary" @click="showCreateDialog">
        <el-icon><Plus /></el-icon>
        新建项目
      </el-button>
    </div>

    <el-empty v-if="projects.length === 0" description="暂无项目">
      <el-button type="primary" @click="showCreateDialog">创建第一个项目</el-button>
    </el-empty>

    <el-row :gutter="20" v-else>
      <el-col :xs="24" :sm="12" :md="8" v-for="project in projects" :key="project.project_id">
        <el-card class="project-card" shadow="hover" @click="goToProject(project)">
          <template #header>
            <div class="card-header">
              <span class="project-name">{{ project.name }}</span>
              <el-tag :type="statusType(project.status)" size="small">
                {{ statusText(project.status) }}
              </el-tag>
            </div>
          </template>
          <div class="project-info">
            <p><strong>类型：</strong>{{ typeText(project.primary_type) }} {{ project.secondary_types.map(t => typeText(t)).join(' + ') }}</p>
            <p><strong>创建时间：</strong>{{ formatDate(project.created_at) }}</p>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 创建项目对话框 -->
    <el-dialog v-model="createVisible" title="新建项目" width="500px">
      <el-form :model="createForm" :rules="createRules" ref="createFormRef" label-width="100px">
        <el-form-item label="项目名称" prop="name">
          <el-input v-model="createForm.name" placeholder="请输入项目名称" />
        </el-form-item>
        <el-form-item label="主类型" prop="primary_type">
          <el-select v-model="createForm.primary_type" placeholder="选择主类型" style="width: 100%">
            <el-option v-for="t in primaryTypes" :key="t.code" :label="t.name" :value="t.code" />
          </el-select>
        </el-form-item>
        <el-form-item label="附属类型">
          <el-select v-model="createForm.secondary_types" multiple placeholder="可选，最多2个" style="width: 100%">
            <el-option v-for="t in secondaryTypes" :key="t.code" :label="t.name" :value="t.code" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="createVisible = false">取消</el-button>
        <el-button type="primary" @click="handleCreate" :loading="creating">创建</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useProjectStore } from '@/stores/project'
import { ElMessage } from 'element-plus'

const router = useRouter()
const projectStore = useProjectStore()

const projects = ref<any[]>([])
const createVisible = ref(false)
const creating = ref(false)
const createFormRef = ref()

const createForm = ref({
  name: '',
  primary_type: '',
  secondary_types: [] as string[]
})

const createRules = {
  name: [{ required: true, message: '请输入项目名称', trigger: 'blur' }],
  primary_type: [{ required: true, message: '请选择主类型', trigger: 'change' }]
}

const primaryTypes = [
  { code: 'A', name: '买卖' },
  { code: 'B', name: '备忘录' },
  { code: 'C', name: '股权转让' },
  { code: 'D', name: '合作' },
  { code: 'E', name: '劳动' },
  { code: 'F', name: '知识产权' },
  { code: 'G', name: '担保' },
  { code: 'H', name: '债权' },
  { code: 'I', name: '居间' },
  { code: 'J', name: '终止' }
]

const secondaryTypes = [
  { code: 'A', name: '买卖' },
  { code: 'B', name: '备忘录' },
  { code: 'C', name: '股权转让' },
  { code: 'D', name: '合作' },
  { code: 'E', name: '劳动' },
  { code: 'F', name: '知识产权' },
  { code: 'G', name: '担保' },
  { code: 'H', name: '债权' },
  { code: 'I', name: '居间' },
  { code: 'J', name: '终止' }
]

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
  const t = primaryTypes.find(p => p.code === code)
  return t?.name || code
}

function formatDate(dateStr: string) {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('zh-CN')
}

function showCreateDialog() {
  createVisible.value = true
}

async function handleCreate() {
  await createFormRef.value.validate(async (valid: boolean) => {
    if (!valid) return
    creating.value = true
    try {
      await projectStore.createProject(
        createForm.value.name,
        createForm.value.primary_type,
        createForm.value.secondary_types
      )
      ElMessage.success('项目创建成功')
      createVisible.value = false
    } catch (e: any) {
      ElMessage.error(e.response?.data?.detail?.msg || '创建失败')
    } finally {
      creating.value = false
    }
  })
}

function goToProject(project: any) {
  router.push(`/project/${project.project_id}`)
}

onMounted(async () => {
  projects.value = await projectStore.fetchProjects()
})
</script>

<style scoped>
.project-list {
  padding: 20px 0;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.header h2 {
  font-size: 24px;
  margin: 0;
}

.project-card {
  margin-bottom: 20px;
  cursor: pointer;
  transition: transform 0.2s;
}

.project-card:hover {
  transform: translateY(-4px);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.project-name {
  font-weight: bold;
  font-size: 16px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 200px;
}

.project-info p {
  margin: 8px 0;
  font-size: 14px;
  color: #666;
}
</style>
