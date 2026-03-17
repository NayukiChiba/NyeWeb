<template>
  <div>
    <div v-if="projects.length > 0" class="admin-grid">
      <ProjectCard v-for="p in projects" :key="p.id" :project="p" @edit="$emit('edit', $event)" @delete="$emit('delete', $event)" @update-status="(t, s) => $emit('update-status', t, s)" @update-visibility="(t, v) => $emit('update-visibility', t, v)"/>
    </div>
    <div v-else class="admin-empty">
      <p>暂无项目数据</p>
    </div>
  </div>
</template>

<script setup>
import ProjectCard from './ProjectCard.vue'
defineProps({ projects: { type: Array, default: () => [] } })
defineEmits(['edit', 'delete', 'update-status', 'update-visibility'])
</script>
