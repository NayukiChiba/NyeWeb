<template>
  <div class="task-card" :class="{ 'is-completed': todo.completed }">
    <div class="card-top">
      <span class="icon" v-html="iconContent"></span>
      <span class="priority-badge" :style="priorityStyle">{{ todo.priority || 'medium' }}</span>
    </div>

    <div class="card-content">
      <h3 class="task-title">{{ todo.task }}</h3>
    </div>

    <div class="card-bottom">
      <div class="progress-wrapper">
        <div class="progress-track">
          <div class="progress-fill" :style="{ width: `${todo.progress || 0}%` }"></div>
        </div>
        <span class="progress-text">{{ todo.progress || 0 }}%</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import {computed} from 'vue'

const props = defineProps({
  todo: {
    type: Object,
    required: true,
  },
})

const priorityColors = {
  high: {bg: '#fff1f0', text: '#ff4d4f'},
  medium: {bg: '#fffbe6', text: '#faad14'},
  low: {bg: '#f6ffed', text: '#52c41a'},
}

const priorityStyle = computed(() => {
  const colors = priorityColors[props.todo.priority?.toLowerCase()] || {bg: '#f5f5f5', text: '#888'}
  return {
    backgroundColor: colors.bg,
    color: colors.text,
    borderColor: colors.bg,
  }
})

const iconContent = computed(() => {
  const icon = props.todo.icon
  if (!icon) return '📋'
  if (icon.startsWith('<svg')) return icon
  if (icon.startsWith('http') || icon.startsWith('/')) {
    return `<img src="${icon}" alt="icon" class="task-icon-img" />`
  }
  return icon
})
</script>

<style scoped>
.task-card {
  background: #fff;
  border: 1px solid #ebeef5;
  border-radius: 12px;
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.task-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
  border-color: #c6e2ff;
}

.task-card.is-completed {
  opacity: 0.55;
  background: #fafafa;
}

.task-card.is-completed .task-title {
  text-decoration: line-through;
  color: #909399;
}

.card-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.icon {
  font-size: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon :deep(svg) {
  width: 24px;
  height: 24px;
}

.icon :deep(.task-icon-img) {
  width: 24px;
  height: 24px;
  object-fit: contain;
}

.priority-badge {
  font-size: 0.75rem;
  font-weight: 500;
  text-transform: capitalize;
  border: 1px solid #ebeef5;
  padding: 0.15rem 0.5rem;
  border-radius: 4px;
}

.task-title {
  font-size: 1rem;
  font-weight: 600;
  margin: 0;
  line-height: 1.45;
  color: #303133;
}

.card-bottom {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-top: auto;
}

.progress-wrapper {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.progress-track {
  flex: 1;
  height: 6px;
  background: #f0f2f5;
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #409eff, #337ecc);
  border-radius: 3px;
  transition: width 0.4s ease;
}

.progress-text {
  font-size: 0.75rem;
  color: #909399;
  font-variant-numeric: tabular-nums;
  width: 2.5em;
  text-align: right;
}

@media (max-width: 768px) {
  .task-card {
    padding: 1rem;
  }
}
</style>
