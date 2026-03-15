<template>
  <div class="admin-filter">
    <div class="flex items-center justify-between mb-4">
      <span class="text-sm font-semibold text-primary">筛选条件</span>
      <el-button link size="small" @click="$emit('reset')">重置</el-button>
    </div>
    <div class="flex flex-wrap gap-4 items-center">
      <el-select
        :model-value="filters.tags"
        :multiple-limit="3"
        allow-create filterable multiple
        placeholder="标签筛选"
        size="default"
        style="width: 260px"
        @update:model-value="$emit('update:tags', $event)"
      >
        <el-option v-for="tag in allTags" :key="tag" :label="tag" :value="tag"/>
      </el-select>
      <el-input
        :model-value="filters.title"
        clearable
        placeholder="标题搜索"
        style="width: 200px"
        @update:model-value="$emit('update:title', $event)"
      />
      <el-select
        :model-value="filters.status"
        placeholder="状态"
        style="width: 120px"
        @update:model-value="$emit('update:status', $event)"
      >
        <el-option label="全部" value=""/>
        <el-option label="已发布" value="published"/>
        <el-option label="草稿" value="draft"/>
        <el-option label="已回收" value="recycled"/>
      </el-select>
    </div>
  </div>
</template>

<script setup>
defineProps({
  filters: { type: Object, required: true },
  allTags: { type: Array, default: () => [] }
})
defineEmits(['reset', 'update:tags', 'update:title', 'update:status'])
</script>
