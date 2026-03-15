<template>
  <div class="glass-card flex flex-col items-center text-center p-8 relative overflow-visible">
    <!-- Gradient accent at top of card -->
    <div class="absolute top-0 left-0 right-0 h-1 rounded-t-2xl" style="background: linear-gradient(90deg, #6366F1, #EC4899, #F59E0B);"></div>
    
    <div class="relative mb-6">
      <el-avatar :size="100" src="/avatar.jpg" class="ring-3 ring-accent/20 shadow-lg"/>
      <div class="absolute -bottom-1 -right-1 w-6 h-6 rounded-full bg-emerald-400 border-2 border-white shadow-sm"></div>
    </div>
    
    <h2 class="text-xl font-bold text-primary tracking-tight">卟瓿钚</h2>
    <p class="text-secondary text-sm mt-1">一名普通大学生</p>
    
    <div class="flex gap-3 mt-5">
      <a v-for="link in socialLinks" :key="link.title"
        class="w-9 h-9 rounded-xl bg-muted flex items-center justify-center transition-all duration-200 hover:-translate-y-0.5 hover:shadow-md hover:bg-accent hover:text-white group cursor-pointer"
        :href="link.url" target="_blank" :title="link.title">
        <img :src="link.icon" :alt="link.title" class="w-4 h-4 opacity-60 group-hover:opacity-100 group-hover:invert transition-all"/>
      </a>
    </div>

    <div class="w-full h-px bg-border/60 my-5"></div>

    <div class="w-full text-left text-sm text-secondary space-y-2.5">
      <p class="flex items-center gap-2">
        <span class="text-primary/40 text-xs">🏫</span>
        <a href="https://www.whu.edu.cn/" target="_blank" class="text-primary hover:text-accent transition-colors font-medium">武汉大学</a>
      </p>
      <p class="flex items-center gap-2">
        <span class="text-primary/40 text-xs">✉️</span>
        <a href="mailto:NayeyYe@163.com" class="text-primary hover:text-accent transition-colors font-medium">NayeyYe@163.com</a>
      </p>
    </div>
  </div>
</template>

<script setup>
import githubIcon from '/github.svg'
import csdnIcon from '/csdn.svg'
import twitterIcon from '/twitter.svg'

const socialLinks = [
  { url: 'https://github.com/NayukiChiba', icon: githubIcon, title: 'GitHub' },
  { url: 'https://blog.csdn.net/2302_77222155?type=blog', icon: csdnIcon, title: 'CSDN' },
  { url: 'https://x.com/NayukiChiba', icon: twitterIcon, title: 'Twitter' },
]
</script>
