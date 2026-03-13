<script lang="ts" setup>
import {computed, ref} from 'vue'

interface Props {
  tags: string[]
  counts: Record<string, number>
}

const props = defineProps<Props>()

const emit = defineEmits(['tag-selected'])

const activeTag = ref<string | null>(null)

const selectTag = (tag: string | null) => {
  if (activeTag.value === tag) {
    activeTag.value = null
  } else {
    activeTag.value = tag
  }
  emit('tag-selected', activeTag.value)
}

const clearFilter = () => {
  activeTag.value = null
  emit('tag-selected', null)
}

// 计算数值范围，用于动态调整样式
const fontMetrics = computed(() => {
  const countsArray = Object.values(props.counts)
  if (countsArray.length === 0) {
    return {min: 1, max: 1}
  }
  return {
    min: Math.min(...countsArray),
    max: Math.max(...countsArray),
  }
})

// 根据项目数量获取标签样式
const getTagStyle = (count) => {
  const {min, max} = fontMetrics.value
  const basePadding = 1
  const maxPadding = 2.5

  let horizontalPadding
  if (max === min || count === undefined) {
    horizontalPadding = basePadding
  } else {
    const normalized = (count - min) / (max - min)
    horizontalPadding = basePadding + normalized * (maxPadding - basePadding)
  }

  return {
    padding: `0 ${horizontalPadding.toFixed(2)}em`,
  }
}
</script>

<template>
  <el-card class="tag-filter-card" shadow="never">
    <template #header>
      <div class="card-header">
        <span>技术标签</span>
        <el-button v-if="activeTag" link type="primary" @click="clearFilter">清空</el-button>
      </div>
    </template>
    <div v-if="props.tags.length > 0" class="tag-list">
      <el-tag
          v-for="tag in props.tags"
          :key="tag"
          :class="{ 'is-active': activeTag === tag }"
          :style="getTagStyle(props.counts[tag] || 0)"
          class="tag-item"
          effect="light"
          @click="selectTag(tag)"
      >
        {{ tag }} ({{ props.counts[tag] || 0 }})
      </el-tag>
    </div>
    <el-empty v-else :image-size="60" description="暂无标签数据">
    </el-empty>
  </el-card>
</template>

<style scoped>
.tag-filter-card {
  border-radius: 15px;
  border: 1px solid var(--el-border-color-lighter);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
}

.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.tag-item {
  cursor: pointer;
  transition: all 0.2s ease-in-out;
  border: 1px solid var(--el-border-color-light);
  height: auto;
  line-height: 2;
  background-color: #ffffff;
  color: var(--el-text-color-primary);
}

.tag-item:hover {
  background-color: #f5f7fa;
  color: var(--el-color-primary);
}

.tag-item.is-active {
  background-color: var(--el-color-primary);
  color: #fff;
  border-color: var(--el-color-primary);
}
</style>