<template>
  <div class="todo-management">
    <!-- 操作栏 -->
    <div class="action-bar">
      <div class="action-buttons">
        <el-button type="primary" @click="openCreateDialog">新增待办</el-button>
        <el-button :icon="Refresh" circle @click="refreshTodos"/>
      </div>
    </div>

    <!-- 待办列表 -->
    <el-card shadow="never" class="list-card">
      <el-table :data="paginatedTodos" v-loading="loading" stripe style="width: 100%">
        <el-table-column prop="id" label="ID" width="70" sortable/>
        <el-table-column prop="task" label="任务" min-width="200" show-overflow-tooltip/>
        <el-table-column prop="type" label="类型" width="120">
          <template #default="{ row }">
            <el-tag :type="typeTagMap[row.type] || 'info'" size="small">{{ typeTextMap[row.type] || row.type }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="priority" label="优先级" width="100">
          <template #default="{ row }">
            <el-tag :type="priorityTagMap[row.priority] || 'info'" size="small" effect="dark">
              {{ row.priority }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="progress" label="进度" width="150">
          <template #default="{ row }">
            <el-progress :percentage="row.progress || 0" :stroke-width="6" :text-inside="false" style="width: 100px"/>
          </template>
        </el-table-column>
        <el-table-column prop="completed" label="状态" width="90">
          <template #default="{ row }">
            <el-tag :type="row.completed ? 'success' : 'warning'" size="small">
              {{ row.completed ? '已完成' : '进行中' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="icon" label="图标" width="70">
          <template #default="{ row }">
            <span v-if="row.icon" v-html="iconPreview(row.icon)"></span>
            <span v-else class="text-muted">无</span>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="可见性" width="90">
          <template #default="{ row }">
            <el-tag :type="row.status === 'active' ? 'success' : 'danger'" size="small">
              {{ row.status === 'active' ? '活跃' : '隐藏' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="240" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="toggleCompleted(row)">
              {{ row.completed ? '标记未完成' : '标记完成' }}
            </el-button>
            <el-button size="small" @click="openEditDialog(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="deleteTodo(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div v-if="todos.length > pageSize" class="pagination-wrapper">
        <el-pagination
            v-model:current-page="currentPage"
            :page-size="pageSize"
            :total="todos.length"
            background
            layout="prev, pager, next, total"
        />
      </div>
    </el-card>

    <!-- 新增/编辑待办对话框 -->
    <el-dialog
        v-model="dialogVisible"
        :title="isEditing ? '编辑待办' : '新增待办'"
        width="550px"
        destroy-on-close
    >
      <el-form :model="form" label-width="80px">
        <el-form-item label="任务" required>
          <el-input v-model="form.task" placeholder="输入任务描述"/>
        </el-form-item>
        <el-form-item label="类型">
          <el-select v-model="form.type" placeholder="选择类型" style="width: 100%">
            <el-option label="🚀 短期目标" value="short-term"/>
            <el-option label="📅 中期目标" value="mid-term"/>
            <el-option label="🏔️ 长期目标" value="long-term"/>
          </el-select>
        </el-form-item>
        <el-form-item label="优先级">
          <el-select v-model="form.priority" placeholder="选择优先级" style="width: 100%">
            <el-option label="高优先级" value="high"/>
            <el-option label="中优先级" value="medium"/>
            <el-option label="低优先级" value="low"/>
          </el-select>
        </el-form-item>
        <el-form-item label="进度">
          <el-slider v-model="form.progress" :min="0" :max="100" show-input/>
        </el-form-item>
        <el-form-item label="图标">
          <el-input v-model="form.icon" placeholder="Emoji、URL 或 SVG 代码"/>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="form.status" placeholder="选择可见状态" style="width: 100%">
            <el-option label="活跃" value="active"/>
            <el-option label="隐藏" value="inactive"/>
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
import {computed, onMounted, ref} from 'vue'
import {ElMessage, ElMessageBox} from 'element-plus'
import {Delete, Refresh} from '@element-plus/icons-vue'
import axios from 'axios'

const loading = ref(false)
const submitting = ref(false)
const todos = ref([])
const dialogVisible = ref(false)
const isEditing = ref(false)
const editingId = ref(null)
const currentPage = ref(1)
const pageSize = ref(10)

const typeTextMap = {'short-term': '短期', 'mid-term': '中期', 'long-term': '长期'}
const typeTagMap = {'short-term': 'danger', 'mid-term': 'warning', 'long-term': 'success'}
const priorityTagMap = {high: 'danger', medium: 'warning', low: 'success'}

const defaultForm = () => ({
  task: '',
  type: 'short-term',
  priority: 'medium',
  progress: 0,
  icon: '',
  status: 'active',
  completed: false,
})
const form = ref(defaultForm())

const paginatedTodos = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  return todos.value.slice(start, start + pageSize.value)
})

const iconPreview = (icon) => {
  if (!icon) return ''
  if (icon.startsWith('<svg')) return `<span style="display:inline-flex;width:20px;height:20px;">${icon}</span>`
  if (icon.startsWith('http') || icon.startsWith('/')) return `<img src="${icon}" alt="" style="width:20px;height:20px;object-fit:contain;" />`
  return icon
}

const fetchTodos = async () => {
  loading.value = true
  try {
    const res = await axios.get('/api/admin/todos')
    todos.value = res.data || []
  } catch (error) {
    console.error('获取待办列表失败:', error)
    ElMessage.error('获取待办列表失败')
  } finally {
    loading.value = false
  }
}

const openCreateDialog = () => {
  isEditing.value = false
  editingId.value = null
  form.value = defaultForm()
  dialogVisible.value = true
}

const openEditDialog = (todo) => {
  isEditing.value = true
  editingId.value = todo.id
  form.value = {
    task: todo.task,
    type: todo.type || 'short-term',
    priority: todo.priority || 'medium',
    progress: todo.progress || 0,
    icon: todo.icon || '',
    status: todo.status || 'active',
    completed: todo.completed || false,
  }
  dialogVisible.value = true
}

const submitTodo = async () => {
  if (!form.value.task) {
    ElMessage.warning('请填写任务描述')
    return
  }
  submitting.value = true
  try {
    const payload = {...form.value}
    if (!isEditing.value) delete payload.completed
    if (isEditing.value) {
      await axios.put(`/api/todos/${editingId.value}`, payload)
      ElMessage.success('待办已更新')
    } else {
      await axios.post('/api/todos', payload)
      ElMessage.success('待办已创建')
    }
    dialogVisible.value = false
    await refreshTodos()
  } catch (error) {
    console.error('提交待办失败:', error)
    ElMessage.error('提交待办失败')
  } finally {
    submitting.value = false
  }
}

const toggleCompleted = async (todo) => {
  try {
    await axios.put(`/api/todos/${todo.id}`, {completed: !todo.completed})
    ElMessage.success(todo.completed ? '已标记为未完成' : '已标记为完成')
    await refreshTodos()
  } catch (error) {
    console.error('更新状态失败:', error)
    ElMessage.error('更新状态失败')
  }
}

const deleteTodo = async (todo) => {
  try {
    await ElMessageBox.confirm('确定要删除这条待办吗？', '提示', {type: 'warning'})
    await axios.delete(`/api/todos/${todo.id}`)
    ElMessage.success('删除成功')
    await refreshTodos()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除待办失败:', error)
      ElMessage.error('删除待办失败')
    }
  }
}

const refreshTodos = async () => {
  await fetchTodos()
}

onMounted(() => {
  refreshTodos()
})
</script>

<style scoped>
.todo-management {
  padding: 20px;
  background: #f8f9fa;
  min-height: 100vh;
}

.action-bar {
  margin-bottom: 20px;
}

.action-buttons {
  display: flex;
  gap: 12px;
}

.list-card {
  border-radius: 12px;
  border: 1px solid #e1e8ed;
}

.text-muted {
  color: #909399;
  font-size: 0.85em;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  padding: 20px 0;
  border-top: 1px solid #ebeef5;
}

@media (max-width: 768px) {
  .todo-management {
    padding: 15px;
  }
}
</style>
