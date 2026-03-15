<script setup>
import Header from '@/components/Header.vue'
</script>

<template>
  <div class="relative min-h-screen font-sans antialiased flex flex-col bg-white text-primary">
    <!-- Top gradient accent bar -->
    <div class="fixed top-0 left-0 right-0 h-1 z-[60]" style="background: linear-gradient(90deg, #6366F1 0%, #EC4899 40%, #F59E0B 70%, #10B981 100%);"></div>

    <!-- Subtle ambient shapes -->
    <div class="fixed inset-0 z-0 pointer-events-none overflow-hidden">
      <div class="absolute -top-40 -right-40 w-[600px] h-[600px] rounded-full opacity-[0.04]" style="background: radial-gradient(circle, #6366F1, transparent 70%);"></div>
      <div class="absolute top-1/2 -left-40 w-[500px] h-[500px] rounded-full opacity-[0.03]" style="background: radial-gradient(circle, #EC4899, transparent 70%);"></div>
      <div class="absolute -bottom-20 right-1/3 w-[400px] h-[400px] rounded-full opacity-[0.03]" style="background: radial-gradient(circle, #F59E0B, transparent 70%);"></div>
    </div>

    <Header/>
    <main class="flex-grow w-full max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-8 pt-24 pb-16 relative z-10">
      <router-view/>
    </main>

    <!-- Footer -->
    <footer class="relative z-10 border-t border-gray-100 mt-auto">
      <div class="max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div class="flex flex-col sm:flex-row items-center justify-between gap-4">
          <span class="text-sm text-secondary">© 2024 NayukiWeb — Built with curiosity.</span>
          <div class="flex gap-6">
            <a href="https://github.com/NayukiChiba" target="_blank" class="text-secondary hover:text-accent transition-colors text-sm">GitHub</a>
            <a href="mailto:NayukiChiba@163.com" class="text-secondary hover:text-accent transition-colors text-sm">Email</a>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>
