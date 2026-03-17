<template>
  <div class="admin-page">
    <div class="admin-header">
      <h2 class="admin-title">文章管理</h2>
      <div class="flex gap-2">
        <el-button type="primary" @click="openUpload">上传文章</el-button>
        <el-button :icon="Refresh" circle @click="refreshArticles"/>
      </div>
    </div>

    <ArticleFilterBar :filters="filterForm" :sort-order="sortOrder" @reset="resetFilters" @update:category="filterForm.category = $event" @update:title="filterForm.title = $event" @update:status="filterForm.status = $event" @update:sort-order="sortOrder = $event"/>
    <p class="text-xs text-secondary/60 mb-4">共 {{ sortedArticles.length }} 篇文章</p>

    <ArticleGrid :articles="paginatedArticles" @edit="openEdit" @delete="deleteArticle" @update-status="updateStatus" @visit="visitArticle"/>

    <div v-if="sortedArticles.length > pageSize" class="flex justify-center mt-6">
      <el-pagination v-model:current-page="currentPage" :page-size="pageSize" :total="sortedArticles.length" background layout="prev, pager, next"/>
    </div>

    <UploadArticleDialog v-model="showUploadDialog" @upload-success="refreshArticles"/>
    <EditArticleDialog v-model="showEditDialog" :article="editingArticle" @update-success="refreshArticles"/>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Refresh } from '@element-plus/icons-vue'
import axios from 'axios'
import ArticleFilterBar from '@/components/Admin/ArticleManagement/ArticleFilterBar.vue'
import ArticleGrid from '@/components/Admin/ArticleManagement/ArticleGrid.vue'
import UploadArticleDialog from '@/components/Admin/ArticleManagement/UploadArticleDialog.vue'
import EditArticleDialog from '@/components/Admin/ArticleManagement/EditArticleDialog.vue'

const articles = ref([])
const currentPage = ref(1)
const pageSize = 12
const sortOrder = ref('desc')
const showUploadDialog = ref(false)
const showEditDialog = ref(false)
const editingArticle = ref(null)
const filterForm = reactive({ tags: [], title: '', category: '', status: '' })

const filteredArticles = computed(() => {
  let arr = articles.value
  if (filterForm.category) arr = arr.filter(a => a.category && (a.category === filterForm.category || a.category.startsWith(filterForm.category + '/')))
  if (filterForm.tags?.length) arr = arr.filter(a => a.tags && filterForm.tags.every(t => a.tags.includes(t)))
  if (filterForm.title) arr = arr.filter(a => a.title?.includes(filterForm.title))
  if (filterForm.status) arr = arr.filter(a => a.status === filterForm.status)
  return arr
})

const sortedArticles = computed(() => {
  const arr = [...filteredArticles.value]
  arr.sort((a, b) => {
    const d1 = new Date(a.date || '1970'), d2 = new Date(b.date || '1970')
    return sortOrder.value === 'asc' ? d1 - d2 : d2 - d1
  })
  return arr
})

const paginatedArticles = computed(() => sortedArticles.value.slice((currentPage.value - 1) * pageSize, currentPage.value * pageSize))

watch([() => filterForm.tags, () => filterForm.title, () => filterForm.category, () => filterForm.status, sortOrder], () => { currentPage.value = 1 }, { deep: true })

const resetFilters = () => { Object.assign(filterForm, { tags: [], title: '', category: '', status: '' }); currentPage.value = 1 }

const fetchArticles = async () => {
  try { articles.value = (await axios.get('/api/admin/articles')).data } catch { ElMessage.error('获取文章失败') }
}

const refreshArticles = () => fetchArticles()
const openUpload = () => { showUploadDialog.value = true }
const openEdit = (a) => { editingArticle.value = { ...a }; showEditDialog.value = true }

const deleteArticle = async (a) => {
  try {
    await ElMessageBox.confirm('确定删除？', '提示', { type: 'warning' })
    await axios.delete(`/api/articles/${a.id}`)
    ElMessage.success('删除成功'); refreshArticles()
  } catch (e) { if (e !== 'cancel') ElMessage.error('删除失败') }
}

const updateStatus = async (a, s) => {
  if (a.status === s) return
  try { await axios.patch(`/api/articles/${a.id}/status`, { status: s }); a.status = s; ElMessage.success('状态已更新') }
  catch { ElMessage.error('更新失败'); refreshArticles() }
}

const visitArticle = (a) => {
  if (a.status === 'published') {
    window.open(`/article/${a.filepath || a.category || 'uncategorized'}/${a.slug || a.filename}`, '_blank')
  } else ElMessage.warning('只有已发布的文章才能访问')
}

onMounted(() => refreshArticles())
</script>
