<template>
  <div class="diary-management">
    <!-- 操作栏 -->
    <div class="action-bar">
      <div class="action-buttons">
        <el-button type="primary" @click="openCreateDialog">新增日记</el-button>
        <el-button :icon="Refresh" circle @click="refreshDiaries"/>
      </div>
    </div>

    <!-- 日记列表 -->
    <el-card shadow="never" class="list-card">
      <el-table :data="paginatedDiaries" v-loading="loading" stripe style="width: 100%">
        <el-table-column prop="id" label="ID" width="70" sortable/>
        <el-table-column prop="date" label="日期" width="180">
          <template #default="{ row }">
            {{ formatDate(row.date) }}
          </template>
        </el-table-column>
        <el-table-column prop="mood" label="心情" width="100">
          <template #default="{ row }">
            <span>{{ moodMap[row.mood] || '😐' }} {{ row.mood || '-' }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="weather" label="天气" width="100">
          <template #default="{ row }">
            <span>{{ weatherMap[row.weather] || '🌤️' }} {{ row.weather || '-' }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="content" label="内容" min-width="250" show-overflow-tooltip/>
        <el-table-column prop="images" label="图片" width="80">
          <template #default="{ row }">
            <el-tag v-if="row.images && row.images.length" size="small" type="info">
              {{ row.images.length }}张
            </el-tag>
            <span v-else class="text-muted">无</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="160" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="openEditDialog(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="deleteDiary(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div v-if="diaries.length > pageSize" class="pagination-wrapper">
        <el-pagination
            v-model:current-page="currentPage"
            :page-size="pageSize"
            :total="diaries.length"
            background
            layout="prev, pager, next, total"
        />
      </div>
    </el-card>

    <!-- 新增/编辑日记对话框 -->
    <el-dialog
        v-model="dialogVisible"
        :title="isEditing ? '编辑日记' : '新增日记'"
        width="600px"
        destroy-on-close
    >
      <el-form :model="form" label-width="80px">
        <el-form-item label="日期" required>
          <el-date-picker
              v-model="form.date"
              type="datetime"
              placeholder="选择日期时间"
              format="YYYY-MM-DD HH:mm"
              value-format="YYYY-MM-DDTHH:mm"
              style="width: 100%"
          />
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
          <div class="image-urls">
            <div v-for="(img, index) in form.images" :key="index" class="image-url-row">
              <el-input v-model="form.images[index]" placeholder="图片 URL"/>
              <el-button :icon="Delete" circle size="small" @click="form.images.splice(index, 1)"/>
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
import {computed, onMounted, ref} from 'vue'
import {ElMessage, ElMessageBox} from 'element-plus'
import {Delete, Refresh} from '@element-plus/icons-vue'
import axios from 'axios'

const loading = ref(false)
const submitting = ref(false)
const diaries = ref([])
const dialogVisible = ref(false)
const isEditing = ref(false)
const editingId = ref(null)
const currentPage = ref(1)
const pageSize = ref(10)

const moodMap = {
  happy: '😊', relieved: '😌', sad: '😢', angry: '😠',
  neutral: '😐', excited: '🤩', tired: '😫',
}
const weatherMap = {
  sunny: '☀️', cloudy: '☁️', rainy: '🌧️', snowy: '❄️', windy: '💨',
}

const defaultForm = () => ({
  date: '',
  content: '',
  mood: null,
  weather: null,
  images: [],
})
const form = ref(defaultForm())

const paginatedDiaries = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  return diaries.value.slice(start, start + pageSize.value)
})

const formatDate = (dateStr) => {
  const d = new Date(dateStr)
  if (isNaN(d.getTime())) return dateStr
  const pad = (n) => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}`
}

const fetchDiaries = async () => {
  loading.value = true
  try {
    const res = await axios.get('/api/diaries')
    diaries.value = (res.data || []).sort((a, b) => new Date(b.date) - new Date(a.date))
  } catch (error) {
    console.error('获取日记列表失败:', error)
    ElMessage.error('获取日记列表失败')
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

const openEditDialog = (diary) => {
  isEditing.value = true
  editingId.value = diary.id
  form.value = {
    date: diary.date,
    content: diary.content,
    mood: diary.mood || null,
    weather: diary.weather || null,
    images: diary.images ? [...diary.images] : [],
  }
  dialogVisible.value = true
}

const submitDiary = async () => {
  if (!form.value.date || !form.value.content) {
    ElMessage.warning('请填写日期和内容')
    return
  }
  submitting.value = true
  try {
    const payload = {
      ...form.value,
      images: form.value.images.filter(url => url.trim()),
    }
    if (isEditing.value) {
      await axios.put(`/api/diaries/${editingId.value}`, payload)
      ElMessage.success('日记已更新')
    } else {
      await axios.post('/api/diaries', payload)
      ElMessage.success('日记已创建')
    }
    dialogVisible.value = false
    await refreshDiaries()
  } catch (error) {
    console.error('提交日记失败:', error)
    ElMessage.error('提交日记失败')
  } finally {
    submitting.value = false
  }
}

const deleteDiary = async (diary) => {
  try {
    await ElMessageBox.confirm('确定要删除这条日记吗？', '提示', {type: 'warning'})
    await axios.delete(`/api/diaries/${diary.id}`)
    ElMessage.success('删除成功')
    await refreshDiaries()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除日记失败:', error)
      ElMessage.error('删除日记失败')
    }
  }
}

const refreshDiaries = async () => {
  await fetchDiaries()
}

onMounted(() => {
  refreshDiaries()
})
</script>

<style scoped>
.diary-management {
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

.image-urls {
  display: flex;
  flex-direction: column;
  gap: 8px;
  width: 100%;
}

.image-url-row {
  display: flex;
  gap: 8px;
  align-items: center;
}

.image-url-row .el-input {
  flex: 1;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  padding: 20px 0;
  border-top: 1px solid #ebeef5;
}

@media (max-width: 768px) {
  .diary-management {
    padding: 15px;
  }
}
</style>
