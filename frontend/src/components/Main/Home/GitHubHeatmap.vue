<template>
  <div class="glass-card">
    <div class="flex justify-between items-center mb-4">
      <h3 class="font-bold text-base text-primary tracking-tight">GitHub 活动</h3>
    </div>
    <div class="github-chart-container">
      <img
        src="https://activity.yumeko.site/graph?username=NayukiChiba&theme=xcode&bg_color=FF000000&color=000000&hide_border=true"
        alt="NayukiChiba's GitHub Contribution Graph"
        loading="lazy"
        class="chart-image"
      />
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.github-chart-container {
  display: flex;
  align-items: center;
  justify-content: center;
  overflow-x: auto;
  padding: 8px 0;
  transition: opacity 0.3s ease;
}

.github-chart-container:hover {
  opacity: 0.9;
}

.chart-image {
  max-width: 100%;
  height: auto;
}

@media (max-width: 767px) {
  .github-chart-container {
    overflow-x: auto;
  }

  .chart-image {
    min-width: 600px;
  }
}
</style>