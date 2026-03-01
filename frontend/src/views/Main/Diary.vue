<template>
  <div class="diary-container">
    <div class="header">
      <h1>个人日记</h1>
      <p>记录生活点滴与碎碎念。</p>
    </div>

    <div v-loading="loading" class="timeline" id="diary-timeline">
      <el-empty v-if="!loading && diaries.length === 0" description="暂无日记数据"></el-empty>

      <div v-for="year in years" :key="year" class="year-section">
        <div class="timeline-marker year-marker"></div>
        <div class="year-accordion">
          <div class="year-summary" @click="toggleYear(year)">
            <span class="expand-arrow" :class="{ expanded: expandedYears.has(year) }">▶</span>
            <span class="year-text">{{ year }}年</span>
            <span class="entry-count">({{ getYearCount(year) }} 条)</span>
          </div>

          <transition name="slide-down">
            <div v-if="expandedYears.has(year)" class="year-content">
              <div v-for="month in getMonths(year)" :key="month" class="month-section">
                <div class="timeline-marker month-marker"></div>
                <div class="month-accordion">
                  <div class="month-summary" @click="toggleMonth(year, month)">
                    <span class="expand-arrow"
                          :class="{ expanded: expandedMonths.has(`${year}-${month}`) }">▶</span>
                    <span class="month-text">{{ monthNames[parseInt(month) - 1] }}</span>
                    <span class="entry-count">({{ groupedDiaries[year][month].length }} 条)</span>
                  </div>

                  <transition name="slide-down">
                    <div v-if="expandedMonths.has(`${year}-${month}`)" class="month-content">
                      <div class="diary-entries">
                        <DiaryCard
                            v-for="diary in groupedDiaries[year][month]"
                            :key="diary.id"
                            :diary="diary"
                        />
                      </div>
                    </div>
                  </transition>
                </div>
              </div>
            </div>
          </transition>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {computed, onMounted, ref} from 'vue'
import axios from 'axios'
import DiaryCard from '@/components/Main/Diary/DiaryCard.vue'

const loading = ref(false)
const diaries = ref([])
const expandedYears = ref(new Set())
const expandedMonths = ref(new Set())

const API_BASE_URL = '/api'

const monthNames = [
  '一月', '二月', '三月', '四月', '五月', '六月',
  '七月', '八月', '九月', '十月', '十一月', '十二月',
]

const fetchDiaries = async () => {
  loading.value = true
  try {
    const response = await axios.get(`${API_BASE_URL}/diaries`, {
      timeout: 10000,
      headers: {'Accept': 'application/json'},
    })
    if (response.data && Array.isArray(response.data)) {
      diaries.value = response.data.sort(
          (a, b) => new Date(b.date).valueOf() - new Date(a.date).valueOf()
      )
      console.log(`日记页面: 成功获取 ${diaries.value.length} 条日记`)
    }
  } catch (error) {
    console.error('日记页面: 获取日记数据失败:', error)
    diaries.value = []
  } finally {
    loading.value = false
  }
}

// Group diaries by year and month
const groupedDiaries = computed(() => {
  const grouped = {}
  diaries.value.forEach((diary) => {
    const date = new Date(diary.date)
    const year = date.getFullYear().toString()
    const month = String(date.getMonth() + 1).padStart(2, '0')
    if (!grouped[year]) grouped[year] = {}
    if (!grouped[year][month]) grouped[year][month] = []
    grouped[year][month].push(diary)
  })
  return grouped
})

const years = computed(() => {
  return Object.keys(groupedDiaries.value).sort((a, b) => parseInt(b) - parseInt(a))
})

const getMonths = (year) => {
  return Object.keys(groupedDiaries.value[year]).sort((a, b) => parseInt(b) - parseInt(a))
}

const getYearCount = (year) => {
  return Object.values(groupedDiaries.value[year]).reduce(
      (sum, monthDiaries) => sum + monthDiaries.length, 0
  )
}

const toggleYear = (year) => {
  if (expandedYears.value.has(year)) {
    expandedYears.value.delete(year)
  } else {
    expandedYears.value.add(year)
  }
  // Trigger reactivity
  expandedYears.value = new Set(expandedYears.value)
}

const toggleMonth = (year, month) => {
  const key = `${year}-${month}`
  if (expandedMonths.value.has(key)) {
    expandedMonths.value.delete(key)
  } else {
    expandedMonths.value.add(key)
  }
  expandedMonths.value = new Set(expandedMonths.value)
}

// Auto-expand latest year and month
const autoExpandLatest = () => {
  if (years.value.length > 0) {
    const latestYear = years.value[0]
    expandedYears.value.add(latestYear)
    expandedYears.value = new Set(expandedYears.value)

    const months = getMonths(latestYear)
    if (months.length > 0) {
      const latestMonth = months[0]
      expandedMonths.value.add(`${latestYear}-${latestMonth}`)
      expandedMonths.value = new Set(expandedMonths.value)
    }
  }
}

onMounted(async () => {
  await fetchDiaries()
  autoExpandLatest()
})
</script>

<style scoped>
.diary-container {
  max-width: 800px;
  margin: 100px auto 40px;
  padding: 0 20px;
}

.header {
  text-align: center;
  margin-bottom: 40px;
}

.header h1 {
  font-size: 2.5em;
  margin-bottom: 10px;
  color: inherit;
}

.header p {
  font-size: 1.1em;
  color: #606266;
}

/* Timeline Styles */
.timeline {
  position: relative;
  padding-left: 2rem;
  border-left: 2px solid #c6e2ff;
  margin-left: 1rem;
  min-height: 200px;
}

/* Year Section */
.year-section {
  position: relative;
  margin-bottom: 2.5rem;
}

.year-marker {
  position: absolute;
  left: -2.6rem;
  top: 0.35rem;
  width: 14px;
  height: 14px;
  background: #409eff;
  border-radius: 50%;
  z-index: 1;
  box-shadow: 0 0 0 4px #fff;
}

.year-summary {
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.4rem;
  font-weight: 700;
  color: #303133;
  padding: 0.5rem 0;
  transition: color 0.2s;
  user-select: none;
}

.year-summary:hover {
  color: #409eff;
}

.year-text {
  margin-right: 0.25rem;
}

.entry-count {
  font-size: 0.9rem;
  font-weight: 500;
  color: #909399;
}

.expand-arrow {
  font-size: 0.7em;
  color: #409eff;
  transition: transform 0.2s ease;
  display: inline-block;
}

.expand-arrow.expanded {
  transform: rotate(90deg);
}

.year-content {
  margin-top: 1.25rem;
  position: relative;
  padding-left: 2rem;
  border-left: 2px solid #ebeef5;
  margin-left: 0.5rem;
}

/* Month Section */
.month-section {
  position: relative;
  margin-bottom: 2rem;
}

.month-marker {
  position: absolute;
  left: -2.55rem;
  top: 0.35rem;
  width: 10px;
  height: 10px;
  background: #fff;
  border: 2px solid #409eff;
  border-radius: 50%;
  z-index: 1;
}

.month-summary {
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.15rem;
  font-weight: 600;
  color: #606266;
  padding: 0.3rem 0;
  transition: color 0.2s;
  user-select: none;
}

.month-summary:hover {
  color: #409eff;
}

.month-content {
  margin-top: 0.75rem;
}

.diary-entries {
  display: flex;
  flex-direction: column;
  gap: 0;
}

/* Slide down transition */
.slide-down-enter-active {
  animation: slideDown 0.3s ease-out;
}

.slide-down-leave-active {
  animation: slideDown 0.2s ease-out reverse;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Mobile responsive */
@media (max-width: 1024px) {
  .diary-container {
    margin: 90px auto 30px;
    padding: 0 15px;
  }
}

@media (max-width: 768px) {
  .diary-container {
    margin: 80px auto 20px;
    padding: 0 10px;
  }

  .header {
    margin-bottom: 25px;
  }

  .header h1 {
    font-size: 2em;
  }

  .header p {
    font-size: 1em;
  }

  .year-summary {
    font-size: 1.2rem;
  }

  .month-summary {
    font-size: 1rem;
  }

  .year-content {
    padding-left: 1.5rem;
  }
}

@media (max-width: 480px) {
  .diary-container {
    margin: 70px auto 15px;
    padding: 0 5px;
  }

  .header {
    margin-bottom: 20px;
  }

  .header h1 {
    font-size: 1.8em;
  }

  .header p {
    font-size: 0.9em;
  }
}
</style>
