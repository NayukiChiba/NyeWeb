<template>
  <a :href="project.link" target="_blank" rel="noopener" class="card-link">
    <el-card class="project-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <span>{{ project.name }}</span>
          <el-tag v-if="project.status" :type="statusType" size="small" effect="plain" round>
            {{ statusLabel }}
          </el-tag>
        </div>
      </template>
      <div class="card-summary">
        <p>{{ project.description }}</p>
      </div>
      <div class="card-footer">
        <div class="project-tags">
          <el-tag
              v-for="tag in (project.techStack || project.tags || [])"
              :key="tag"
              effect="plain"
              round
              size="small"
              type="info"
          >
            {{ tag }}
          </el-tag>
        </div>
      </div>
    </el-card>
  </a>
</template>

<script setup>
import {computed} from 'vue'

const props = defineProps({
  project: {
    type: Object,
    required: true
  }
})

const statusType = computed(() => {
  const map = { completed: 'success', 'in-progress': 'warning', planning: 'info' }
  return map[props.project.status] || 'info'
})

const statusLabel = computed(() => {
  const map = { completed: '已完成', 'in-progress': '进行中', planning: '计划中' }
  return map[props.project.status] || props.project.status
})
</script>

<style scoped>
.project-card {
  height: 100%;
  display: flex;
  flex-direction: column;
  border-radius: 15px;
  border: 1px solid var(--el-border-color-lighter);
}

.card-link {
  text-decoration: none;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header span {
  font-weight: bold;
  font-size: 1.1em;
  color: #303133;
}

.card-summary {
  flex-grow: 1;
  color: #606266;
  font-size: 0.9em;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 3;
  overflow: hidden;
  text-overflow: ellipsis;
  min-height: 63px;
}

.card-footer {
  margin-top: 15px;
  padding-top: 10px;
  border-top: 1px solid #ebeef5;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.project-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
</style>
