<template>
  <div class="resources-page">
    <div class="header">
      <h1>资源中心</h1>
      <p>精心整理的书籍、图库和其他学习资源，助你更上一层楼。</p>
    </div>

    <div class="controls-container">
      <el-radio-group v-model="activeTab" size="large">
        <el-radio-button label="books">书籍</el-radio-button>
        <el-radio-button label="gallery">图库</el-radio-button>
      </el-radio-group>

      <div class="filter-bar">
        <el-input
            v-model="searchQuery"
            class="search-input"
            clearable
            placeholder="搜索资源..."
        />
        <el-select
            v-model="selectedTags"
            class="tag-select"
            filterable
            multiple
            placeholder="按标签筛选"
        >
          <el-option
              v-for="tag in allTags"
              :key="tag"
              :label="tag"
              :value="tag"
          />
        </el-select>
      </div>
    </div>

    <div v-loading="loading" class="content-grid">
      <!-- Books Grid -->
      <div v-if="activeTab === 'books'">
        <el-row :gutter="20">
          <el-col
              v-for="book in displayedItems"
              :key="book.id"
              :md="8" :sm="12" :xs="24"
              class="grid-col"
          >
            <BookCard :book="book"/>
          </el-col>
        </el-row>

        <!-- 书籍分页控件 -->
        <div v-if="!loading && displayedItems.length > 0 && booksTotalPages > 1" class="pagination-container">
          <el-pagination
              v-model:current-page="booksCurrentPage"
              :page-size="booksPageSize"
              :total="booksTotalItems"
              :pager-count="5"
              layout="prev, pager, next, jumper"
              background
              @current-change="handleBooksPageChange"
          />
        </div>
      </div>

      <!-- Gallery Waterfall -->
      <div v-if="activeTab === 'gallery'">
        <div class="waterfall-grid">
          <FigureCard
              v-for="figure in displayedItems"
              :key="figure.id"
              :figure="figure"
          />
        </div>

        <!-- 图表分页控件 -->
        <div v-if="!loading && displayedItems.length > 0 && figuresTotalPages > 1" class="pagination-container">
          <el-pagination
              v-model:current-page="figuresCurrentPage"
              :page-size="figuresPageSize"
              :total="figuresTotalItems"
              :pager-count="5"
              layout="prev, pager, next, jumper"
              background
              @current-change="handleFiguresPageChange"
          />
        </div>
      </div>

      <el-empty v-if="!loading && displayedItems.length === 0" description="没有找到匹配的资源"></el-empty>
    </div>
  </div>
</template>

<script setup>
import {computed, onMounted, ref, watch} from 'vue';
import axios from 'axios';
import BookCard from '@/components/Main/Resources/BookCard.vue';
import FigureCard from '@/components/Main/Resources/FigureCard.vue';

const activeTab = ref('books');
const searchQuery = ref('');
const selectedTags = ref([]);
const loading = ref(false);

// 数据库数据
const booksFromDB = ref([]);
const bookTagsFromDB = ref([]);
const figuresFromDB = ref([]);
const figureTagsFromDB = ref([]);

// 分页状态
const booksCurrentPage = ref(1);
const booksPageSize = ref(6);
const booksTotalItems = ref(0);
const booksTotalPages = ref(0);

const figuresCurrentPage = ref(1);
const figuresPageSize = ref(6);
const figuresTotalItems = ref(0);
const figuresTotalPages = ref(0);

const API_BASE_URL = '/api';

// 获取书籍数据
const fetchBooks = async () => {
  loading.value = true;
  try {
    const params = {
      page: booksCurrentPage.value,
      limit: booksPageSize.value
    };
    
    // 添加搜索参数
    if (searchQuery.value.trim()) {
      params.search = searchQuery.value.trim();
    }
    
    // 添加标签参数
    if (selectedTags.value.length > 0) {
      params.tags = selectedTags.value.join(',');
    }

    const response = await axios.get(`${API_BASE_URL}/books`, {
      params: params,
      timeout: 10000,
      headers: {
        'Accept': 'application/json'
      }
    });

    if (response.data && response.data.data) {
      booksFromDB.value = response.data.data;
      booksTotalItems.value = response.data.pagination.total;
      booksTotalPages.value = response.data.pagination.pages;
      console.log(`Resources: 成功获取 ${booksFromDB.value.length} 本书籍，页码: ${booksCurrentPage.value}`);
    }
  } catch (error) {
    console.error('Resources: 获取书籍数据失败:', error);
    booksFromDB.value = [];
    booksTotalItems.value = 0;
    booksTotalPages.value = 0;
  } finally {
    loading.value = false;
  }
};

// 获取书籍标签数据
const fetchBookTags = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/book-tags`, {
      timeout: 10000,
      headers: {
        'Accept': 'application/json'
      }
    });

    if (response.data) {
      bookTagsFromDB.value = response.data.tags || [];
      console.log(`Resources: 成功获取 ${bookTagsFromDB.value.length} 个书籍标签`);
    }
  } catch (error) {
    console.error('Resources: 获取书籍标签数据失败:', error);
    bookTagsFromDB.value = [];
  }
};

// 获取图库数据
const fetchFigures = async () => {
  loading.value = true;
  try {
    const response = await axios.get(`${API_BASE_URL}/gallery`, {
      timeout: 10000,
      headers: {
        'Accept': 'application/json'
      }
    });

    if (response.data && Array.isArray(response.data)) {
      let allFigures = response.data;

      // 搜索过滤
      if (searchQuery.value.trim()) {
        const q = searchQuery.value.trim().toLowerCase();
        allFigures = allFigures.filter(f => f.title && f.title.toLowerCase().includes(q));
      }

      // 标签过滤
      if (selectedTags.value.length > 0) {
        allFigures = allFigures.filter(f =>
          f.tags && selectedTags.value.some(t => f.tags.includes(t))
        );
      }

      // 提取标签
      const tagSet = new Set();
      response.data.forEach(f => {
        if (f.tags) f.tags.forEach(t => tagSet.add(t));
      });
      figureTagsFromDB.value = Array.from(tagSet);

      // 前端分页
      figuresTotalItems.value = allFigures.length;
      figuresTotalPages.value = Math.ceil(allFigures.length / figuresPageSize.value);
      const start = (figuresCurrentPage.value - 1) * figuresPageSize.value;
      figuresFromDB.value = allFigures.slice(start, start + figuresPageSize.value);
      console.log(`Resources: 成功获取 ${allFigures.length} 个图片`);
    }
  } catch (error) {
    console.error('Resources: 获取图库数据失败:', error);
    figuresFromDB.value = [];
    figuresTotalItems.value = 0;
    figuresTotalPages.value = 0;
  } finally {
    loading.value = false;
  }
};

// fetchFigureTags 不再需要，标签从gallery数据中提取

const allTags = computed(() => {
  if (activeTab.value === 'books') {
    // 使用从API获取的所有书籍标签
    return bookTagsFromDB.value.sort();
  } else {
    // 使用从API获取的所有图表标签
    return figureTagsFromDB.value.sort();
  }
});

// 直接使用API返回的数据（筛选已在后端完成）
const displayedItems = computed(() => {
  return activeTab.value === 'books' ? booksFromDB.value : figuresFromDB.value;
});

// 切换书籍页码
const handleBooksPageChange = (page) => {
  booksCurrentPage.value = page;
  fetchBooks();
};

// 切换图表页码
const handleFiguresPageChange = (page) => {
  figuresCurrentPage.value = page;
  fetchFigures();
};

// 监听activeTab变化，切换标签时获取对应数据和标签
watch(activeTab, (newTab) => {
  // 清空筛选条件
  selectedTags.value = []
  searchQuery.value = ''
  if (newTab === 'books') {
    booksCurrentPage.value = 1
    fetchBooks()
    fetchBookTags()
  } else if (newTab === 'gallery') {
    figuresCurrentPage.value = 1
    fetchFigures()
  }
})

// 监听搜索和标签变化，重新获取数据
watch([searchQuery, selectedTags], () => {
  // 重置到第一页
  if (activeTab.value === 'books') {
    booksCurrentPage.value = 1;
    fetchBooks();
  } else if (activeTab.value === 'gallery') {
    figuresCurrentPage.value = 1;
    fetchFigures();
  }
});

onMounted(async () => {
  // 默认显示书籍，所以首次加载获取书籍数据
  await Promise.all([fetchBooks(), fetchBookTags()]);
});
</script>

<style scoped>
.resources-page {
  max-width: 1400px;
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
}

.header p {
  font-size: 1.1em;
  color: #606266;
}

.controls-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 20px;
  margin-bottom: 40px;
}

.filter-bar {
  display: flex;
  gap: 15px;
  flex-grow: 1;
  justify-content: flex-end;
}

.search-input {
  max-width: 250px;
}

.tag-select {
  max-width: 300px;
  width: 100%;
}

.content-grid {
  min-height: 300px;
}

.waterfall-grid {
  columns: 3;
  column-gap: 16px;
}

@media (max-width: 1024px) {
  .waterfall-grid {
    columns: 2;
  }
}

@media (max-width: 640px) {
  .waterfall-grid {
    columns: 1;
  }
}

.grid-col {
  margin-bottom: 20px;
}

.pagination-container {
  margin-top: 30px;
  display: flex;
  justify-content: center;
}

/* 响应式布局 */
@media (max-width: 1024px) {
  .resources-page {
    margin: 90px auto 30px;
    padding: 0 15px;
  }
  
  .header {
    margin-bottom: 30px;
  }
  
  .header h1 {
    font-size: 2.2em;
  }
  
  .controls-container {
    flex-direction: column;
    align-items: stretch;
    gap: 15px;
  }
  
  .filter-bar {
    justify-content: stretch;
  }
  
  .search-input {
    max-width: none;
  }
  
  .tag-select {
    max-width: none;
  }
}

@media (max-width: 768px) {
  .resources-page {
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
  
  .controls-container {
    gap: 12px;
    margin-bottom: 30px;
  }
  
  .filter-bar {
    flex-direction: column;
    gap: 10px;
  }
  
  .grid-col {
    margin-bottom: 15px;
  }
  
  .pagination-container {
    margin-top: 20px;
  }
}

@media (max-width: 480px) {
  .resources-page {
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
  
  .controls-container {
    gap: 10px;
    margin-bottom: 20px;
  }
  
  .grid-col {
    margin-bottom: 12px;
  }
  
  .pagination-container {
    margin-top: 15px;
  }
  
  :deep(.el-pagination) {
    --el-font-size-base: 12px;
  }
  
  :deep(.el-radio-button__inner) {
    padding: 8px 12px;
  }
}
</style>
