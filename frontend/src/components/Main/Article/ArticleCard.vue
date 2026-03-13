<template>
  <router-link :to="articleLink" class="block group">
    <div class="glass-card flex flex-col h-full group-hover:shadow-glow group-hover:border-accent/30">
      <!-- Title with gradient hover -->
      <h3 class="font-bold text-base text-primary mb-2 tracking-tight transition-colors group-hover:text-accent leading-snug">
        {{ article.title }}
      </h3>
      <!-- Summary -->
      <p class="text-secondary text-sm leading-relaxed line-clamp-2 mb-4 flex-grow">
        {{ article.description }}
      </p>
      <!-- Footer -->
      <div class="pt-3 border-t border-gray-100 flex justify-between items-center mt-auto">
        <div class="flex flex-wrap gap-1.5">
          <span v-for="tag in article.tags" :key="tag" class="tag-pill !text-[11px] !px-2 !py-0.5">{{ tag }}</span>
        </div>
        <span class="text-xs text-secondary/60 whitespace-nowrap ml-3 tabular-nums">{{ article.date }}</span>
      </div>
    </div>
  </router-link>
</template>

<script setup>
import {computed} from 'vue'

const props = defineProps({ article: { type: Object, required: true } })

const articleLink = computed(() => {
  return `/articles/${props.article.slug}`
})
</script>
