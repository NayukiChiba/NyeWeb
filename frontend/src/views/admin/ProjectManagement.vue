<template>
  <div class="admin-page">
    <div class="admin-header">
      <h2 class="admin-title">项目管理</h2>
      <div class="flex gap-2">
        <el-button type="primary" @click="openCreate">上传项目</el-button>
        <el-button :icon="Refresh" circle @click="refreshProjects"/>
      </div>
    </div>

    <ProjectFilterBar :filters="filterForm" :all-tags="allTags" @reset="resetFilters" @update:tags="filterForm.tags = $event" @update:title="filterForm.title = $event" @update:status="filterForm.status = $event"/>
    <p class="text-xs text-secondary/60 mb-4">共 {{ filteredProjects.length }} 个项目</p>

    <ProjectGrid :projects="paginatedProjects" @edit="openEdit" @delete="deleteProject" @update-status="updateStatus"/>

    <div v-if="filteredProjects.length > pageSize" class="flex justify-center mt-6">
      <el-pagination v-model:current-page="currentPage" :page-size="pageSize" :total="filteredProjects.length" background layout="prev, pager, next"/>
    </div>

    <ProjectFormDialog v-model="dialogVisible" :project="currentProject" :all-tags="allTags" :is-edit="isEditing" @success="refreshProjects"/>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Refresh } from '@element-plus/icons-vue'
import axios from 'axios'
import ProjectFilterBar from '@/components/Admin/ProjectManagement/ProjectFilterBar.vue'
import ProjectGrid from '@/components/Admin/ProjectManagement/ProjectGrid.vue'
import ProjectFormDialog from '@/components/Admin/ProjectManagement/ProjectFormDialog.vue'

const projects = ref([])
const allTags = ref([])
const currentPage = ref(1)
const pageSize = 12
const dialogVisible = ref(false)
const isEditing = ref(false)
const currentProject = ref(null)
const filterForm = reactive({ tags: [], title: '', status: '' })

const filteredProjects = computed(() => {
  let arr = projects.value
  if (filterForm.tags.length) arr = arr.filter(p => p.tags?.length && filterForm.tags.every(tag => p.tags.includes(tag)))
  if (filterForm.title) arr = arr.filter(p => p.name?.includes(filterForm.title))
  if (filterForm.status) arr = arr.filter(p => p.status === filterForm.status)
  return arr
})

const paginatedProjects = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return filteredProjects.value.slice(start, start + pageSize)
})

watch([() => filterForm.tags, () => filterForm.title, () => filterForm.status], () => { currentPage.value = 1 }, { deep: true })

const resetFilters = () => { filterForm.tags = []; filterForm.title = ''; filterForm.status = ''; currentPage.value = 1 }

const fetchProjects = async () => {
  try {
    const res = await axios.get('/api/admin/projects')
    projects.value = res.data || []
  } catch { ElMessage.error('获取项目列表失败') }
}

const fetchTags = async () => {
  try {
    const res = await axios.get('/api/project-tags')
    allTags.value = res.data?.tags || []
  } catch {}
}

const refreshProjects = async () => { await fetchProjects(); await fetchTags() }
const openCreate = () => { isEditing.value = false; currentProject.value = null; dialogVisible.value = true }
const openEdit = (p) => { isEditing.value = true; currentProject.value = { ...p }; dialogVisible.value = true }

const deleteProject = async (p) => {
  try {
    await ElMessageBox.confirm('确定要删除该项目吗？', '提示', { type: 'warning' })
    await axios.delete(`/api/projects/${p.id}`)
    ElMessage.success('删除成功')
    refreshProjects()
  } catch (e) { if (e !== 'cancel') ElMessage.error('删除失败') }
}

const updateStatus = async (p, newStatus) => {
  if (p.status === newStatus) return
  try {
    await axios.patch(`/api/projects/${p.id}/status`, { status: newStatus })
    p.status = newStatus
    ElMessage.success('状态已更新')
  } catch { ElMessage.error('更新失败'); refreshProjects() }
}

onMounted(() => refreshProjects())
</script>