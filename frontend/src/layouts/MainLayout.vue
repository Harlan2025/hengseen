<template>
  <div class="layout">
    <el-header class="header">
      <div class="logo">衡简叙约</div>
      <el-menu mode="horizontal" :ellipsis="false" class="nav-menu">
        <el-menu-item index="/projects">我的项目</el-menu-item>
        <el-menu-item index="#" @click="handleLogout">退出登录</el-menu-item>
      </el-menu>
    </el-header>
    
    <el-main class="main">
      <router-view />
    </el-main>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'

const router = useRouter()
const authStore = useAuthStore()

async function handleLogout() {
  authStore.logout()
  ElMessage.success('已退出登录')
  router.push('/login')
}
</script>

<style scoped>
.layout {
  min-height: 100vh;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: white;
  padding: 0 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.logo {
  font-size: 24px;
  font-weight: bold;
  color: #0077B6;
}

.nav-menu {
  border-bottom: none;
}

.main {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}
</style>
