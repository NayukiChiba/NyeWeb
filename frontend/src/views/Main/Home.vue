<template>
  <div class="flex flex-col gap-16 w-full">
    
    <!-- Hero Section — Bold Artistic Statement -->
    <section class="relative pt-8 pb-4">
      <div class="flex flex-col gap-4">
        <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-accent/5 text-accent text-xs font-semibold w-fit">
          <span class="w-2 h-2 rounded-full bg-accent animate-pulse"></span>
          个人博客 · Personal Blog
        </div>
        <h1 class="font-heading font-black text-5xl md:text-7xl tracking-tight text-primary leading-[1.05]">
          Hi, I'm <span class="text-gradient">Nayuki</span>
        </h1>
        <p class="font-sans text-lg md:text-xl text-secondary max-w-xl leading-relaxed">
          记录知识、项目与日常生活的小空间。<br/>
          <span class="text-primary/40">A space for knowledge, projects, and daily life.</span>
        </p>
      </div>
      <!-- Decorative element -->
      <div class="absolute -top-10 right-0 w-64 h-64 rounded-full opacity-[0.06] blur-3xl pointer-events-none" style="background: linear-gradient(135deg, #6366F1, #EC4899);"></div>
    </section>

    <!-- Main Content Layout -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 w-full items-start">
      
      <!-- Left Sidebar -->
      <aside class="lg:col-span-3 flex flex-col gap-6 order-2 lg:order-1 w-full">
        <div class="lg:sticky lg:top-24 flex flex-col gap-6 w-full">
          <ProfileCard class="w-full"/>
          <Timeline class="w-full hidden lg:block"/>
        </div>
      </aside>

      <!-- Center Content -->
      <div class="lg:col-span-6 flex flex-col gap-10 order-1 lg:order-2 w-full min-w-0">
        
        <GitHubHeatmap class="w-full hidden sm:block"/>
        
        <!-- Recent Articles -->
        <section>
          <div class="flex justify-between items-end mb-6">
            <h2 class="section-title">最近文章</h2>
            <router-link class="text-accent hover:text-accent/80 font-medium text-sm transition-colors" to="/knowledge">查看全部 →</router-link>
          </div>
          <div v-loading="articlesLoading" class="flex flex-col gap-4">
            <ArticleCard
                v-for="article in recentArticles"
                :key="article.slug"
                :article="article"
            />
            <div v-if="!articlesLoading && recentArticles.length === 0" class="text-center py-12 text-secondary">
              <p class="text-4xl mb-2">📝</p>
              <p>暂无文章</p>
            </div>
          </div>
        </section>

        <!-- Recent Projects -->
        <section>
          <div class="flex justify-between items-end mb-6">
            <h2 class="section-title">最近项目</h2>
            <router-link class="text-accent hover:text-accent/80 font-medium text-sm transition-colors" to="/projects">查看全部 →</router-link>
          </div>
          <div v-loading="projectsLoading" class="grid grid-cols-1 gap-4">
            <ProjectCard
                v-for="project in recentProjects"
                :key="project.id"
                :project="project"
            />
            <div v-if="!projectsLoading && recentProjects.length === 0" class="text-center py-12 text-secondary">
              <p class="text-4xl mb-2">🚀</p>
              <p>暂无项目</p>
            </div>
          </div>
        </section>

        <!-- Latest Diary -->
        <section v-if="latestDiary">
          <div class="flex justify-between items-end mb-6">
            <h2 class="section-title">最新日记</h2>
            <router-link class="text-accent hover:text-accent/80 font-medium text-sm transition-colors" to="/diary">查看全部 →</router-link>
          </div>
          
          <div class="glass-card">
            <div class="flex flex-wrap gap-3 text-sm text-secondary mb-4">
              <span class="tag-pill">📅 {{ formatDiaryDate(latestDiary.date) }}</span>
              <span v-if="latestDiary.weather" class="tag-pill">{{ weatherEmoji(latestDiary.weather) }} {{ latestDiary.weather }}</span>
              <span class="tag-pill">{{ moodEmoji(latestDiary.mood) }} {{ latestDiary.mood || 'neutral' }}</span>
            </div>
            <p class="text-primary leading-relaxed whitespace-pre-wrap max-h-32 overflow-hidden text-ellipsis m-0">
              {{ latestDiary.content }}
            </p>
            <div v-if="latestDiary.images && latestDiary.images.length > 0" class="flex gap-2 mt-4 overflow-x-auto pb-2 snap-x">
              <img v-for="(img, idx) in latestDiary.images" :key="idx" :src="img" alt="日记附图" loading="lazy" class="h-24 w-auto rounded-xl object-cover border border-gray-200 shadow-sm snap-start shrink-0" />
            </div>
          </div>
        </section>
      </div>

      <!-- Right Sidebar (Todos) -->
      <aside v-if="activeTodos.length > 0" class="lg:col-span-3 flex flex-col order-3 w-full relative">
        <section class="lg:sticky lg:top-24">
          <div class="flex justify-between items-end mb-6">
            <h2 class="section-title text-xl">待办事项</h2>
            <router-link class="text-accent hover:text-accent/80 font-medium text-xs transition-colors" to="/todo">全部 →</router-link>
          </div>
          
          <div class="flex flex-col gap-3">
            <div v-for="todo in activeTodos" :key="todo.id" class="glass-card !p-4">
              <div class="flex justify-between items-center mb-2">
                <span class="w-6 h-6 flex-shrink-0 flex items-center justify-center" v-html="todoIcon(todo.icon)"></span>
                <span class="text-[10px] font-semibold px-2 py-0.5 rounded-full whitespace-nowrap capitalize" :class="priorityClass(todo.priority)">{{ priorityLabel(todo.priority) }}</span>
              </div>
              <div class="text-sm font-medium text-primary mb-3 leading-snug">{{ todo.task }}</div>
              <div class="flex items-center gap-3">
                <div class="flex-1 h-1.5 bg-muted rounded-full overflow-hidden">
                  <div class="h-full rounded-full transition-all duration-500" :style="{ width: `${todo.progress || 0}%`, background: 'var(--gradient-brand)' }"></div>
                </div>
                <span class="text-xs text-secondary font-medium min-w-[2.5em] text-right">{{ todo.progress || 0 }}%</span>
              </div>
            </div>
          </div>
        </section>
      </aside>
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

const fetchArticles = async () => {
  articlesLoading.value = true
  try {
    const response = await axios.get(`${API_BASE_URL}/articles`, { timeout: 10000, headers: { 'Accept': 'application/json' } })
    if (response.data && Array.isArray(response.data)) { articlesFromDB.value = response.data }
  } catch (error) { console.error('首页: 获取文章数据失败:', error); articlesFromDB.value = [] }
  finally { articlesLoading.value = false }
}

const fetchProjects = async () => {
  projectsLoading.value = true
  try {
    const response = await axios.get(`${API_BASE_URL}/projects`, { timeout: 10000, headers: { 'Accept': 'application/json' } })
    if (response.data && Array.isArray(response.data)) { projectsFromDB.value = response.data }
  } catch (error) { console.error('首页: 获取项目数据失败:', error); projectsFromDB.value = [] }
  finally { projectsLoading.value = false }
}

const recentArticles = computed(() => [...articlesFromDB.value].sort((a, b) => new Date(b.date) - new Date(a.date)).slice(0, 3))
const recentProjects = computed(() => [...projectsFromDB.value].sort((a, b) => b.id - a.id).slice(0, 3))

const fetchDiaries = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/diaries`, { timeout: 10000, headers: {'Accept': 'application/json'} })
    if (response.data && Array.isArray(response.data) && response.data.length > 0) {
      latestDiary.value = response.data.sort((a, b) => new Date(b.date) - new Date(a.date))[0]
    }
  } catch (error) { console.error('首页: 获取日记数据失败:', error) }
}

const fetchTodos = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/todos`, { timeout: 10000, headers: {'Accept': 'application/json'} })
    if (response.data && Array.isArray(response.data)) { todosFromDB.value = response.data }
  } catch (error) { console.error('首页: 获取待办数据失败:', error) }
}

const activeTodos = computed(() => todosFromDB.value.filter(t => !t.completed).slice(0, 3))

const moodMap = { happy: '😊', relieved: '😌', sad: '😢', angry: '😠', neutral: '😐', excited: '🤩', tired: '😫' }
const weatherMap = { sunny: '☀️', cloudy: '☁️', rainy: '🌧️', snowy: '❄️', windy: '💨' }
const moodEmoji = (mood) => moodMap[mood] || '😐'
const weatherEmoji = (weather) => weatherMap[weather] || '🌤️'
const formatDiaryDate = (dateStr) => {
  const d = new Date(dateStr)
  if (isNaN(d.getTime())) return dateStr
  const pad = (n) => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}`
}

const todoIcon = (icon) => {
  if (!icon) return '📋'
  if (icon.startsWith('<svg')) return icon.replace('<svg', '<svg style="width:24px;height:24px;"')
  if (icon.startsWith('http') || icon.startsWith('/')) return `<img src="${icon}" alt="icon" style="width:24px;height:24px;object-fit:contain;" />`
  return icon
}
const priorityLabel = (p) => {
  const map = { high: '高', medium: '中', low: '低' }
  return map[p?.toLowerCase()] || p
}
const priorityClass = (priority) => {
  const map = {
    high: 'bg-red-50 text-red-500',
    medium: 'bg-amber-50 text-amber-600',
    low: 'bg-emerald-50 text-emerald-500',
  }
  return map[priority?.toLowerCase()] || 'bg-slate-50 text-slate-400'
}

onMounted(async () => {
  await Promise.all([fetchArticles(), fetchProjects(), fetchDiaries(), fetchTodos()])
})
</script>