<script setup>
import { ref, onMounted } from 'vue'
import { RouterView } from 'vue-router'
import AppHeader from './components/common/AppHeader.vue'
import AppFooter from './components/common/AppFooter.vue'
import SearchModal from './components/common/SearchModal.vue'
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()

// 어드민 페이지 여부 확인
const isAdminRoute = computed(() => {
  return route.path.startsWith('/admin')
})

const isSearchModalOpen = ref(false)
const authStore = useAuthStore()

onMounted(() => {
  authStore.init()
})
</script>

<template>
  <template v-if="!isAdminRoute">
    <AppHeader @open-search="isSearchModalOpen = true" />
  </template>
  
  <RouterView />

  <template v-if="!isAdminRoute">
    <AppFooter />
    <SearchModal v-model="isSearchModalOpen" />
  </template>
</template>

<style scoped>
</style>
