<template>
  <div class="admin-page">
    <div class="admin-header">
      <h2 class="admin-title">日记管理</h2>
      <div class="flex gap-2">
        <el-button type="primary" @click="openCreate">新增日记</el-button>
        <el-button :icon="Refresh" circle @click="refreshDiaries"/>
      </div>
    </div>

    <p class="text-xs text-secondary/60 mb-4">共 {{ diaries.length }} 条日记</p>

    <div v-if="paginatedDiaries.length" class="admin-grid">
      <div v-for="d in paginatedDiaries" :key="d.id" class="admin-card">
        <div class="flex items-start justify-between mb-2">
          <span class="text-xs text-secondary/60 tabular-nums">{{ formatDate(d.date) }}</span>
          <div class="flex gap-1.5">
            <span v-if="d.mood" class="text-sm">{{ moodMap[d.mood] || '😐' }}</span>
            <span v-if="d.weather" class="text-sm">{{ weatherMap[d.weather] || '🌤️' }}</span>
          </div>
        </div>
        <p class="text-sm text-primary leading-relaxed line-clamp-3 mb-3">{{ d.content }}</p>
        <div v-if="d.images && d.images.length" class="mb-3">
          <span class="tag-pill text-[11px]">📷 {{ d.images.length }}张图片</span>
        </div>
        <div class="pt-3 border-t border-gray-100 flex justify-end gap-2">
          <el-button size="small" @click="openEdit(d)">编辑</el-button>
          <el-button size="small" type="danger" @click="deleteDiary(d)">删除</el-button>
        </div>
      </div>
    </div>
    <div v-else class="text-center py-12 text-secondary/60">
      <p class="text-lg mb-1">📔</p>
      <p class="text-sm">暂无日记</p>
    </div>

    <div v-if="diaries.length > pageSize" class="flex justify-center mt-6">
      <el-pagination v-model:current-page="currentPage" :page-size="pageSize" :total="diaries.length" background layout="prev, pager, next"/>
    </div>

    <!-- Dialog -->
    <el-dialog v-model="dialogVisible" :title="isEditing ? '编辑日记' : '新增日记'" width="560px" destroy-on-close>
      <el-form :model="form" label-width="80px">
        <el-form-item label="日期" required>
          <el-date-picker v-model="form.date" type="datetime" placeholder="选择日期时间" format="YYYY-MM-DD HH:mm" value-format="YYYY-MM-DDTHH:mm" style="width: 100%"/>
        </el-form-item>
        <el-form-item label="内容" required>
          <el-input v-model="form.content" type="textarea" :rows="5" placeholder="写点什么..."/>
        </el-form-item>
        <el-form-item label="心情">
          <el-select v-model="form.mood" placeholder="选择心情" clearable style="width: 100%">
            <el-option v-for="(emoji, key) in moodMap" :key="key" :label="`${emoji} ${key}`" :value="key"/>
          </el-select>
        </el-form-item>
        <el-form-item label="天气">
          <el-select v-model="form.weather" placeholder="选择天气" clearable style="width: 100%">
            <el-option v-for="(emoji, key) in weatherMap" :key="key" :label="`${emoji} ${key}`" :value="key"/>
          </el-select>
        </el-form-item>
        <el-form-item label="图片">
          <div class="w-full space-y-2">
            <div v-for="(img, i) in form.images" :key="i" class="flex gap-2 items-center">
              <el-input v-model="form.images[i]" placeholder="图片 URL"/>
              <el-button :icon="Delete" circle size="small" @click="form.images.splice(i, 1)"/>
            </div>
            <el-button size="small" @click="form.images.push('')">+ 添加图片 URL</el-button>
          </div>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="submitDiary">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Delete, Refresh } from '@element-plus/icons-vue'
import axios from 'axios'

const diaries = ref([])
const currentPage = ref(1)
const pageSize = 12
const dialogVisible = ref(false)
const isEditing = ref(false)
const editingId = ref(null)
const submitting = ref(false)

const moodMap = { happy: '😊', relieved: '😌', sad: '😢', angry: '😠', neutral: '😐', excited: '🤩', tired: '😫' }
const weatherMap = { sunny: '☀️', cloudy: '☁️', rainy: '🌧️', snowy: '❄️', windy: '💨' }

const defaultForm = () => ({ date: '', content: '', mood: null, weather: null, images: [] })
const form = ref(defaultForm())

const paginatedDiaries = computed(() => diaries.value.slice((currentPage.value - 1) * pageSize, currentPage.value * pageSize))

const formatDate = (d) => {
  const date = new Date(d)
  if (isNaN(date.getTime())) return d
  const pad = n => String(n).padStart(2, '0')
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())} ${pad(date.getHours())}:${pad(date.getMinutes())}`
}

const fetchDiaries = async () => {
  try { diaries.value = ((await axios.get('/api/diaries')).data || []).sort((a, b) => new Date(b.date) - new Date(a.date)) }
  catch { ElMessage.error('获取日记失败') }
}

const refreshDiaries = () => fetchDiaries()
const openCreate = () => { isEditing.value = false; editingId.value = null; form.value = defaultForm(); dialogVisible.value = true }
const openEdit = (d) => {
  isEditing.value = true; editingId.value = d.id
  form.value = { date: d.date, content: d.content, mood: d.mood || null, weather: d.weather || null, images: d.images ? [...d.images] : [] }
  dialogVisible.value = true
}

const submitDiary = async () => {
  if (!form.value.date || !form.value.content) { ElMessage.warning('请填写日期和内容'); return }
  submitting.value = true
  try {
    const payload = { ...form.value, images: form.value.images.filter(u => u.trim()) }
    if (isEditing.value) { await axios.put(`/api/diaries/${editingId.value}`, payload); ElMessage.success('已更新') }
    else { await axios.post('/api/diaries', payload); ElMessage.success('已创建') }
    dialogVisible.value = false; refreshDiaries()
  } catch { ElMessage.error('提交失败') }
  finally { submitting.value = false }
}

const deleteDiary = async (d) => {
  try {
    await ElMessageBox.confirm('确定删除？', '提示', { type: 'warning' })
    await axios.delete(`/api/diaries/${d.id}`); ElMessage.success('删除成功'); refreshDiaries()
  } catch (e) { if (e !== 'cancel') ElMessage.error('删除失败') }
}

onMounted(() => refreshDiaries())
</script>
