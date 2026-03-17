<template>
  <div class="admin-page">
    <!-- Header -->
    <div class="admin-header">
      <h2 class="admin-title">工具管理</h2>
      <div class="flex gap-2">
        <el-button type="primary" @click="openCreate">新建工具</el-button>
        <el-button :icon="Refresh" circle @click="refreshTools"/>
      </div>
    </div>

    <!-- Filter -->
    <ToolFilterBar
      :filters="filterForm"
      :all-tags="allTags"
      @reset="resetFilters"
      @update:tags="filterForm.tags = $event"
      @update:title="filterForm.title = $event"
      @update:status="filterForm.status = $event"
    />

    <!-- Stats -->
    <p class="text-xs text-secondary/60 mb-4">共 {{ filteredTools.length }} 个工具</p>

    <!-- Grid -->
    <ToolGrid
      :tools="paginatedTools"
      @edit="openEdit"
      @delete="deleteTool"
      @update-status="updateStatus"
    />

    <!-- Pagination -->
    <div v-if="filteredTools.length > pageSize" class="flex justify-center mt-6">
      <el-pagination
        v-model:current-page="currentPage"
        :page-size="pageSize"
        :total="filteredTools.length"
        background
        layout="prev, pager, next"
      />
    </div>

    <!-- Dialog -->
    <ToolFormDialog
      v-model="dialogVisible"
      :tool="currentTool"
      :all-tags="allTags"
      :is-edit="isEditing"
      @success="refreshTools"
    />
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Refresh } from '@element-plus/icons-vue'
import axios from 'axios'
import ToolFilterBar from '@/components/Admin/ToolManagement/ToolFilterBar.vue'
import ToolGrid from '@/components/Admin/ToolManagement/ToolGrid.vue'
import ToolFormDialog from '@/components/Admin/ToolManagement/ToolFormDialog.vue'

const tools = ref([])
const allTags = ref([])
const currentPage = ref(1)
const pageSize = 12
const dialogVisible = ref(false)
const isEditing = ref(false)
const currentTool = ref(null)

const filterForm = reactive({ tags: [], title: '', status: '' })

const filteredTools = computed(() => {
  let arr = tools.value
  if (filterForm.tags.length) arr = arr.filter(t => t.tags?.length && filterForm.tags.every(tag => t.tags.includes(tag)))
  if (filterForm.title) arr = arr.filter(t => t.name?.includes(filterForm.title))
  if (filterForm.status) arr = arr.filter(t => t.status === filterForm.status)
  return arr
})

const paginatedTools = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return filteredTools.value.slice(start, start + pageSize)
})

watch([() => filterForm.tags, () => filterForm.title, () => filterForm.status], () => {
  currentPage.value = 1
}, { deep: true })

const resetFilters = () => {
  filterForm.tags = []
  filterForm.title = ''
  filterForm.status = ''
  currentPage.value = 1
}

const fetchTools = async () => {
  try {
    const res = await axios.get('/api/admin/tools', { timeout: 8000 })
    tools.value = (res.data || []).map(t => ({ ...t, tags: Array.isArray(t.tags) ? t.tags : [] }))
  } catch { ElMessage.error('获取工具列表失败') }
}

const fetchTags = async () => {
  try {
    const res = await axios.get('/api/tool-tags', { timeout: 5000 })
    allTags.value = res.data?.tags || []
  } catch {}
}

const refreshTools = async () => {
  await fetchTools()
  await fetchTags()
}

const openCreate = () => {
  isEditing.value = false
  currentTool.value = null
  dialogVisible.value = true
}

const openEdit = (tool) => {
  isEditing.value = true
  currentTool.value = { ...tool }
  dialogVisible.value = true
}

const deleteTool = async (tool) => {
  try {
    await ElMessageBox.confirm('确定要删除该工具吗？', '提示', { type: 'warning' })
    await axios.delete(`/api/tools/${tool.id}`)
    ElMessage.success('删除成功')
    refreshTools()
  } catch (e) {
    if (e !== 'cancel') ElMessage.error('删除失败')
  }
}

const updateStatus = async (tool, newStatus) => {
  if (tool.status === newStatus) return
  try {
    await axios.patch(`/api/tools/${tool.id}/status`, { status: newStatus })
    tool.status = newStatus
    ElMessage.success('状态已更新')
  } catch { ElMessage.error('更新失败'); refreshTools() }
}

onMounted(() => refreshTools())
</script>