import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/utils/api'

export interface User {
  user_id: string
  nickname: string | null
  avatar_url: string | null
  login_type: string
  created_at: string
}

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string>(localStorage.getItem('token') || '')

  const isLoggedIn = computed(() => !!token.value)
  const userName = computed(() => user.value?.nickname || user.value?.user_id || '用户')

  async function login(phone: string, code: string) {
    const res = await api.post('/auth/login', {
      phone,
      code,
      agree_user_agreement: true,
      agree_privacy_policy: true,
      agreement_version: 'V1.0'
    })
    const data = res.data as any
    token.value = data.access_token
    localStorage.setItem('token', data.access_token)
    await fetchUser()
    return data
  }

  async function register(phone: string, code: string, nickname: string) {
    const res = await api.post('/auth/register', {
      phone,
      code,
      nickname,
      agree_user_agreement: true,
      agree_privacy_policy: true,
      agreement_version: 'V1.0'
    })
    const data = res.data as any
    token.value = data.access_token
    localStorage.setItem('token', data.access_token)
    await fetchUser()
    return data
  }

  async function fetchUser() {
    try {
      const res = await api.get('/auth/me')
      user.value = res.data as User
    } catch {
      logout()
    }
  }

  function logout() {
    token.value = ''
    user.value = null
    localStorage.removeItem('token')
  }

  return { user, token, isLoggedIn, userName, login, register, fetchUser, logout }
})
