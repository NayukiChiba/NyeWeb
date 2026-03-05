<template>
  <a :href="project.link" target="_blank" rel="noopener" class="block group">
    <div class="glass-card flex flex-col h-full group-hover:shadow-glow group-hover:border-accent/30">
      <div class="flex justify-between items-start mb-2">
        <h3 class="font-bold text-base text-primary tracking-tight transition-colors group-hover:text-accent leading-snug">
          {{ project.name }}
        </h3>
        <span class="text-[11px] font-semibold px-2 py-0.5 rounded-full whitespace-nowrap ml-2 flex-shrink-0" :class="statusClass">
          {{ statusLabel }}
        </span>
      </div>
      <p class="text-secondary text-sm leading-relaxed line-clamp-2 mb-4 flex-grow">
        {{ project.description }}
      </p>
      <div class="pt-3 border-t border-gray-100 flex flex-wrap gap-1.5 mt-auto">
        <span v-for="tag in (project.techStack || project.tags || [])" :key="tag" class="tag-pill !text-[11px] !px-2 !py-0.5">{{ tag }}</span>
      </div>
    </div>
  </a>
</template>

<script setup>
import {computed} from 'vue'

const props = defineProps({ project: { type: Object, required: true } })

const statusClass = computed(() => {
  const map = { 
    completed: 'bg-emerald-50 text-emerald-600', 
    'in-progress': 'bg-amber-50 text-amber-600', 
    planning: 'bg-slate-100 text-slate-500' 
  }
  return map[props.project.status] || 'bg-slate-100 text-slate-500'
})

const statusLabel = computed(() => {
  const map = { completed: '已完成', 'in-progress': '进行中', planning: '计划中' }
  return map[props.project.status] || props.project.status
})
</script>
