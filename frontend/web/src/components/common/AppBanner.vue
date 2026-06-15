<script setup>
import { computed } from 'vue'

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  subtitle: {
    type: String,
    default: ''
  },
  bgImage: {
    type: String,
    default: ''
  }
})

const bannerStyle = computed(() => {
  if (props.bgImage) {
    return {
      backgroundImage: `linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url(${props.bgImage})`,
      backgroundSize: 'cover',
      backgroundPosition: 'center',
      backgroundRepeat: 'no-repeat'
    }
  }
  // Default gradient if no image is provided
  return {
    background: 'linear-gradient(135deg, #2c3e50, #3498db)'
  }
})
</script>

<template>
  <section class="banner-section" :style="bannerStyle">
    <div class="banner-content">
      <h2>{{ title }}</h2>
      <p v-if="subtitle">{{ subtitle }}</p>
    </div>
  </section>
</template>

<style scoped>
.banner-section {
  width: 100%;
  height: 250px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  margin-bottom: 40px;
}

.banner-content {
  text-align: center;
  padding: 0 20px;
}

.banner-content h2 {
  font-size: 48px;
  font-weight: 800;
  margin-bottom: 10px;
  letter-spacing: 2px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.banner-content p {
  font-size: 16px;
  opacity: 0.9;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}
</style>
