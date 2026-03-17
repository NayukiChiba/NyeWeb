<template>
  <div class="admin-card group">
    <div class="flex items-start justify-between mb-2">
      <h3 class="font-bold text-base text-primary truncate flex-1 mr-2">{{ project.name }}</h3>
      <span :class="['status-badge', statusClass]">{{ statusText }}</span>
    </div>
    <p v-if="project.description" class="text-sm text-secondary leading-relaxed line-clamp-2 mb-3">
      {{ project.description }}
    </p>
    <a v-if="project.link" :href="project.link" target="_blank" class="text-xs text-accent hover:underline truncate block mb-3">
      {{ project.link }}
    </a>
    <div v-if="project.tech_stack && project.tech_stack.length" class="flex flex-wrap gap-1.5 mb-4">
      <span v-for="tag in project.tech_stack.slice(0, 5)" :key="tag" class="tag-pill text-[11px]">{{ tag }}</span>
      <span v-if="project.tech_stack.length > 5" class="text-xs text-secondary/50">+{{ project.tech_stack.length - 5 }}</span>
    </div>
    <div class="pt-3 border-t border-gray-100 flex items-center justify-between">
      <div class="flex items-center gap-2">
        <el-select :model-value="project.status" size="small" style="width: 110px" @change="(v) => $emit('update-status', project, v)">
          <el-option label="计划中" value="planning"/>
          <el-option label="进行中" value="in-progress"/>
          <el-option label="已完成" value="completed"/>
        </el-select>
        <el-select :model-value="String(project.visibility)" size="small" style="width: 90px" @change="(v) => $emit('update-visibility', project, Number(v))">
          <el-option label="可见" value="1"/>
          <el-option label="隐藏" value="0"/>
        </el-select>
      </div>
      <div class="flex gap-2">
        <el-button size="small" @click="$emit('edit', project)">编辑</el-button>
        <el-button size="small" type="danger" @click="$emit('delete', project)">删除</el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
const props = defineProps({ project: { type: Object, required: true } })
defineEmits(['edit', 'delete', 'update-status', 'update-visibility'])

const statusMap = { planning: '计划中', 'in-progress': '进行中', completed: '已完成' }
const statusClassMap = { planning: 'draft', 'in-progress': 'published', completed: 'published' }
const statusText = computed(() => statusMap[props.project.status] || props.project.status)
const statusClass = computed(() => statusClassMap[props.project.status] || 'draft')
</script>
