<template>
  <div class="glass-card">
    <div class="flex justify-between items-center mb-4">
      <h3 class="font-bold text-base text-primary tracking-tight">GitHub 活动</h3>
    </div>
    <div class="github-stats-container">
      <img
        src="https://github-cards.yumeko.site/api/cards/stats?username=NayukiChiba&theme=github"
        alt="NayukiChiba's GitHub Stats"
        loading="lazy"
        class="stats-image"
      />
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.github-stats-container {
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  height: 160px;
  transition: opacity 0.3s ease;
}

.github-stats-container:hover {
  opacity: 0.9;
}

.stats-image {
  max-width: 100%;
  height: 100%;
  object-fit: contain;
}

@media (max-width: 767px) {
  .github-stats-container {
    height: 140px;
    overflow-x: auto;
  }

  .stats-image {
    height: 100%;
    width: auto;
    object-fit: contain;
  }
}
</style>