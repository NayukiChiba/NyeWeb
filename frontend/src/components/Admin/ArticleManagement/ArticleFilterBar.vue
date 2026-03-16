<template>
  <div class="admin-filter">
    <div class="flex items-center justify-between mb-4">
      <span class="text-sm font-semibold text-primary">筛选条件</span>
      <el-button link size="small" @click="$emit('reset')">重置</el-button>
    </div>
    <div class="flex flex-wrap gap-4 items-center">
      <el-input :model-value="filters.category" clearable placeholder="分类路径" style="width: 180px" @update:model-value="$emit('update:category', $event)"/>
      <el-input :model-value="filters.title" clearable placeholder="标题搜索" style="width: 180px" @update:model-value="$emit('update:title', $event)"/>
      <el-select :model-value="filters.status" placeholder="状态" style="width: 120px" @update:model-value="$emit('update:status', $event)">
        <el-option label="全部" value=""/><el-option label="已发布" value="published"/><el-option label="草稿" value="draft"/><el-option label="已回收" value="recycled"/>
      </el-select>
      <el-select :model-value="sortOrder" placeholder="排序" style="width: 120px" @update:model-value="$emit('update:sortOrder', $event)">
        <el-option label="最新优先" value="desc"/><el-option label="最早优先" value="asc"/>
      </el-select>
    </div>
  </div>
</template>

<script setup>
defineProps({ filters: Object, sortOrder: String })
defineEmits(['reset', 'update:category', 'update:title', 'update:status', 'update:sortOrder'])
</script>
