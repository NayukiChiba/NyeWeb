<script setup>
import {computed, ref, onMounted, onUnmounted} from 'vue'
import {useRoute} from 'vue-router'
import {Menu as IconMenu, Close as IconClose} from '@element-plus/icons-vue'

const route = useRoute()
const isAdminPage = computed(() => route.path.startsWith('/admin'))
const isAdminLogin = computed(() => route.path === '/admin/login')
const isHeaderVisible = ref(true)
let lastScrollTop = 0
const scrolled = ref(false)

const handleScroll = () => {
  const scrollTop = window.pageYOffset || document.documentElement.scrollTop
  scrolled.value = scrollTop > 10
  if (scrollTop > lastScrollTop && scrollTop > 100) {
    isHeaderVisible.value = false
  } else if (scrollTop < lastScrollTop) {
    isHeaderVisible.value = true
  }
  lastScrollTop = scrollTop
}

const isMenuOpen = ref(false)
const toggleMenu = () => { isMenuOpen.value = !isMenuOpen.value }
const closeMenu = () => { isMenuOpen.value = false }

onMounted(() => { window.addEventListener('scroll', handleScroll) })
onUnmounted(() => { window.removeEventListener('scroll', handleScroll) })
</script>

<template>
  <header
    v-if="!isAdminPage || isAdminLogin"
    :class="[
      'fixed top-1 left-4 right-4 z-50 transition-all duration-500 ease-out rounded-2xl',
      isHeaderVisible ? 'translate-y-0 opacity-100' : '-translate-y-full opacity-0',
      scrolled ? 'bg-white/90 backdrop-blur-xl shadow-lg border border-gray-200/50' : 'bg-transparent'
    ]"
  >
    <div class="max-w-[1400px] mx-auto px-6">
      <div class="flex justify-between items-center h-14">

        <!-- Logo -->
        <router-link to="/" class="group flex items-center gap-2">
          <div class="w-8 h-8 rounded-lg flex items-center justify-center text-white font-bold text-sm" style="background: linear-gradient(135deg, #6366F1, #EC4899);">N</div>
          <span class="font-heading font-bold text-lg tracking-tight text-primary">NayukiWeb</span>
        </router-link>

        <!-- Desktop Nav -->
        <nav v-if="!isAdminLogin" class="hidden md:flex items-center gap-1">
          <router-link v-for="item in [
            {to: '/', label: '首页'},
            {to: '/projects', label: '项目'},
            {to: '/articles', label: '文章'},
            {to: '/diary', label: '日记'},
            {to: '/todo', label: '待办'},
            {to: '/tools', label: '工具'},
            {to: '/resources', label: '资源'},
          ]" :key="item.to" :to="item.to"
            class="px-3 py-1.5 text-sm font-medium text-secondary hover:text-primary hover:bg-muted rounded-lg transition-all duration-200"
            active-class="!text-accent !bg-accent/5"
          >{{ item.label }}</router-link>
        </nav>

        <!-- Right -->
        <div class="hidden md:flex items-center gap-4">
          <router-link v-if="!isAdminLogin" to="/about" class="text-sm font-medium text-secondary hover:text-accent transition-colors">关于我</router-link>
          <router-link to="/admin/login" class="flex-shrink-0 group">
            <div class="w-8 h-8 rounded-full overflow-hidden ring-2 ring-border group-hover:ring-accent transition-all duration-200">
              <img src="/avatar.jpg" alt="Avatar" class="w-full h-full object-cover" @error="(e) => e.target.style.display='none'"/>
            </div>
          </router-link>
        </div>

        <!-- Mobile Button -->
        <div v-if="!isAdminLogin" class="flex items-center md:hidden">
          <button @click="toggleMenu" class="text-secondary hover:text-primary outline-none transition-colors cursor-pointer p-1 rounded-lg hover:bg-muted">
            <el-icon :size="22">
              <IconClose v-if="isMenuOpen" />
              <IconMenu v-else />
            </el-icon>
          </button>
        </div>
      </div>
    </div>

    <!-- Mobile Nav -->
    <div v-if="isMenuOpen && !isAdminLogin" class="md:hidden border-t border-gray-100 bg-white rounded-b-2xl">
      <div class="px-6 py-4 flex flex-col gap-1">
        <router-link v-for="item in [
          {to: '/', label: '首页'}, {to: '/projects', label: '项目'}, {to: '/articles', label: '文章'},
          {to: '/diary', label: '日记'}, {to: '/todo', label: '待办'}, {to: '/tools', label: '工具'},
          {to: '/resources', label: '资源'}, {to: '/about', label: '关于我'},
        ]" :key="item.to" :to="item.to" @click="closeMenu"
          class="block px-3 py-2 text-base font-medium text-primary hover:text-accent hover:bg-muted rounded-lg transition-all"
        >{{ item.label }}</router-link>
      </div>
    </div>
  </header>
</template>
