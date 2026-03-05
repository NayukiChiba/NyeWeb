<template>
  <div class="glass-card">
    <div class="flex justify-between items-center mb-5">
      <h3 class="font-bold text-base text-primary tracking-tight">GitHub 贡献</h3>
      <el-tooltip content="过去一年的代码提交活动" placement="top">
        <span class="text-secondary/50 hover:text-accent cursor-pointer transition-colors text-sm">ⓘ</span>
      </el-tooltip>
    </div>
    <div v-loading="loading" class="heatmap-container">
      <div v-if="!loading && contributions.length === 0" class="text-center py-8 text-secondary">
        <p class="text-3xl mb-1">📊</p>
        <p class="text-sm">暂无贡献数据</p>
      </div>
      <div v-else-if="!loading" class="heatmap">
        <div class="heatmap-months">
          <span v-for="month in months" :key="month" class="month-label">{{ month }}</span>
        </div>
        <div class="heatmap-grid">
          <div v-for="(week, weekIndex) in weeks" :key="weekIndex" class="heatmap-week">
            <div
              v-for="day in week" :key="day.date"
              class="heatmap-day" :class="getDayColorClass(day.count)"
              :style="{ opacity: day.count > 0 ? 0.5 + (day.count / maxCount) * 0.5 : 1.0 }"
              :title="`${day.date}: ${day.count} 次提交`"
            />
          </div>
        </div>
        <div class="heatmap-legend">
          <span>少</span>
          <div class="legend-items">
            <div class="legend-item" style="background: #F1F5F9;"></div>
            <div class="legend-item" style="background: #C7D2FE;"></div>
            <div class="legend-item" style="background: #818CF8;"></div>
            <div class="legend-item" style="background: #6366F1;"></div>
            <div class="legend-item" style="background: #4338CA;"></div>
          </div>
          <span>多</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

const loading = ref(false)
const contributions = ref([])
const maxCount = ref(0)
const GITHUB_TOKEN = import.meta.env.VITE_GITHUB_TOKEN

const months = computed(() => {
  const monthNames = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
  const uniqueMonths = new Set()
  contributions.value.forEach(c => { uniqueMonths.add(new Date(c.date).getMonth()) })
  return Array.from(uniqueMonths).sort().map(m => monthNames[m])
})

const weeks = computed(() => {
  const w = []; let cur = []
  contributions.value.forEach((day, i) => {
    if (i % 7 === 0 && cur.length > 0) { w.push(cur); cur = [] }
    cur.push(day)
  })
  if (cur.length > 0) w.push(cur)
  return w
})

const getDayColorClass = (count) => {
  if (count === 0) return 'color-0'
  if (count <= 1) return 'color-1'
  if (count <= 3) return 'color-2'
  if (count <= 5) return 'color-3'
  return 'color-4'
}

const getOneYearAgo = () => { const d = new Date(); d.setFullYear(d.getFullYear() - 1); return d }

const generateMockData = () => {
  const data = []; const today = new Date(); const ago = new Date(today); ago.setFullYear(ago.getFullYear() - 1)
  for (let d = new Date(ago); d <= today; d.setDate(d.getDate() + 1)) {
    data.push({ date: d.toISOString().split('T')[0], count: Math.random() > 0.7 ? Math.floor(Math.random() * 10) : 0 })
  }
  return data
}

const fetchGitHubContributions = async () => {
  if (!GITHUB_TOKEN || GITHUB_TOKEN === 'your_github_token_here') { return }
  loading.value = true
  try {
    const query = `query { viewer { contributionsCollection(from: "${getOneYearAgo().toISOString()}", to: "${new Date().toISOString()}") { contributionCalendar { totalContributions weeks { contributionDays { date contributionCount color } } } } } }`
    const response = await axios.post('https://api.github.com/graphql', { query }, { headers: { 'Authorization': `Bearer ${GITHUB_TOKEN}`, 'Content-Type': 'application/json' }, timeout: 10000 })
    const data = response.data.data.viewer.contributionsCollection.contributionCalendar
    const all = []; data.weeks.forEach(w => { w.contributionDays.forEach(d => { all.push({ date: d.date, count: d.contributionCount }) }) })
    contributions.value = all; maxCount.value = Math.max(...all.map(d => d.count), 1)
  } catch (error) {
    contributions.value = generateMockData(); maxCount.value = Math.max(...contributions.value.map(d => d.count), 1)
  } finally { loading.value = false }
}

onMounted(() => { fetchGitHubContributions() })
</script>

<style scoped>
.heatmap-container { display: flex; flex-direction: column; align-items: center; width: 100%; }
.heatmap { display: flex; flex-direction: column; gap: 3px; width: 100%; }
.heatmap-months { display: flex; justify-content: space-between; margin-bottom: 4px; font-size: 10px; color: #94A3B8; }
.month-label { flex: 1; text-align: center; }
.heatmap-grid { display: flex; gap: 3px; justify-content: space-between; width: 100%; flex-wrap: nowrap; }
.heatmap-week { display: flex; flex-direction: column; gap: 3px; flex: 1; min-width: 0; }
.heatmap-day { width: 100%; aspect-ratio: 1; border-radius: 3px; cursor: pointer; transition: all 0.2s; background: #F1F5F9; }
.heatmap-day:hover { transform: scale(1.3); z-index: 10; box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.5); }
.color-0 { background: #F1F5F9; }
.color-1 { background: #C7D2FE; }
.color-2 { background: #818CF8; }
.color-3 { background: #6366F1; }
.color-4 { background: #4338CA; }
.heatmap-legend { display: flex; align-items: center; gap: 6px; margin-top: 12px; font-size: 10px; color: #94A3B8; justify-content: center; }
.legend-items { display: flex; gap: 3px; }
.legend-item { width: 11px; height: 11px; border-radius: 3px; }
</style>