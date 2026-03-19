<template>
  <div class="page-container">
    <div v-if="articleNotFound" class="not-found">
      <h1>404 - 文章未找到</h1>
      <p>抱歉，您要查找的文章不存在或链接已更改。</p>
      <router-link to="/articles">返回文章列表</router-link>
    </div>
    <div v-else class="content-layout">

      <!-- 主内容区 -->
      <main class="main-content">
        <header v-if="articleTitle" class="article-header">
          <h1 class="article-title">{{ articleTitle }}</h1>
          <div class="article-meta">
            <span v-if="articleDataRef?.date" class="meta-item">
              <el-icon><Calendar /></el-icon> {{ formatDate(articleDataRef.date) }}
            </span>
            <span v-if="articleDataRef?.category" class="meta-item">
              <el-icon><Folder /></el-icon> {{ articleDataRef.category }}
            </span>
            <span v-if="articleDataRef?.tags && articleDataRef.tags.length" class="meta-item tags">
              <el-icon><CollectionTag /></el-icon>
              <el-tag v-for="tag in articleDataRef.tags" :key="tag" size="small" class="tag-item">{{ tag }}</el-tag>
            </span>
          </div>
        </header>

        <MarkdownRenderer
          v-if="rawMarkdown"
          :content="rawMarkdown"
          :category="articleDataRef?.category || ''"
          @headings-extracted="onHeadingsExtracted"
        />
      </main>

      <!-- 右侧文章大纲 -->
      <aside class="sidebar-right" :class="{ collapsed: rightCollapsed }">
        <div v-show="!rightCollapsed" class="sidebar-content">
          <Outline 
            v-if="headings.length" 
            :active-id="activeHeadingId" 
            :outline="headings"
            :show-collapse-button="true"
            @collapse="toggleRight"
          />
          <el-empty v-else description="暂无大纲" />
        </div>
      </aside>

      <!-- 右侧展开按钮 -->
      <el-button 
        v-if="rightCollapsed" 
        class="expand-btn expand-btn-right" 
        circle 
        @click="toggleRight"
      >
        <el-icon>
          <ArrowLeft />
        </el-icon>
      </el-button>
    </div>
  </div>
</template>

<script setup>
import { nextTick, onMounted, onUnmounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import Outline from '@/components/Main/Outline.vue'
import MarkdownRenderer from '@/components/Main/Article/MarkdownRenderer.vue'
import { ArrowLeft, Calendar, Folder, CollectionTag } from '@element-plus/icons-vue'

const route = useRoute()
const articleTitle = ref('')
const articleNotFound = ref(false)
const headings = ref([])
const activeHeadingId = ref('')
const rightCollapsed = ref(false)
const rawMarkdown = ref('')
let observer = null

const articleDataRef = ref(null)

const API_BASE_URL = '/api'

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
}

const toggleRight = () => {
  rightCollapsed.value = !rightCollapsed.value
}

const onHeadingsExtracted = (extractedHeadings) => {
  headings.value = extractedHeadings
  nextTick(() => setupIntersectionObserver())
}

const setupIntersectionObserver = () => {
  if (observer) {
    observer.disconnect()
  }

  const headingElements = document.querySelectorAll('.markdown-body h1, .markdown-body h2, .markdown-body h3, .markdown-body h4, .markdown-body h5, .markdown-body h6')

  observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        activeHeadingId.value = entry.target.id
      }
    })
  }, {
    rootMargin: '0px 0px -80% 0px',
    threshold: 0
  })

  headingElements.forEach(el => observer.observe(el))
}

const fetchArticle = async () => {
  articleNotFound.value = false
  rawMarkdown.value = ''
  articleTitle.value = ''
  headings.value = []
  articleDataRef.value = null

  const slugParam = route.params.slug
  const slug = Array.isArray(slugParam) ? slugParam.join('/') : slugParam
  if (!slug) {
    articleNotFound.value = true
    return
  }

  try {
    const response = await axios.get(`${API_BASE_URL}/articles/${slug}`, {
      timeout: 10000,
      headers: { 'Accept': 'application/json' }
    })
    const articleData = response.data

    if (articleData) {
      articleDataRef.value = articleData
      articleTitle.value = articleData.title

      if (!articleData.content) {
        console.warn('文章内容为空')
        articleNotFound.value = true
        return
      }

      // 后端API已经剥离了YAML frontmatter，直接使用
      rawMarkdown.value = articleData.content
      console.log(`成功加载文章: ${articleData.title}`)
    } else {
      articleNotFound.value = true
    }
  } catch (error) {
    console.error('获取文章信息失败:', error)
    articleNotFound.value = true
  }
}

onMounted(fetchArticle)
watch(() => route.params.slug, fetchArticle)

onUnmounted(() => {
  if (observer) {
    observer.disconnect()
  }
})
</script>

<style scoped>
.page-container {
  width: 100%;
  margin-top: 20px;
  margin-bottom: 40px;
  padding: 0;
}

.content-layout {
  display: flex;
  gap: 24px;
  align-items: flex-start;
  justify-content: center;
}

.main-content {
  flex: 1;
  min-width: 0;
  max-width: 900px;
}

.sidebar-right {
  width: 240px;
  flex-shrink: 0;
  align-self: stretch;
  transition: width 0.3s ease;
}

.sidebar-right.collapsed {
  width: 0;
  overflow: hidden;
}

.sidebar-content {
  position: sticky;
  top: 100px;
  max-height: calc(100vh - 120px);
  overflow-y: auto;
  overflow-x: hidden;
  width: 240px;
}

/* article header styles */
.article-header {
  margin-bottom: 2rem;
  padding: 1.5rem 2.5rem;
  background-color: var(--color-background, #FAFAFA);
  border-radius: 12px;
  box-shadow: var(--shadow-md);
  border: 1px solid #E2E8F0;
}

.article-title {
  font-size: 2.2rem;
  font-weight: 700;
  color: var(--color-primary, #18181B);
  margin-bottom: 1.2rem;
  line-height: 1.3;
  margin-top: 0;
}

.article-meta {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 1.5rem;
  color: #64748B;
  font-size: 0.95rem;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.tag-item {
  margin-right: 0.4rem;
}
.tag-item:last-child {
  margin-right: 0;
}

.not-found {
  text-align: center;
  padding: 40px;
  color: #606266;
}

/* 确保大纲组件不产生额外滚动条 */
.sidebar-content :deep(.outline-container) {
  overflow: visible !important;
  max-height: none !important;
  height: auto !important;
}

.sidebar-content :deep(.el-scrollbar) {
  height: auto !important;
}

.sidebar-content :deep(.el-scrollbar__wrap) {
  overflow: visible !important;
  max-height: none !important;
}

.sidebar-content :deep(.el-scrollbar__view) {
  overflow: visible !important;
}

/* sidebar-content 内部滚动 */
.sidebar-content {
  overflow-y: auto !important;
  overflow-x: hidden !important;
  scrollbar-width: thin;
}

.sidebar-content::-webkit-scrollbar {
  width: 6px !important;
  display: block !important;
}

.sidebar-content::-webkit-scrollbar-track {
  background: transparent;
}

.sidebar-content::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 3px;
}

.sidebar-content::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 0, 0, 0.3);
}

.sidebar-content > * {
  overflow: visible !important;
  max-height: none !important;
}

.sidebar-content :deep(div:not(.sidebar-content)) {
  scrollbar-width: none !important;
}

.sidebar-content :deep(div:not(.sidebar-content)::-webkit-scrollbar) {
  display: none !important;
}

/* 展开按钮样式 */
.expand-btn {
  position: fixed;
  top: 50vh;
  transform: translateY(-50%);
  z-index: 100;
  width: 36px;
  height: 36px;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.15);
  background-color: var(--el-color-primary);
  color: white;
  border: none;
}

.expand-btn:hover {
  background-color: var(--el-color-primary-dark-2);
}

.expand-btn-right {
  right: 20px;
}

/* 响应式布局 */
@media (max-width: 1024px) {
  .content-layout {
    flex-direction: column;
    align-items: stretch;
  }
  
  .sidebar-right,
  .sidebar-right.collapsed {
    width: 100%;
  }
  
  .sidebar-content {
    position: static;
    max-height: none;
    width: 100% !important;
  }
  
  .expand-btn {
    position: relative;
    top: auto;
    transform: none;
    margin: 12px auto;
  }
}

@media (max-width: 768px) {
  .page-container {
    padding: 0 15px;
  }
}

@media (max-width: 480px) {
  .page-container {
    padding: 0 10px;
  }
}
</style>
