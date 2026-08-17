import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/utils/api'

export interface Project {
  project_id: string
  name: string
  primary_type: string
  secondary_types: string[]
  status: string
  created_at: string
  updated_at: string
}

export const useProjectStore = defineStore('project', () => {
  const projects = ref<Project[]>([])
  const currentProject = ref<Project | null>(null)

  async function fetchProjects() {
    const res = await api.get('/projects/list')
    projects.value = (res.data as any).items || []
    return projects.value
  }

  async function createProject(name: string, primaryType: string, secondaryTypes: string[]) {
    const res = await api.post('/projects', {
      name,
      primary_type: primaryType,
      secondary_types: secondaryTypes
    })
    await fetchProjects()
    return res.data as Project
  }

  async function fetchProject(id: string) {
    const res = await api.get(`/projects/${id}`)
    currentProject.value = res.data as Project
    return currentProject.value
  }

  return { projects, currentProject, fetchProjects, createProject, fetchProject }
})
