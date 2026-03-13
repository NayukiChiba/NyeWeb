<template>
  <div class="glass-card">
    <h3 class="font-bold text-base text-primary tracking-tight mb-5">项目Git历史</h3>
    <div v-loading="loading" class="min-h-[120px]">
      <div v-if="!loading && events.length > 0" class="relative pl-5 border-l-2 border-gray-200 space-y-5">
        <div v-for="(event, index) in events" :key="index" class="relative">
          <!-- Dot -->
          <div class="absolute -left-[calc(0.625rem+1px)] top-1 w-3 h-3 rounded-full border-2 border-accent bg-white transition-colors"></div>
          <div class="ml-2">
            <p class="text-xs text-secondary/60 mb-0.5 tabular-nums">{{ event.date }}</p>
            <p class="text-sm font-medium text-accent m-0">{{ event.repo }}</p>
            <p class="text-sm text-primary leading-relaxed m-0">
              {{ event.message.length > 80 ? event.message.slice(0, 80) + '...' : event.message }}
            </p>
          </div>
        </div>
      </div>
      <div v-else-if="!loading && events.length === 0" class="text-center py-4 text-secondary text-sm">
        暂无Git历史数据
      </div>
    </div>
    <div v-if="totalPages > 1" class="flex justify-center items-center gap-3 mt-4 pt-3 border-t border-gray-100">
      <button
        :disabled="currentPage <= 1"
        class="text-xs text-secondary hover:text-accent disabled:opacity-30 disabled:cursor-not-allowed cursor-pointer transition-colors"
        @click="changePage(-1)"
      >← 上一页</button>
      <span class="text-xs text-secondary/60">{{ currentPage }}/{{ totalPages }}</span>
      <button
        :disabled="currentPage >= totalPages"
        class="text-xs text-secondary hover:text-accent disabled:opacity-30 disabled:cursor-not-allowed cursor-pointer transition-colors"
        @click="changePage(1)"
      >下一页 →</button>
    </div>
  </div>
</template>

<script setup>
import {onMounted, ref, computed} from 'vue'
import axios from 'axios'

const loading = ref(false)
const allEvents = ref([])
const currentPage = ref(1)
const pageSize = 6

const events = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return allEvents.value.slice(start, start + pageSize)
})

const totalPages = computed(() => Math.ceil(allEvents.value.length / pageSize))

const changePage = (delta) => {
  const newPage = currentPage.value + delta
  if (newPage >= 1 && newPage <= totalPages.value) {
    currentPage.value = newPage
  }
}

const formatDate = (dateStr) => {
  try {
    const date = new Date(dateStr)
    if (isNaN(date.getTime())) return '未知时间'
    return date.toLocaleString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit' })
  } catch (e) { return '时间格式错误' }
}

const fetchGitHistory = async () => {
  loading.value = true
  try {
    // 优先尝试从后端 /api/timeline 获取
    const response = await axios.get('/api/timeline', { timeout: 10000, headers: { 'Accept': 'application/json' } })
    let data = []
    if (response.data && Array.isArray(response.data)) {
      data = response.data
    } else if (response.data?.data && Array.isArray(response.data.data)) {
      data = response.data.data
    }

    if (data.length > 0) {
      allEvents.value = data.map(item => ({
        date: formatDate(item.timestamp || item.date),
        repo: item.repo || item.project || 'NayukiWeb',
        message: item.content || item.message || ''
      }))
    } else {
      // 回退：使用 GitHub Events API
      await fetchFromGitHub()
    }
  } catch (error) {
    console.warn('后端时间线获取失败，尝试GitHub API:', error.message)
    await fetchFromGitHub()
  } finally {
    loading.value = false
  }
}

const fetchFromGitHub = async () => {
  try {
    const response = await axios.get('https://api.github.com/users/NayeyYe/events/public', {
      params: { per_page: 30 },
      timeout: 10000
    })
    if (response.data && Array.isArray(response.data)) {
      allEvents.value = response.data
        .filter(e => e.type === 'PushEvent')
        .flatMap(e => {
          const repo = e.repo?.name?.split('/')[1] || e.repo?.name || ''
          return (e.payload?.commits || []).map(c => ({
            date: formatDate(e.created_at),
            repo: repo,
            message: c.message || ''
          }))
        })
        .slice(0, 30)
    }
  } catch (error) {
    console.error('GitHub API获取失败:', error)
    allEvents.value = []
  }
}

onMounted(() => { fetchGitHistory() })
</script>
