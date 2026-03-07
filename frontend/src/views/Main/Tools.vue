<template>
  <div class="tools-page">
    <div class="header">
      <h1 class="section-title text-3xl">小工具箱</h1>
      <p class="text-secondary mt-2">常用书签、在线工具与资源导航。</p>
    </div>

    <!-- Search -->
    <div class="search-bar glass-card !p-4 mb-8">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="搜索工具..."
        class="w-full bg-transparent outline-none text-primary placeholder:text-secondary/50"
      />
    </div>

    <div v-if="loading" class="text-center py-20 text-secondary">加载中...</div>

    <div v-else-if="categories.length === 0" class="text-center py-20 text-secondary">没有找到匹配的工具</div>

    <!-- Category Sections -->
    <div v-else class="flex flex-col gap-10">
      <section v-for="category in categories" :key="category" class="category-section">
        <!-- Section Header -->
        <div class="flex items-center justify-between mb-4 pb-2 border-b border-gray-200">
          <h2 class="text-lg font-semibold text-primary">{{ category }}</h2>
          <div v-if="getTotalPages(category) > 1" class="flex items-center gap-3">
            <button
              class="nav-btn"
              :disabled="getCategoryPage(category) === 0"
              @click="prevPage(category)"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"/></svg>
            </button>
            <span class="text-sm text-secondary tabular-nums">
              {{ getCategoryPage(category) + 1 }} / {{ getTotalPages(category) }}
            </span>
            <button
              class="nav-btn"
              :disabled="getCategoryPage(category) >= getTotalPages(category) - 1"
              @click="nextPage(category)"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg>
            </button>
          </div>
        </div>

        <!-- Tools Grid (current page) -->
        <transition name="fade" mode="out-in">
          <div :key="getCategoryPage(category)" class="tools-grid">
            <ToolCard
              v-for="tool in getPageTools(category)"
              :key="tool.id"
              :tool="tool"
            />
          </div>
        </transition>
      </section>
    </div>
  </div>
</template>

<script setup>
import {computed, onMounted, ref, watch} from 'vue';
import axios from 'axios';
import ToolCard from '@/components/Main/Tools/ToolCard.vue';

const searchQuery = ref('');
const loading = ref(false);
const allTools = ref([]);
const categoryPages = ref({});  // { category: currentPageIndex }

const ITEMS_PER_PAGE = 6;
const API_BASE_URL = '/api';

// Fetch ALL tools (no server-side pagination)
const fetchAllTools = async () => {
  loading.value = true;
  try {
    const params = { page: 1, limit: 999 };
    if (searchQuery.value.trim()) {
      params.search = searchQuery.value.trim();
    }
    const response = await axios.get(`${API_BASE_URL}/tools`, {
      params,
      timeout: 10000,
      headers: { 'Accept': 'application/json' }
    });
    if (response.data && response.data.data) {
      allTools.value = response.data.data;
      // Reset pages
      categoryPages.value = {};
    }
  } catch (error) {
    console.error('Tools: 获取工具数据失败:', error);
    allTools.value = [];
  } finally {
    loading.value = false;
  }
};

// Group by category
const grouped = computed(() => {
  const map = {};
  allTools.value.forEach(tool => {
    const cat = tool.category || '其他';
    if (!map[cat]) map[cat] = [];
    map[cat].push(tool);
  });
  return map;
});

const categories = computed(() => Object.keys(grouped.value).sort());

const getCategoryPage = (cat) => categoryPages.value[cat] || 0;

const getTotalPages = (cat) => {
  const tools = grouped.value[cat] || [];
  return Math.ceil(tools.length / ITEMS_PER_PAGE);
};

const getPageTools = (cat) => {
  const tools = grouped.value[cat] || [];
  const page = getCategoryPage(cat);
  return tools.slice(page * ITEMS_PER_PAGE, (page + 1) * ITEMS_PER_PAGE);
};

const prevPage = (cat) => {
  const current = getCategoryPage(cat);
  if (current > 0) categoryPages.value[cat] = current - 1;
};

const nextPage = (cat) => {
  const current = getCategoryPage(cat);
  if (current < getTotalPages(cat) - 1) categoryPages.value[cat] = current + 1;
};

watch(searchQuery, () => {
  categoryPages.value = {};
  fetchAllTools();
});

onMounted(fetchAllTools);
</script>

<style scoped>
.tools-page {
  max-width: 960px;
  margin: 100px auto 40px;
  padding: 0 20px;
}

.header {
  text-align: center;
  margin-bottom: 32px;
}

.nav-btn {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: 1px solid #e2e8f0;
  background: white;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
}

.nav-btn:hover:not(:disabled) {
  border-color: #6366f1;
  color: #6366f1;
  background: #f0f0ff;
}

.nav-btn:disabled {
  opacity: 0.35;
  cursor: not-allowed;
}

.tools-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 12px;
}

@media (min-width: 640px) {
  .tools-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .tools-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

/* Fade transition */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@media (max-width: 768px) {
  .tools-page {
    margin: 80px auto 20px;
  }
}
</style>
