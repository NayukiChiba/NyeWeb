<template>
  <div class="glass-card">
    <h3 class="font-bold text-base text-primary tracking-tight mb-5">网站历程</h3>
    <div v-loading="loading" class="min-h-[120px]">
      <div v-if="!loading && timelineItems.length > 0" class="relative pl-5 border-l-2 border-gray-200 space-y-5">
        <div v-for="item in timelineItems" :key="'item-' + item.id" class="relative">
          <!-- Dot -->
          <div class="absolute -left-[calc(0.625rem+1px)] top-1 w-3 h-3 rounded-full border-2 border-accent bg-white transition-colors"></div>
          <div class="ml-2">
            <p class="text-xs text-secondary/60 mb-0.5 tabular-nums">{{ formatTimestamp(item.timestamp) }}</p>
            <p class="text-sm text-primary leading-relaxed m-0">
              {{ item.content.length > 60 ? item.content.slice(0, 60) + '...' : item.content }}
            </p>
          </div>
        </div>
      </div>
      <div v-else-if="!loading && timelineItems.length === 0" class="text-center py-4 text-secondary text-sm">
        暂无历程数据
      </div>
    </div>
  </div>
</template>

<script setup>
import {onMounted, ref} from 'vue'
import axios from 'axios'

const loading = ref(false)
const timelineItems = ref([])
const API_BASE_URL = '/api'

const formatTimestamp = (timestamp) => {
  try {
    if (!timestamp) return '未知时间'
    const date = new Date(timestamp)
    if (isNaN(date.getTime())) return '无效时间'
    return date.toLocaleString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit' })
  } catch (e) { return '时间格式错误' }
}

const fetchTimelineData = async () => {
  loading.value = true
  try {
    const response = await axios.get(`${API_BASE_URL}/timeline`, { timeout: 10000, headers: { 'Accept': 'application/json' } })
    if (response.data && Array.isArray(response.data)) { timelineItems.value = response.data }
    else if (response.data?.data && Array.isArray(response.data.data)) { timelineItems.value = response.data.data }
  } catch (error) { console.error('获取时间线数据失败:', error) }
  finally { loading.value = false }
}

onMounted(() => { fetchTimelineData() })
</script>
