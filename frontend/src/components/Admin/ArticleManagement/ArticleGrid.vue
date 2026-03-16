<template>
  <div>
    <div v-if="articles.length > 0" class="admin-grid">
      <ArticleCard v-for="a in articles" :key="a.id" :article="a" @edit="$emit('edit', $event)" @delete="$emit('delete', $event)" @update-status="(t, s) => $emit('update-status', t, s)" @visit="$emit('visit', $event)"/>
    </div>
    <div v-else class="text-center py-12 text-secondary/60">
      <p class="text-lg mb-1">📝</p>
      <p class="text-sm">暂无文章数据</p>
    </div>
  </div>
</template>

<script setup>
import ArticleCard from './ArticleCard.vue'
defineProps({ articles: { type: Array, default: () => [] } })
defineEmits(['edit', 'delete', 'update-status', 'visit'])
</script>
