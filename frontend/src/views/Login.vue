<template>
  <div class="login-container">
    <div class="login-box">
      <div class="logo">
        <h1>衡简叙约</h1>
        <p>AI访谈式合同生成系统</p>
      </div>
      
      <el-tabs v-model="activeTab">
        <el-tab-pane label="登录" name="login">
          <el-form :model="loginForm" :rules="loginRules" ref="loginFormRef">
            <el-form-item prop="phone">
              <el-input 
                v-model="loginForm.phone" 
                placeholder="手机号"
                prefix-icon="Phone"
                maxlength="11"
              />
            </el-form-item>
            <el-form-item prop="code">
              <el-input 
                v-model="loginForm.code" 
                placeholder="验证码"
                prefix-icon="Message"
                maxlength="6"
              >
                <template #append>
                  <el-button @click="sendCode" :disabled="countdown > 0">
                    {{ countdown > 0 ? `${countdown}s` : '获取验证码' }}
                  </el-button>
                </template>
              </el-input>
            </el-form-item>
            <el-form-item>
              <el-button 
                type="primary" 
                style="width: 100%"
                :loading="loading"
                @click="handleLogin"
              >
                登录
              </el-button>
            </el-form-item>
            <div class="footer-link">
              还没有账号？<router-link to="/register">立即注册</router-link>
            </div>
          </el-form>
        </el-tab-pane>
        
        <el-tab-pane label="注册" name="register">
          <el-form :model="registerForm" :rules="registerRules" ref="registerFormRef">
            <el-form-item prop="phone">
              <el-input 
                v-model="registerForm.phone" 
                placeholder="手机号"
                prefix-icon="Phone"
                maxlength="11"
              />
            </el-form-item>
            <el-form-item prop="code">
              <el-input 
                v-model="registerForm.code" 
                placeholder="验证码"
                prefix-icon="Message"
                maxlength="6"
              >
                <template #append>
                  <el-button @click="sendCodeRegister" :disabled="countdownRegister > 0">
                    {{ countdownRegister > 0 ? `${countdownRegister}s` : '获取验证码' }}
                  </el-button>
                </template>
              </el-input>
            </el-form-item>
            <el-form-item prop="nickname">
              <el-input 
                v-model="registerForm.nickname" 
                placeholder="昵称（可选）"
                prefix-icon="User"
                maxlength="50"
              />
            </el-form-item>
            <el-form-item>
              <el-button 
                type="primary" 
                style="width: 100%"
                :loading="loading"
                @click="handleRegister"
              >
                注册
              </el-button>
            </el-form-item>
            <div class="footer-link">
              已有账号？<router-link to="/login">立即登录</router-link>
            </div>
          </el-form>
        </el-tab-pane>
      </el-tabs>
      
      <div class="test-account">
        <p>测试账号：13900139001 / 验证码：123456</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'

const router = useRouter()
const authStore = useAuthStore()

const activeTab = ref('login')
const loading = ref(false)
const countdown = ref(0)
const countdownRegister = ref(0)

const loginForm = reactive({
  phone: '',
  code: ''
})

const registerForm = reactive({
  phone: '',
  code: '',
  nickname: ''
})

const loginRules = {
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
  ],
  code: [
    { required: true, message: '请输入验证码', trigger: 'blur' },
    { pattern: /^\d{4,6}$/, message: '请输入4-6位验证码', trigger: 'blur' }
  ]
}

const registerRules = {
  ...loginRules,
  nickname: [{ max: 50, message: '昵称不能超过50个字符', trigger: 'blur' }]
}

const loginFormRef = ref()
const registerFormRef = ref()

function startCountdown(target: any) {
  target.value = 60
  const timer = setInterval(() => {
    target.value--
    if (target.value <= 0) {
      clearInterval(timer)
    }
  }, 1000)
}

async function sendCode() {
  if (!loginForm.phone) {
    ElMessage.warning('请先输入手机号')
    return
  }
  // Mock: 验证码固定为123456
  ElMessage.success('验证码已发送：123456')
  startCountdown(countdown)
}

async function sendCodeRegister() {
  if (!registerForm.phone) {
    ElMessage.warning('请先输入手机号')
    return
  }
  ElMessage.success('验证码已发送：123456')
  startCountdown(countdownRegister)
}

async function handleLogin() {
  await loginFormRef.value.validate(async (valid: boolean) => {
    if (!valid) return
    loading.value = true
    try {
      await authStore.login(loginForm.phone, loginForm.code)
      ElMessage.success('登录成功')
      router.push('/projects')
    } catch (e: any) {
      ElMessage.error(e.response?.data?.detail?.msg || '登录失败')
    } finally {
      loading.value = false
    }
  })
}

async function handleRegister() {
  await registerFormRef.value.validate(async (valid: boolean) => {
    if (!valid) return
    loading.value = true
    try {
      await authStore.register(registerForm.phone, registerForm.code, registerForm.nickname)
      ElMessage.success('注册成功')
      router.push('/projects')
    } catch (e: any) {
      ElMessage.error(e.response?.data?.detail?.msg || '注册失败')
    } finally {
      loading.value = false
    }
  })
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-box {
  background: white;
  border-radius: 16px;
  padding: 40px;
  width: 420px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.logo {
  text-align: center;
  margin-bottom: 30px;
}

.logo h1 {
  font-size: 32px;
  color: #1a1a1a;
  margin-bottom: 8px;
}

.logo p {
  color: #666;
  font-size: 14px;
}

.footer-link {
  text-align: center;
  margin-top: 16px;
  font-size: 14px;
  color: #666;
}

.footer-link a {
  color: #409eff;
  text-decoration: none;
}

.test-account {
  margin-top: 24px;
  padding: 12px;
  background: #f5f7fa;
  border-radius: 8px;
  text-align: center;
  font-size: 12px;
  color: #999;
}
</style>
