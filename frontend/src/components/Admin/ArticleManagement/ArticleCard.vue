<template>
  <div class="admin-card group">
    <div class="flex items-start justify-between mb-2">
      <h3 class="font-bold text-base text-primary truncate flex-1 mr-2">{{ article.title }}</h3>
      <span :class="['status-badge', article.status === 'published' ? 'published' : article.status === 'draft' ? 'draft' : 'recycled']">
        {{ { published: '已发布', draft: '草稿', recycled: '已回收' }[article.status] || '未知' }}
      </span>
    </div>
    <p v-if="article.category" class="text-xs text-accent mb-2">{{ article.category }}</p>
    <p v-if="article.description" class="text-sm text-secondary leading-relaxed line-clamp-2 mb-3">{{ article.description }}</p>
    <div v-if="article.tags && article.tags.length" class="flex flex-wrap gap-1.5 mb-3">
      <span v-for="tag in article.tags.slice(0, 4)" :key="tag" class="tag-pill text-[11px]">{{ tag }}</span>
    </div>
    <p v-if="article.date" class="text-xs text-secondary/50 mb-3">{{ article.date }}</p>
    <div class="pt-3 border-t border-gray-100 flex items-center justify-between">
      <el-select :model-value="article.status" size="small" style="width: 90px" @change="(v) => $emit('update-status', article, v)">
        <el-option label="草稿" value="draft"/><el-option label="已发布" value="published"/><el-option label="已回收" value="recycled"/>
      </el-select>
      <div class="flex gap-2">
        <el-button size="small" @click="$emit('edit', article)">编辑</el-button>
        <el-button v-if="article.status === 'published'" size="small" type="success" @click="$emit('visit', article)">访问</el-button>
        <el-button size="small" type="danger" @click="$emit('delete', article)">删除</el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({ article: { type: Object, required: true } })
defineEmits(['edit', 'delete', 'update-status', 'visit'])
</script>
