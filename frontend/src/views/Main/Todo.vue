<template>
  <div class="todo-container">
    <div class="header">
      <h1>任务管理</h1>
      <p>规划与追踪个人目标。</p>
    </div>

    <div v-loading="loading" class="todo-content">
      <el-empty v-if="!loading && todos.length === 0" description="暂无待办数据"></el-empty>

      <!-- 已完成任务（折叠） -->
      <div v-if="completedTodos.length > 0" class="completed-section">
        <div class="completed-header" @click="showCompleted = !showCompleted">
          <span class="expand-arrow" :class="{ expanded: showCompleted }">▶</span>
          <span>已完成任务 ({{ completedTodos.length }})</span>
        </div>
        <transition name="slide-down">
          <div v-if="showCompleted" class="task-grid">
            <TaskCard v-for="todo in completedTodos" :key="todo.id" :todo="todo"/>
          </div>
        </transition>
      </div>

      <div class="todo-layers">
        <!-- 短期目标 -->
        <section v-if="shortTermTodos.length > 0" class="layer-section">
          <h2 class="layer-title">🚀 短期目标 (Short-term)</h2>
          <div class="task-grid">
            <TaskCard v-for="todo in shortTermTodos" :key="todo.id" :todo="todo"/>
          </div>
        </section>

        <!-- 中期目标 -->
        <section v-if="midTermTodos.length > 0" class="layer-section">
          <h2 class="layer-title">📅 中期目标 (Medium-term)</h2>
          <div class="task-grid">
            <TaskCard v-for="todo in midTermTodos" :key="todo.id" :todo="todo"/>
          </div>
        </section>

        <!-- 长期目标 -->
        <section v-if="longTermTodos.length > 0" class="layer-section">
          <h2 class="layer-title">🏔️ 长期目标 (Long-term)</h2>
          <div class="task-grid">
            <TaskCard v-for="todo in longTermTodos" :key="todo.id" :todo="todo"/>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
import {computed, onMounted, ref} from 'vue'
import axios from 'axios'
import TaskCard from '@/components/Main/Todo/TaskCard.vue'

const loading = ref(false)
const todos = ref([])
const showCompleted = ref(false)

const API_BASE_URL = '/api'

const fetchTodos = async () => {
  loading.value = true
  try {
    const response = await axios.get(`${API_BASE_URL}/todos`, {
      timeout: 10000,
      headers: {'Accept': 'application/json'},
    })
    if (response.data && Array.isArray(response.data)) {
      todos.value = response.data
      console.log(`待办页面: 成功获取 ${todos.value.length} 条待办`)
    }
  } catch (error) {
    console.error('待办页面: 获取待办数据失败:', error)
    todos.value = []
  } finally {
    loading.value = false
  }
}

const activeTodos = computed(() => todos.value.filter((t) => !t.completed))
const completedTodos = computed(() => todos.value.filter((t) => t.completed))

const shortTermTodos = computed(() => activeTodos.value.filter((t) => t.type === 'short-term'))
const midTermTodos = computed(() => activeTodos.value.filter((t) => t.type === 'mid-term'))
const longTermTodos = computed(() => activeTodos.value.filter((t) => t.type === 'long-term'))

onMounted(() => {
  fetchTodos()
})
</script>

<style scoped>
.todo-container {
  max-width: 1000px;
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

.todo-content {
  min-height: 200px;
}

/* Completed Section */
.completed-section {
  margin-bottom: 2.5rem;
  border: 1px solid #ebeef5;
  border-radius: 10px;
  padding: 0.75rem 1rem;
  background: #fafafa;
}

.completed-header {
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 500;
  color: #909399;
  user-select: none;
  padding: 0.25rem 0;
  transition: color 0.2s;
}

.completed-header:hover {
  color: #606266;
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

/* Layers */
.layer-section {
  margin-bottom: 3rem;
}

.layer-title {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 1.25rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #ebeef5;
  color: #303133;
}

.task-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
  margin-top: 1rem;
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

/* Responsive */
@media (min-width: 640px) {
  .task-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .task-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 1024px) {
  .todo-container {
    margin: 90px auto 30px;
    padding: 0 15px;
  }
}

@media (max-width: 768px) {
  .todo-container {
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
}

@media (max-width: 480px) {
  .todo-container {
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
