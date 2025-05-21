<template>
  <a :href="tool.url" class="tool-card-link" rel="noopener noreferrer" target="_blank">
    <el-card class="tool-card" shadow="hover">
      <div class="card-content">
        <div class="tool-header">
          <span v-if="tool.icon" class="tool-icon" v-html="tool.icon"></span>
          <h3 class="tool-title">{{ tool.name }}</h3>
        </div>
        <p class="tool-description">{{ tool.description }}</p>
        <div v-if="tool.category" class="tool-category">
          <el-tag size="small" type="info" effect="plain" round>{{ tool.category }}</el-tag>
        </div>
      </div>
    </el-card>
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
.tool-card-link {
  text-decoration: none;
  color: inherit;
  display: block;
  height: 100%;
}

.tool-card {
  border-radius: 15px;
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
  height: 100%;
}

.tool-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--el-box-shadow-light);
}

.card-content {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.tool-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;
}

.tool-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  flex-shrink: 0;
}

.tool-icon :deep(svg) {
  width: 20px;
  height: 20px;
  color: var(--el-color-primary);
}

.tool-title {
  font-size: 1.2em;
  font-weight: bold;
  margin: 0;
}

.tool-description {
  font-size: 0.9em;
  color: var(--el-text-color-secondary);
  flex-grow: 1;
  margin-bottom: 15px;
}

.tool-category {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
</style>
