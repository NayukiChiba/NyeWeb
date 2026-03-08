<template>
  <a :href="tool.url" class="tool-link" rel="noopener noreferrer" target="_blank">
    <div class="glass-card !p-4 flex items-start gap-3 group cursor-pointer">
      <span v-if="tool.icon" class="tool-icon flex-shrink-0 w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-50 to-pink-50 flex items-center justify-center" v-html="tool.icon"></span>
      <div class="flex-1 min-w-0">
        <h3 class="text-sm font-semibold text-primary group-hover:text-accent transition-colors leading-snug mb-1">{{ tool.name }}</h3>
        <p class="text-xs text-secondary leading-relaxed line-clamp-2 mb-2">{{ tool.description }}</p>
        <span v-if="tool.category" class="tag-pill text-[10px]">{{ tool.category }}</span>
      </div>
      <svg class="w-4 h-4 text-secondary/30 group-hover:text-accent transition-colors flex-shrink-0 mt-1" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 6H5.25A2.25 2.25 0 003 8.25v10.5A2.25 2.25 0 005.25 21h10.5A2.25 2.25 0 0018 18.75V10.5m-10.5 6L21 3m0 0h-5.25M21 3v5.25" />
      </svg>
    </div>
  </a>
</template>

<script setup>
defineProps({
  tool: {
    type: Object,
    required: true,
  },
});
</script>

<style scoped>
.tool-link {
  text-decoration: none;
  color: inherit;
  display: block;
}

.tool-icon :deep(svg) {
  width: 20px;
  height: 20px;
  color: #6366f1;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
