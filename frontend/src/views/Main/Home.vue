<template>
  <div class="home-container">
    <div class="left-column">
      <ProfileCard class="profile-card-container"/>
      <Timeline class="timeline-editor-container"/>
    </div>
    <div class="right-column-content">
      <!-- GitHub热力图放在最近文章上方 -->
      <GitHubHeatmap class="github-heatmap-card"/>
      
      <el-card class="content-card">
        <template #header>
          <div class="card-header">
            <span>最近文章</span>
            <router-link class="more-link" to="/knowledge">查看全部 &gt;</router-link>
          </div>
        </template>
        <div v-loading="articlesLoading" class="card-list">
          <ArticleCard
              v-for="article in recentArticles"
              :key="article.slug"
              :article="article"
              class="list-item-card"
          />
          <el-empty v-if="!articlesLoading && recentArticles.length === 0" :image-size="60" description="暂无文章数据">
          </el-empty>
        </div>
      </el-card>

      <el-card class="content-card">
        <template #header>
          <div class="card-header">
            <span>最近项目</span>
            <router-link class="more-link" to="/projects">查看全部 &gt;</router-link>
          </div>
        </template>
        <div v-loading="projectsLoading" class="card-list">
          <ProjectCard
              v-for="project in recentProjects"
              :key="project.id"
              :project="project"
              class="list-item-card"
          />
          <el-empty v-if="!projectsLoading && recentProjects.length === 0" :image-size="60" description="暂无项目数据">
          </el-empty>
        </div>
      </el-card>

      <!-- 最新日记 -->
      <el-card v-if="latestDiary" class="content-card">
        <template #header>
          <div class="card-header">
            <span>最新日记</span>
            <router-link class="more-link" to="/diary">查看全部 &gt;</router-link>
          </div>
        </template>
        <div class="diary-preview">
          <div class="diary-meta">
            <span class="meta-item">📅 {{ formatDiaryDate(latestDiary.date) }}</span>
            <span v-if="latestDiary.weather" class="meta-item">{{ weatherEmoji(latestDiary.weather) }} {{ latestDiary.weather }}</span>
            <span class="meta-item">{{ moodEmoji(latestDiary.mood) }} {{ latestDiary.mood || 'neutral' }}</span>
          </div>
          <p class="diary-content">{{ latestDiary.content }}</p>
          <div v-if="latestDiary.images && latestDiary.images.length > 0" class="diary-images">
            <img v-for="(img, idx) in latestDiary.images" :key="idx" :src="img" alt="日记附图" loading="lazy" />
          </div>
        </div>
      </el-card>
    </div>

    <!-- 待办事项侧边栏 -->
    <div v-if="activeTodos.length > 0" class="todo-sidebar">
      <el-card class="content-card">
        <template #header>
          <div class="card-header">
            <span>待办事项</span>
            <router-link class="more-link" to="/todo">查看全部 &gt;</router-link>
          </div>
        </template>
        <div class="todo-list">
          <div v-for="todo in activeTodos" :key="todo.id" class="todo-item">
            <div class="todo-top">
              <span class="todo-icon" v-html="todoIcon(todo.icon)"></span>
              <span class="todo-priority" :style="priorityStyle(todo.priority)">{{ todo.priority }}</span>
            </div>
            <div class="todo-task">{{ todo.task }}</div>
            <div class="todo-progress">
              <div class="progress-bar">
                <div class="progress-fill" :style="{ width: `${todo.progress || 0}%` }"></div>
              </div>
              <span class="progress-text">{{ todo.progress || 0 }}%</span>
            </div>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import {computed, onMounted, ref} from 'vue'
import axios from 'axios'
import ProfileCard from '@/components/Main/Home/ProfileCard.vue'
import Timeline from '@/components/Main/Home/Timeline.vue'
import ArticleCard from '@/components/Main/Article/ArticleCard.vue'
import ProjectCard from '@/components/Main/Project/ProjectCard.vue'
import GitHubHeatmap from '@/components/Main/Home/GitHubHeatmap.vue'

const articlesLoading = ref(false)
const projectsLoading = ref(false)
const articlesFromDB = ref([])
const projectsFromDB = ref([])
const latestDiary = ref(null)
const todosFromDB = ref([])

const API_BASE_URL = '/api'

// 获取文章数据
const fetchArticles = async () => {
  articlesLoading.value = true
  try {
    const response = await axios.get(`${API_BASE_URL}/articles`, {
      timeout: 10000,
      headers: {
        'Accept': 'application/json'
      }
    })

    if (response.data && Array.isArray(response.data)) {
      articlesFromDB.value = response.data
      console.log(`首页: 成功获取 ${articlesFromDB.value.length} 篇文章`)
    }
  } catch (error) {
    console.error('首页: 获取文章数据失败:', error)
    articlesFromDB.value = []
  } finally {
    articlesLoading.value = false
  }
}

// 获取项目数据
const fetchProjects = async () => {
  projectsLoading.value = true
  try {
    const response = await axios.get(`${API_BASE_URL}/projects`, {
      timeout: 10000,
      headers: {
        'Accept': 'application/json'
      }
    })

    if (response.data && Array.isArray(response.data)) {
      projectsFromDB.value = response.data
      console.log(`首页: 成功获取 ${projectsFromDB.value.length} 个项目`)
    }
  } catch (error) {
    console.error('首页: 获取项目数据失败:', error)
    projectsFromDB.value = []
  } finally {
    projectsLoading.value = false
  }
}

// 最近文章(从数据库获取，取前3篇)
const recentArticles = computed(() => {
  return [...articlesFromDB.value]
      .sort((a, b) => new Date(b.date) - new Date(a.date))
      .slice(0, 3)
})

// 最近项目(从数据库获取，取前3个)
const recentProjects = computed(() => {
  return [...projectsFromDB.value]
      .sort((a, b) => b.id - a.id)
      .slice(0, 3)
})

// 获取日记数据
const fetchDiaries = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/diaries`, {
      timeout: 10000,
      headers: {'Accept': 'application/json'},
    })
    if (response.data && Array.isArray(response.data) && response.data.length > 0) {
      const sorted = response.data.sort((a, b) => new Date(b.date) - new Date(a.date))
      latestDiary.value = sorted[0]
      console.log(`首页: 成功获取最新日记`)
    }
  } catch (error) {
    console.error('首页: 获取日记数据失败:', error)
  }
}

// 获取待办事项数据
const fetchTodos = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/todos`, {
      timeout: 10000,
      headers: {'Accept': 'application/json'},
    })
    if (response.data && Array.isArray(response.data)) {
      todosFromDB.value = response.data
      console.log(`首页: 成功获取 ${todosFromDB.value.length} 条待办`)
    }
  } catch (error) {
    console.error('首页: 获取待办数据失败:', error)
  }
}

// 活跃待办事项（取前3个）
const activeTodos = computed(() => {
  return todosFromDB.value
      .filter(t => !t.completed)
      .slice(0, 3)
})

// 日记辅助函数
const moodMap = {
  happy: '😊', relieved: '😌', sad: '😢', angry: '😠',
  neutral: '😐', excited: '🤩', tired: '😫',
}
const weatherMap = {
  sunny: '☀️', cloudy: '☁️', rainy: '🌧️', snowy: '❄️', windy: '💨',
}
const moodEmoji = (mood) => moodMap[mood] || '😐'
const weatherEmoji = (weather) => weatherMap[weather] || '🌤️'
const formatDiaryDate = (dateStr) => {
  const d = new Date(dateStr)
  if (isNaN(d.getTime())) return dateStr
  const pad = (n) => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}`
}

// 待办辅助函数
const todoIcon = (icon) => {
  if (!icon) return '📋'
  if (icon.startsWith('<svg')) return icon
  if (icon.startsWith('http') || icon.startsWith('/')) return `<img src="${icon}" alt="icon" style="width:20px;height:20px;" />`
  return icon
}
const priorityColors = {
  high: {bg: '#fff1f0', text: '#ff4d4f'},
  medium: {bg: '#fffbe6', text: '#faad14'},
  low: {bg: '#f6ffed', text: '#52c41a'},
}
const priorityStyle = (priority) => {
  const c = priorityColors[priority?.toLowerCase()] || {bg: '#f5f5f5', text: '#888'}
  return {backgroundColor: c.bg, color: c.text}
}

onMounted(async () => {
  await Promise.all([fetchArticles(), fetchProjects(), fetchDiaries(), fetchTodos()])
})
</script>

<style scoped>
.home-container {
  padding-top: 80px; /* 为固定的顶栏留出空间 */
  padding-bottom: 40px;
  max-width: 1280px;
  margin: 0 auto;
  display: flex;
  align-items: flex-start;
  gap: 20px;
  padding-left: 20px;
  padding-right: 20px;
}

.left-column {
  display: flex;
  flex-direction: column;
  gap: 20px;
  width: 350px; /* 您可以根据ProfileCard的宽度进行调整 */
  flex-shrink: 0;
}

.profile-card-container {
  position: sticky;
  top: 80px; /* 80px 是顶栏高度 */
  width: 100%;
}

.timeline-editor-container {
  width: 100%;
}

.right-column-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
  min-width: 0;
}

.top-row {
  display: flex;
  gap: 20px;
  align-items: flex-start;
}

.github-heatmap {
  flex: 1;
  min-width: 0;
}

.spacer {
  flex: 1;
  min-width: 0;
}

.content-card {
  width: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header span {
  font-size: 1.2em;
  font-weight: bold;
}

.more-link {
  text-decoration: none;
  color: #409eff;
  font-size: 14px;
}

.more-link:hover {
  text-decoration: underline;
}

.card-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.list-item-card {
  width: 100%;
}

/* 日记预览 */
.diary-preview {
  padding: 4px 0;
}

.diary-meta {
  display: flex;
  gap: 1.25rem;
  font-size: 0.9rem;
  color: #606266;
  flex-wrap: wrap;
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid #f0f2f5;
}

.diary-meta .meta-item {
  display: flex;
  align-items: center;
  gap: 0.35rem;
}

.diary-content {
  margin: 0;
  line-height: 1.8;
  color: #606266;
  font-size: 0.95rem;
  white-space: pre-wrap;
  max-height: 120px;
  overflow: hidden;
  text-overflow: ellipsis;
}

.diary-images {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(80px, 1fr));
  gap: 0.5rem;
  margin-top: 1rem;
}

.diary-images img {
  width: 100%;
  height: 80px;
  object-fit: cover;
  border-radius: 6px;
  border: 1px solid #ebeef5;
}

/* 待办事项侧边栏 */
.todo-sidebar {
  width: 280px;
  flex-shrink: 0;
}

.todo-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.todo-item {
  background: #fafafa;
  border: 1px solid #f0f2f5;
  border-radius: 8px;
  padding: 10px 12px;
  transition: all 0.2s ease;
}

.todo-item:hover {
  border-color: #c6e2ff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.todo-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.todo-icon {
  font-size: 1.1rem;
}

.todo-icon :deep(svg) {
  width: 18px;
  height: 18px;
}

.todo-priority {
  font-size: 0.7rem;
  font-weight: 500;
  text-transform: capitalize;
  padding: 1px 6px;
  border-radius: 3px;
}

.todo-task {
  font-size: 0.85rem;
  font-weight: 500;
  color: #303133;
  line-height: 1.4;
  margin-bottom: 8px;
}

.todo-progress {
  display: flex;
  align-items: center;
  gap: 6px;
}

.progress-bar {
  flex: 1;
  height: 4px;
  background: #f0f2f5;
  border-radius: 2px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #409eff, #337ecc);
  border-radius: 2px;
  transition: width 0.3s ease;
}

.progress-text {
  font-size: 0.7rem;
  color: #909399;
  width: 2.5em;
  text-align: right;
}

/* 响应式布局 */
@media (max-width: 1024px) {
  .home-container {
    flex-direction: column;
  }

  .left-column {
    width: 100%;
  }

  .todo-sidebar {
    width: 100%;
    order: 3;
  }
}

@media (max-width: 768px) {
  .home-container {
    padding: 80px 10px 20px;
  }
  
  .left-column {
    gap: 15px;
  }
  
  .right-column-content {
    gap: 15px;
  }
  
  .card-list {
    gap: 12px;
  }
  
  .card-header span {
    font-size: 1.1em;
  }
  
  .more-link {
    font-size: 13px;
  }
}

@media (max-width: 480px) {
  .home-container {
    padding: 70px 5px 15px;
    gap: 15px;
  }
  
  .left-column {
    gap: 12px;
  }
  
  .right-column-content {
    gap: 12px;
  }
  
  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .card-header span {
    font-size: 1.05em;
  }
  
  .more-link {
    align-self: flex-end;
    font-size: 12px;
  }
  
  .card-list {
    gap: 10px;
  }
}
</style>