<template>
  <div class="admin-card group">
    <!-- Header -->
    <div class="flex items-start justify-between mb-3">
      <h3 class="font-bold text-base text-primary truncate flex-1 mr-2">{{ tool.name }}</h3>
      <span :class="['status-badge', tool.status]">
        {{ statusText }}
      </span>
    </div>

    <!-- URL -->
    <a v-if="tool.url" :href="tool.url" target="_blank"
       class="text-xs text-accent hover:underline truncate block mb-3">
      {{ tool.url }}
    </a>

    <!-- Description -->
    <p v-if="tool.description" class="text-sm text-secondary leading-relaxed line-clamp-2 mb-3">
      {{ tool.description }}
    </p>

    <!-- Tags -->
    <div v-if="tool.tags && tool.tags.length" class="flex flex-wrap gap-1.5 mb-4">
      <span v-for="tag in tool.tags.slice(0, 4)" :key="tag" class="tag-pill text-[11px]">{{ tag }}</span>
      <span v-if="tool.tags.length > 4" class="text-xs text-secondary/50">+{{ tool.tags.length - 4 }}</span>
    </div>

    <!-- Divider + Actions -->
    <div class="pt-3 border-t border-gray-100 flex items-center justify-between">
      <el-select
        :model-value="tool.status"
        size="small"
        style="width: 90px"
        @change="(val) => $emit('update-status', tool, val)"
      >
        <el-option label="草稿" value="draft"/>
        <el-option label="已发布" value="published"/>
        <el-option label="已回收" value="recycled"/>
      </el-select>
      <div class="flex gap-2">
        <el-button size="small" @click="$emit('edit', tool)">编辑</el-button>
        <el-button size="small" type="danger" @click="$emit('delete', tool)">删除</el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  tool: { type: Object, required: true }
})

defineEmits(['edit', 'delete', 'update-status'])

const statusText = computed(() => {
  const map = { published: '已发布', draft: '草稿', recycled: '已回收' }
  return map[props.tool.status] || '未知'
})
</script>
