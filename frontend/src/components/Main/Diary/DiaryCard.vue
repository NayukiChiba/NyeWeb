<template>
  <div class="timeline-item">
    <div class="timeline-marker"></div>
    <div class="timeline-content">
      <div class="diary-summary" @click="isExpanded = !isExpanded">
        <span class="diary-date">{{ displayDate }}</span>
        <span class="diary-mood-preview">{{ moodEmoji }}</span>
        <span class="expand-icon" :class="{ expanded: isExpanded }">▶</span>
      </div>

      <transition name="slide-down">
        <div v-if="isExpanded" class="diary-card-inner">
          <div class="diary-header">
            <div class="meta-group">
              <span class="meta-item" title="日期">📅 {{ displayDate }}</span>
              <span v-if="diary.weather" class="meta-item" title="天气">
                {{ weatherEmoji }}
                <span class="meta-text">{{ diary.weather }}</span>
              </span>
              <span class="meta-item" title="心情">
                {{ moodEmoji }}
                <span class="meta-text">{{ diary.mood || 'neutral' }}</span>
              </span>
            </div>
          </div>
          <div class="diary-body">
            <p>{{ diary.content }}</p>
            <div v-if="validImages.length > 0" class="diary-images">
              <img
                v-for="(img, index) in validImages"
                :key="index"
                :src="img"
                alt="日记附图"
                loading="lazy"
                @click.stop="openLightbox(img)"
              />
            </div>
          </div>
        </div>
      </transition>
    </div>

    <!-- Image Lightbox -->
    <teleport to="body">
      <transition name="fade">
        <div v-if="lightboxVisible" class="diary-lightbox" @click="closeLightbox">
          <div class="diary-lightbox-overlay"></div>
          <div class="diary-lightbox-content" @click.stop>
            <button class="diary-lightbox-close" aria-label="关闭" @click="closeLightbox">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
                   fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                   stroke-linejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
            <img :src="lightboxSrc" alt="放大图片"/>
          </div>
        </div>
      </transition>
    </teleport>
  </div>
</template>

<script setup>
import {computed, ref} from 'vue'

const props = defineProps({
  diary: {
    type: Object,
    required: true,
  },
})

const isExpanded = ref(false)
const lightboxVisible = ref(false)
const lightboxSrc = ref('')

const moodMap = {
  happy: '😊',
  relieved: '😌',
  sad: '😢',
  angry: '😠',
  neutral: '😐',
  excited: '🤩',
  tired: '😫',
}

const weatherMap = {
  sunny: '☀️',
  cloudy: '☁️',
  rainy: '🌧️',
  snowy: '❄️',
  windy: '💨',
}

const displayDate = computed(() => {
  const d = new Date(props.diary.date)
  if (isNaN(d.getTime())) return props.diary.date
  const pad = (n) => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}`
})

const moodEmoji = computed(() => moodMap[props.diary.mood] || '😐')
const weatherEmoji = computed(() => weatherMap[props.diary.weather] || '🌤️')

const validImages = computed(() => {
  return Array.isArray(props.diary.images) ? props.diary.images : []
})

const openLightbox = (src) => {
  lightboxSrc.value = src
  lightboxVisible.value = true
  document.body.style.overflow = 'hidden'
}

const closeLightbox = () => {
  lightboxVisible.value = false
  document.body.style.overflow = ''
}

// Expose expand method for parent
defineExpose({isExpanded})
</script>

<style scoped>
.timeline-item {
  position: relative;
  margin-bottom: 2rem;
}

.timeline-marker {
  position: absolute;
  left: -2.55rem;
  top: 0.4rem;
  width: 12px;
  height: 12px;
  background: #fff;
  border: 3px solid #409eff;
  border-radius: 50%;
  z-index: 1;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.timeline-item:hover .timeline-marker {
  background: #409eff;
  transform: scale(1.2);
  box-shadow: 0 0 0 4px rgba(64, 158, 255, 0.15);
}

.diary-summary {
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem 0;
  font-weight: 600;
  color: #303133;
  transition: all 0.2s ease;
  user-select: none;
}

.diary-summary:hover {
  color: #409eff;
  padding-left: 0.5rem;
}

.diary-date {
  font-size: 1.05rem;
}

.diary-mood-preview {
  font-size: 1.3rem;
  opacity: 0.9;
  transition: transform 0.2s ease;
}

.diary-summary:hover .diary-mood-preview {
  transform: scale(1.15);
}

.expand-icon {
  font-size: 0.7em;
  color: #409eff;
  transition: transform 0.2s ease;
  margin-left: auto;
}

.expand-icon.expanded {
  transform: rotate(90deg);
}

.diary-card-inner {
  margin-top: 1rem;
  background: #fff;
  border: 1px solid #ebeef5;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
  position: relative;
  overflow: visible;
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.3s ease;
}

.diary-card-inner:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
  border-color: #c6e2ff;
}

.diary-header {
  margin-bottom: 1.25rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #f0f2f5;
}

.meta-group {
  display: flex;
  gap: 1.5rem;
  font-size: 0.9rem;
  color: #606266;
  flex-wrap: wrap;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  transition: color 0.2s ease;
}

.meta-item:hover {
  color: #409eff;
}

.meta-text {
  text-transform: capitalize;
}

.diary-body p {
  margin: 0;
  line-height: 1.8;
  color: #606266;
  font-size: 1rem;
  white-space: pre-wrap;
}

.diary-images {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 0.75rem;
  margin-top: 1.25rem;
}

.diary-images img {
  width: 100%;
  height: 120px;
  object-fit: cover;
  border-radius: 8px;
  border: 1px solid #ebeef5;
  cursor: zoom-in;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.diary-images img:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-color: #c6e2ff;
}

/* Slide down transition */
.slide-down-enter-active {
  animation: slideDown 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}

.slide-down-leave-active {
  animation: slideDown 0.25s cubic-bezier(0.4, 0, 0.2, 1) reverse;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-12px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Lightbox */
.diary-lightbox {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
}

.diary-lightbox-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.92);
}

.diary-lightbox-content {
  position: relative;
  z-index: 10000;
  max-width: 90vw;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.diary-lightbox-content img {
  max-width: 100%;
  max-height: 85vh;
  object-fit: contain;
  border-radius: 10px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.6);
}

.diary-lightbox-close {
  position: absolute;
  top: -2rem;
  right: -2rem;
  background: rgba(0, 0, 0, 0.5);
  border: none;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  z-index: 10001;
  backdrop-filter: blur(8px);
}

.diary-lightbox-close:hover {
  background: rgba(220, 38, 38, 0.9);
  transform: scale(1.1);
}

.diary-lightbox-close svg {
  color: white;
}

/* Fade transition for lightbox */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Mobile responsive */
@media (max-width: 768px) {
  .meta-group {
    gap: 1rem;
  }

  .diary-card-inner {
    padding: 1.25rem;
  }

  .diary-lightbox-close {
    top: 1rem;
    right: 1rem;
  }
}
</style>
