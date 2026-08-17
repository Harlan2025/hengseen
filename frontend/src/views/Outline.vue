<template>
  <div class="outline">
    <el-page-header @back="router.push(`/project/${projectId}`)" title="返回">
      <template #content>
        <span class="page-title">合同大纲</span>
      </template>
    </el-page-header>

    <el-divider />

    <div class="outline-container">
      <el-card>
        <template #header>
          <div class="card-header">
            <span>章节结构</span>
            <el-button type="primary" size="small" @click="regenerate" :loading="regenerating">
              重新生成
            </el-button>
          </div>
        </template>

        <el-table :data="chapters" stripe>
          <el-table-column type="index" label="序号" width="60" />
          <el-table-column prop="title" label="章节标题" />
          <el-table-column prop="content" label="章节说明" />
          <el-table-column label="操作" width="120">
            <template #default="{ row }">
              <el-button link type="primary" @click="editChapter(row)">编辑</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>

      <div class="actions">
        <el-button type="success" size="large" @click="confirmOutline">
          确认大纲并生成合同
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
const chapters = ref<any[]>([])
const regenerating = ref(false)

async function generate() {
  try {
    const res = await api.post('/outline/generate', {
      project_id: projectId.value
    })
    chapters.value = res.data.chapters || []
  } catch (e: any) {
    ElMessage.error(e.response?.data?.detail?.msg || '生成失败')
  }
}

function regenerate() {
  regenerating.value = true
  generate().finally(() => {
    regenerating.value = false
  })
}

function confirmOutline() {
  router.push(`/contract/${projectId.value}`)
}

function editChapter(row: any) {
  ElMessage.info('编辑功能开发中')
}

onMounted(generate)
</script>

<style scoped>
.outline {
  padding: 20px 0;
}

.page-title {
  font-size: 20px;
  font-weight: bold;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.actions {
  margin-top: 20px;
  text-align: center;
}
</style>
