<template>
  <div class="admin-page">
    <div class="admin-header">
      <h2 class="admin-title">资源管理</h2>
    </div>

    <!-- Tabs -->
    <div class="flex gap-2 mb-6">
      <button :class="['px-4 py-2 rounded-xl text-sm font-medium transition-all', activeTab === 'books' ? 'bg-accent text-white shadow-sm' : 'bg-white text-secondary border border-gray-200 hover:border-accent/30']" @click="activeTab = 'books'">图书管理</button>
      <button :class="['px-4 py-2 rounded-xl text-sm font-medium transition-all', activeTab === 'figures' ? 'bg-accent text-white shadow-sm' : 'bg-white text-secondary border border-gray-200 hover:border-accent/30']" @click="activeTab = 'figures'">图片管理</button>
    </div>

    <!-- Books Tab -->
    <template v-if="activeTab === 'books'">
      <div class="flex gap-2 mb-4">
        <el-button type="primary" @click="showUploadBookDialog = true">上传图书</el-button>
        <el-button :icon="Refresh" circle @click="refreshBooks"/>
      </div>
      <div class="admin-filter">
        <div class="flex items-center justify-between mb-4">
          <span class="text-sm font-semibold text-primary">筛选</span>
          <el-button link size="small" @click="resetBookFilters">重置</el-button>
        </div>
        <div class="flex flex-wrap gap-4 items-center">
          <el-select v-model="bookFilter.tags" :multiple-limit="3" allow-create filterable multiple placeholder="标签" style="width: 240px"><el-option v-for="t in allBookTags" :key="t" :label="t" :value="t"/></el-select>
          <el-input v-model="bookFilter.title" clearable placeholder="标题" style="width: 180px"/>
          <el-select v-model="bookFilter.status" placeholder="状态" style="width: 110px"><el-option label="全部" value=""/><el-option label="已发布" value="published"/><el-option label="草稿" value="draft"/><el-option label="已回收" value="recycled"/></el-select>
        </div>
      </div>
      <p class="text-xs text-secondary/60 mb-4">共 {{ filteredBooks.length }} 本图书</p>
      <div v-if="paginatedBooks.length" class="admin-grid">
        <div v-for="b in paginatedBooks" :key="b.id" class="admin-card">
          <div class="flex items-start justify-between mb-2">
            <h3 class="font-bold text-sm text-primary truncate flex-1 mr-2">{{ b.title }}</h3>
            <span :class="['status-badge', b.status]">{{ statusText(b.status) }}</span>
          </div>
          <p v-if="b.description" class="text-xs text-secondary line-clamp-2 mb-2">{{ b.description }}</p>
          <p v-if="b.filename" class="text-xs text-secondary/50 font-mono mb-2">{{ b.filename }}</p>
          <div v-if="b.tags?.length" class="flex flex-wrap gap-1 mb-3"><span v-for="t in b.tags.slice(0, 3)" :key="t" class="tag-pill text-[11px]">{{ t }}</span></div>
          <div class="pt-3 border-t border-gray-100 flex items-center justify-between">
            <el-select :model-value="b.status" size="small" style="width: 90px" @change="(v) => updateBookStatus(b, v)"><el-option label="草稿" value="draft"/><el-option label="已发布" value="published"/><el-option label="已回收" value="recycled"/></el-select>
            <div class="flex gap-2">
              <el-button size="small" @click="handleEditBook(b)">编辑</el-button>
              <el-button size="small" type="danger" @click="deleteBook(b)">删除</el-button>
            </div>
          </div>
        </div>
      </div>
      <div v-else class="admin-empty"><p>暂无图书</p></div>
      <div v-if="filteredBooks.length > pageSize" class="flex justify-center mt-6"><el-pagination v-model:current-page="bookPage" :page-size="pageSize" :total="filteredBooks.length" background layout="prev, pager, next"/></div>
    </template>

    <!-- Figures Tab -->
    <template v-if="activeTab === 'figures'">
      <div class="flex gap-2 mb-4">
        <el-button type="primary" @click="showUploadFigureDialog = true">上传图片</el-button>
        <el-button :icon="Refresh" circle @click="refreshFigures"/>
      </div>
      <div class="admin-filter">
        <div class="flex items-center justify-between mb-4">
          <span class="text-sm font-semibold text-primary">筛选</span>
          <el-button link size="small" @click="resetFigureFilters">重置</el-button>
        </div>
        <div class="flex flex-wrap gap-4 items-center">
          <el-select v-model="figureFilter.tags" :multiple-limit="3" allow-create filterable multiple placeholder="标签" style="width: 240px"><el-option v-for="t in allFigureTags" :key="t" :label="t" :value="t"/></el-select>
          <el-input v-model="figureFilter.title" clearable placeholder="标题" style="width: 180px"/>
          <el-select v-model="figureFilter.status" placeholder="状态" style="width: 110px"><el-option label="全部" value=""/><el-option label="已发布" value="published"/><el-option label="草稿" value="draft"/><el-option label="已回收" value="recycled"/></el-select>
        </div>
      </div>
      <p class="text-xs text-secondary/60 mb-4">共 {{ filteredFigures.length }} 张图片</p>
      <div v-if="paginatedFigures.length" class="admin-grid">
        <div v-for="f in paginatedFigures" :key="f.id" class="admin-card">
          <div class="flex items-start justify-between mb-2">
            <h3 class="font-bold text-sm text-primary truncate flex-1 mr-2">{{ f.title }}</h3>
            <span :class="['status-badge', f.status]">{{ statusText(f.status) }}</span>
          </div>
          <p v-if="f.description" class="text-xs text-secondary line-clamp-2 mb-2">{{ f.description }}</p>
          <a v-if="f.url" :href="f.url" target="_blank" class="text-xs text-accent hover:underline truncate block mb-2">{{ f.url }}</a>
          <div v-if="f.tags?.length" class="flex flex-wrap gap-1 mb-3"><span v-for="t in f.tags.slice(0, 3)" :key="t" class="tag-pill text-[11px]">{{ t }}</span></div>
          <div class="pt-3 border-t border-gray-100 flex items-center justify-between">
            <el-select :model-value="f.status" size="small" style="width: 90px" @change="(v) => updateFigureStatus(f, v)"><el-option label="草稿" value="draft"/><el-option label="已发布" value="published"/><el-option label="已回收" value="recycled"/></el-select>
            <div class="flex gap-2">
              <el-button size="small" @click="handleEditFigure(f)">编辑</el-button>
              <el-button size="small" type="danger" @click="deleteFigure(f)">删除</el-button>
            </div>
          </div>
        </div>
      </div>
      <div v-else class="admin-empty"><p>暂无图片</p></div>
      <div v-if="filteredFigures.length > pageSize" class="flex justify-center mt-6"><el-pagination v-model:current-page="figurePage" :page-size="pageSize" :total="filteredFigures.length" background layout="prev, pager, next"/></div>
    </template>

    <!-- Dialogs (reusing existing) -->
    <UploadBookDialog v-model="showUploadBookDialog" @upload-success="refreshBooks"/>
    <EditBookDialog v-model="showEditBookDialog" :book="currentEditBook" @save-success="refreshBooks"/>
    <UploadFigureDialog v-model="showUploadFigureDialog" @upload-success="refreshFigures"/>
    <EditFigureDialog v-model="showEditFigureDialog" :figure="currentEditFigure" @save-success="refreshFigures"/>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Refresh } from '@element-plus/icons-vue'
import axios from 'axios'
import UploadBookDialog from '@/components/Admin/ResourceManagement/UploadBookDialog.vue'
import EditBookDialog from '@/components/Admin/ResourceManagement/EditBookDialog.vue'
import UploadFigureDialog from '@/components/Admin/ResourceManagement/UploadFigureDialog.vue'
import EditFigureDialog from '@/components/Admin/ResourceManagement/EditFigureDialog.vue'

const activeTab = ref('books')
const pageSize = 12

// Books
const books = ref([])
const allBookTags = ref([])
const bookPage = ref(1)
const bookFilter = reactive({ tags: [], title: '', status: '' })
const showUploadBookDialog = ref(false)
const showEditBookDialog = ref(false)
const currentEditBook = ref(null)

const filteredBooks = computed(() => {
  let arr = books.value
  if (bookFilter.tags.length) arr = arr.filter(b => b.tags?.length && bookFilter.tags.every(t => b.tags.includes(t)))
  if (bookFilter.title) arr = arr.filter(b => b.title?.includes(bookFilter.title))
  if (bookFilter.status) arr = arr.filter(b => b.status === bookFilter.status)
  return arr
})
const paginatedBooks = computed(() => filteredBooks.value.slice((bookPage.value - 1) * pageSize, bookPage.value * pageSize))
watch([() => bookFilter.tags, () => bookFilter.title, () => bookFilter.status], () => { bookPage.value = 1 }, { deep: true })
const resetBookFilters = () => { bookFilter.tags = []; bookFilter.title = ''; bookFilter.status = ''; bookPage.value = 1 }

const fetchBooks = async () => { try { books.value = (await axios.get('/api/admin/books')).data } catch { ElMessage.error('获取图书失败') } }
const fetchBookTags = async () => { try { allBookTags.value = (await axios.get('/api/book-tags')).data?.tags || [] } catch {} }
const refreshBooks = async () => { await fetchBooks(); await fetchBookTags() }
const handleEditBook = (b) => { currentEditBook.value = b; showEditBookDialog.value = true }
const deleteBook = async (b) => { try { await ElMessageBox.confirm('确定删除？', '提示', { type: 'warning' }); await axios.delete(`/api/books/${b.id}`); ElMessage.success('删除成功'); refreshBooks() } catch (e) { if (e !== 'cancel') ElMessage.error('删除失败') } }
const updateBookStatus = async (b, s) => { if (b.status === s) return; try { await axios.patch(`/api/books/${b.id}/status`, { status: s }); b.status = s; ElMessage.success('状态已更新') } catch { ElMessage.error('更新失败'); refreshBooks() } }

// Figures
const figures = ref([])
const allFigureTags = ref([])
const figurePage = ref(1)
const figureFilter = reactive({ tags: [], title: '', status: '' })
const showUploadFigureDialog = ref(false)
const showEditFigureDialog = ref(false)
const currentEditFigure = ref(null)

const filteredFigures = computed(() => {
  let arr = figures.value
  if (figureFilter.tags.length) arr = arr.filter(f => f.tags?.length && figureFilter.tags.every(t => f.tags.includes(t)))
  if (figureFilter.title) arr = arr.filter(f => f.title?.includes(figureFilter.title))
  if (figureFilter.status) arr = arr.filter(f => f.status === figureFilter.status)
  return arr
})
const paginatedFigures = computed(() => filteredFigures.value.slice((figurePage.value - 1) * pageSize, figurePage.value * pageSize))
watch([() => figureFilter.tags, () => figureFilter.title, () => figureFilter.status], () => { figurePage.value = 1 }, { deep: true })
const resetFigureFilters = () => { figureFilter.tags = []; figureFilter.title = ''; figureFilter.status = ''; figurePage.value = 1 }

const fetchFigures = async () => { try { figures.value = (await axios.get('/api/admin/figures')).data } catch { ElMessage.error('获取图片失败') } }
const fetchFigureTags = async () => { try { allFigureTags.value = (await axios.get('/api/figure-tags')).data?.tags || [] } catch {} }
const refreshFigures = async () => { await fetchFigures(); await fetchFigureTags() }
const handleEditFigure = (f) => { currentEditFigure.value = f; showEditFigureDialog.value = true }
const deleteFigure = async (f) => { try { await ElMessageBox.confirm('确定删除？', '提示', { type: 'warning' }); await axios.delete(`/api/figures/${f.id}`); ElMessage.success('删除成功'); refreshFigures() } catch (e) { if (e !== 'cancel') ElMessage.error('删除失败') } }
const updateFigureStatus = async (f, s) => { if (f.status === s) return; try { await axios.patch(`/api/figures/${f.id}/status`, { status: s }); f.status = s; ElMessage.success('状态已更新') } catch { ElMessage.error('更新失败'); refreshFigures() } }

const statusText = (s) => ({ published: '已发布', draft: '草稿', recycled: '已回收' }[s] || '未知')

onMounted(() => { refreshBooks(); refreshFigures() })
</script>