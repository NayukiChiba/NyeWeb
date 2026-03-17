<template>
  <div>
    <div v-if="tools.length > 0" class="admin-grid">
      <ToolCard
        v-for="tool in tools"
        :key="tool.id"
        :tool="tool"
        @edit="$emit('edit', $event)"
        @delete="$emit('delete', $event)"
        @update-status="(t, s) => $emit('update-status', t, s)"
      />
    </div>
    <div v-else class="admin-empty">
      <p>暂无工具数据</p>
    </div>
  </div>
</template>

<script setup>
import ToolCard from './ToolCard.vue'

defineProps({
  tools: { type: Array, default: () => [] }
})
defineEmits(['edit', 'delete', 'update-status'])
</script>
