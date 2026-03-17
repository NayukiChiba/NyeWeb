<template>
  <div class="admin-page">
    <div class="admin-header">
      <h2 class="admin-title">待办管理</h2>
      <div class="flex gap-2">
        <el-button type="primary" @click="openCreate">新增待办</el-button>
        <el-button :icon="Refresh" circle @click="refreshTodos"/>
      </div>
    </div>

    <p class="text-xs text-secondary/60 mb-4">共 {{ todos.length }} 条待办</p>

    <div v-if="paginatedTodos.length" class="admin-grid-compact">
      <div v-for="t in paginatedTodos" :key="t.id" class="admin-card">
        <div class="flex items-start justify-between mb-2">
          <div class="flex items-center gap-2 flex-1 min-w-0">
            <span v-if="t.icon" class="text-base flex-shrink-0" v-html="iconPreview(t.icon)"/>
            <h3 class="font-bold text-sm text-primary truncate">{{ t.task }}</h3>
          </div>
          <span :class="['status-badge ml-2', t.completed ? 'published' : 'draft']">
            {{ t.completed ? '已完成' : '进行中' }}
          </span>
        </div>
        <div class="flex flex-wrap gap-2 mb-3">
          <el-tag :type="typeTagMap[t.type] || 'info'" size="small">{{ typeTextMap[t.type] || t.type }}</el-tag>
          <el-tag :type="priorityTagMap[t.priority] || 'info'" size="small" effect="dark">{{ t.priority }}</el-tag>
        </div>
        <el-progress :percentage="t.progress || 0" :stroke-width="4" class="mb-2"/>
        <div class="pt-3 border-t border-gray-100 flex items-center justify-between">
          <el-button size="small" @click="toggleCompleted(t)">
            {{ t.completed ? '标记未完成' : '标记完成' }}
          </el-button>
          <div class="flex gap-2">
            <el-button size="small" @click="openEdit(t)">编辑</el-button>
            <el-button size="small" type="danger" @click="deleteTodo(t)">删除</el-button>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="admin-empty">
      <p>暂无待办</p>
    </div>

    <div v-if="todos.length > pageSize" class="flex justify-center mt-6">
      <el-pagination v-model:current-page="currentPage" :page-size="pageSize" :total="todos.length" background layout="prev, pager, next"/>
    </div>

    <el-dialog v-model="dialogVisible" :title="isEditing ? '编辑待办' : '新增待办'" width="520px" destroy-on-close>
      <el-form :model="form" label-width="80px">
        <el-form-item label="任务" required>
          <el-input v-model="form.task" placeholder="输入任务描述"/>
        </el-form-item>
        <el-form-item label="类型">
          <el-select v-model="form.type" style="width: 100%">
            <el-option label="🚀 短期" value="short-term"/><el-option label="📅 中期" value="mid-term"/><el-option label="🏔️ 长期" value="long-term"/>
          </el-select>
        </el-form-item>
        <el-form-item label="优先级">
          <el-select v-model="form.priority" style="width: 100%">
            <el-option label="高" value="high"/><el-option label="中" value="medium"/><el-option label="低" value="low"/>
          </el-select>
        </el-form-item>
        <el-form-item label="进度">
          <el-slider v-model="form.progress" :min="0" :max="100" show-input/>
        </el-form-item>
        <el-form-item label="图标">
          <el-input v-model="form.icon" placeholder="Emoji / URL / SVG"/>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="form.status" style="width: 100%">
            <el-option label="活跃" value="active"/><el-option label="隐藏" value="inactive"/>
          </el-select>
        </el-form-item>
        <el-form-item v-if="isEditing" label="完成">
          <el-switch v-model="form.completed"/>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="submitTodo">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Refresh } from '@element-plus/icons-vue'
import axios from 'axios'

const todos = ref([])
const currentPage = ref(1)
const pageSize = 12
const dialogVisible = ref(false)
const isEditing = ref(false)
const editingId = ref(null)
const submitting = ref(false)

const typeTextMap = { 'short-term': '短期', 'mid-term': '中期', 'long-term': '长期' }
const typeTagMap = { 'short-term': 'danger', 'mid-term': 'warning', 'long-term': 'success' }
const priorityTagMap = { high: 'danger', medium: 'warning', low: 'success' }

const defaultForm = () => ({ task: '', type: 'short-term', priority: 'medium', progress: 0, icon: '', status: 'active', completed: false })
const form = ref(defaultForm())

const paginatedTodos = computed(() => todos.value.slice((currentPage.value - 1) * pageSize, currentPage.value * pageSize))

const iconPreview = (icon) => {
  if (!icon) return ''
  if (icon.startsWith('<svg')) return `<span style="display:inline-flex;width:18px;height:18px;">${icon}</span>`
  if (icon.startsWith('http') || icon.startsWith('/')) return `<img src="${icon}" alt="" style="width:18px;height:18px;object-fit:contain;"/>`
  return icon
}

const fetchTodos = async () => {
  try { todos.value = (await axios.get('/api/admin/todos')).data || [] } catch { ElMessage.error('获取待办失败') }
}

const refreshTodos = () => fetchTodos()
const openCreate = () => { isEditing.value = false; editingId.value = null; form.value = defaultForm(); dialogVisible.value = true }
const openEdit = (t) => {
  isEditing.value = true; editingId.value = t.id
  form.value = { task: t.task, type: t.type || 'short-term', priority: t.priority || 'medium', progress: t.progress || 0, icon: t.icon || '', status: t.status || 'active', completed: t.completed || false }
  dialogVisible.value = true
}

const submitTodo = async () => {
  if (!form.value.task) { ElMessage.warning('请填写任务描述'); return }
  submitting.value = true
  try {
    const payload = { ...form.value }
    if (!isEditing.value) delete payload.completed
    if (isEditing.value) { await axios.put(`/api/todos/${editingId.value}`, payload); ElMessage.success('已更新') }
    else { await axios.post('/api/todos', payload); ElMessage.success('已创建') }
    dialogVisible.value = false; refreshTodos()
  } catch { ElMessage.error('提交失败') }
  finally { submitting.value = false }
}

const toggleCompleted = async (t) => {
  try { await axios.put(`/api/todos/${t.id}`, { completed: !t.completed }); ElMessage.success(t.completed ? '已标记未完成' : '已完成'); refreshTodos() }
  catch { ElMessage.error('更新失败') }
}

const deleteTodo = async (t) => {
  try {
    await ElMessageBox.confirm('确定删除？', '提示', { type: 'warning' })
    await axios.delete(`/api/todos/${t.id}`); ElMessage.success('删除成功'); refreshTodos()
  } catch (e) { if (e !== 'cancel') ElMessage.error('删除失败') }
}

onMounted(() => refreshTodos())
</script>
