<template>
  <div class="dashboard-layout">
    <AdminSidebar/>
    <div class="main-content" :class="{ 'mobile-main-content': isMobile }">
      <router-view v-if="$route.path !== '/admin/dashboard'"/>
      <div v-else class="admin-page">
        <h2 class="admin-title mb-6">控制台</h2>

        <!-- Stats Row -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <div v-for="s in stats" :key="s.label" class="admin-card text-center">
            <p class="text-2xl font-bold text-accent">{{ s.count }}</p>
            <p class="text-xs text-secondary mt-1">{{ s.label }}</p>
          </div>
        </div>

        <!-- Editors Row -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div class="admin-card" style="cursor: default;">
            <TimelineEditor/>
          </div>
          <div class="admin-card" style="cursor: default;">
            <FavoriteImagesEditor/>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import AdminSidebar from '@/components/Admin/AdminSidebar.vue'
import TimelineEditor from '@/components/Admin/DashBoard/TimelineEditor.vue'
import FavoriteImagesEditor from '@/components/Admin/DashBoard/FavoriteImagesEditor.vue'
import axios from 'axios'

const isMobile = ref(false)
const stats = ref([
  { label: '文章', count: '-' },
  { label: '项目', count: '-' },
  { label: '工具', count: '-' },
  { label: '日记', count: '-' }
])

const fetchStats = async () => {
  try {
    const [articles, projects, tools, diaries] = await Promise.allSettled([
      axios.get('/api/admin/articles'),
      axios.get('/api/admin/projects'),
      axios.get('/api/admin/tools'),
      axios.get('/api/diaries')
    ])
    stats.value[0].count = articles.status === 'fulfilled' ? articles.value.data?.length || 0 : '-'
    stats.value[1].count = projects.status === 'fulfilled' ? projects.value.data?.length || 0 : '-'
    stats.value[2].count = tools.status === 'fulfilled' ? tools.value.data?.length || 0 : '-'
    stats.value[3].count = diaries.status === 'fulfilled' ? diaries.value.data?.length || 0 : '-'
  } catch {}
}

const checkIsMobile = () => { isMobile.value = window.innerWidth <= 768 }

onMounted(() => {
  checkIsMobile()
  window.addEventListener('resize', checkIsMobile)
  fetchStats()
})

onBeforeUnmount(() => { window.removeEventListener('resize', checkIsMobile) })
</script>

<style scoped>
.dashboard-layout { display: flex; height: 100vh; }
.main-content { flex: 1; margin-left: 250px; overflow-y: auto; }
.mobile-main-content { margin-left: 0; }
@media (max-width: 768px) {
  .main-content { margin-left: 0; }
}
</style>
