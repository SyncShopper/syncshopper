<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import AppBanner from '@/components/common/AppBanner.vue'
import { recommendationApi } from '@/api/recommendation'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const recommendations = ref([])
const isLoading = ref(true)
const error = ref(null)

const fetchRecommendations = async () => {
  if (!authStore.isLoggedIn) {
    isLoading.value = false
    return
  }

  isLoading.value = true
  error.value = null
  try {
    const result = await recommendationApi.getMyRecommendations(15)
    
    recommendations.value = result.map((item, index) => ({
      productId: item.productId || item.externalProductId || `temp_${index}`,
      externalProductId: item.externalProductId,
      title: item.title,
      brand: item.brand || '쇼핑몰',
      mallName: item.brand || '쇼핑몰',
      price: item.price,
      imageUrl: item.imageUrl,
      link: item.link || item.affiliateUrl || '',
      affiliateUrl: item.link || item.affiliateUrl || '',
      categoryName: item.categoryName,
      keyword: item.keyword,
      source: 'NAVER'
    }))
    
    if (Object.keys(groupedRecommendations.value).length > 0) {
      activeKeyword.value = Object.keys(groupedRecommendations.value)[0]
    }
  } catch (err) {
    console.error('Recommendation fetch failed:', err)
    error.value = '추천 상품을 불러오는 데 실패했습니다.'
  } finally {
    isLoading.value = false
  }
}

const groupedRecommendations = computed(() => {
  const groups = {}
  recommendations.value.forEach(p => {
    const k = p.keyword || '맞춤 추천'
    if (!groups[k]) groups[k] = []
    groups[k].push(p)
  })
  return groups
})

const activeKeyword = ref(null)

const formatPrice = (price) => {
  if (!price) return '가격 정보 없음'
  return price.toLocaleString('ko-KR') + '원'
}

const goToDetail = (product) => {
  if (!product.productId || String(product.productId).startsWith('temp_')) return
  
  router.push({
    path: `/product/${product.productId}`,
    state: {
      productData: JSON.stringify(product),
      sourcePage: 'RECOMMENDATION_PAGE'
    }
  })
}

onMounted(() => {
  fetchRecommendations()
})
</script>

<template>
  <main class="ai-recommend-page">
    <AppBanner 
      title="AI 추천 상품 리스트" 
      subtitle="사용자 맞춤형 인공지능 쇼핑 제안" 
      bgImage="https://picsum.photos/1200/250?random=20" 
    />

    <div class="container">
      <section class="intro-section">
        <h2 class="section-title">AI 맞춤 추천 서비스</h2>
        <p class="intro-text">
          사용자의 관심 카테고리 및 유튜브 시청 기록을 기반으로 분석된 개인 맞춤형 상품 추천 서비스입니다.<br/>
          지금 가장 필요하실 만한 특별한 상품들을 만나보세요.
        </p>

        <!-- 키워드(카테고리) 탭 UI -->
        <div class="keyword-tabs" v-if="Object.keys(groupedRecommendations).length > 0">
          <button 
            v-for="(keyword, index) in Object.keys(groupedRecommendations)" 
            :key="keyword"
            class="tab-btn"
            :class="{ active: activeKeyword === keyword }"
            @click="activeKeyword = keyword"
          >
            <span class="rank-badge">{{ index + 1 }}위</span> {{ keyword }}
          </button>
        </div>
      </section>

      <section class="recommend-list-section">
        <div v-if="!authStore.isLoggedIn" class="login-required-state">
          <p>해당 기능은 로그인 한 회원만 가능합니다.</p>
          <button @click="router.push('/login')" class="login-btn">로그인하러 가기</button>
        </div>

        <div v-else-if="isLoading" class="loading-state">
          <div class="spinner"></div>
          <p>AI가 맞춤형 상품을 분석하고 있습니다...</p>
        </div>
        
        <div v-else-if="error" class="error-state">
          {{ error }}
        </div>

        <div v-else class="recommend-groups">
          <div v-if="recommendations.length === 0" class="empty-state">추천해 드릴 상품이 없습니다.</div>
          
          <div v-if="activeKeyword && groupedRecommendations[activeKeyword]" class="keyword-group">
            <h3 class="keyword-title">
              <i class="fa-solid fa-tag"></i> '{{ activeKeyword }}' 관련 맞춤 추천 상품
            </h3>
            
            <div class="recommend-list">
              <div 
                v-for="product in groupedRecommendations[activeKeyword]" 
                :key="product.productId" 
                class="product-item" 
                @click="goToDetail(product)"
              >
                <!-- 왼쪽 세로로 긴 이미지 영역 -->
                <div class="image-section">
                  <img :src="product.imageUrl" :alt="product.title" loading="lazy" />
                </div>

                <!-- 오른쪽 정보 영역 -->
                <div class="info-section">
                  <div class="product-basic-info">
                    <div class="brand">{{ product.brand }}</div>
                    <h4 class="title" v-html="product.title"></h4>
                    <div class="price">{{ formatPrice(product.price) }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  </main>
</template>

<style scoped>
.ai-recommend-page {
  background-color: #ffffff; /* 깔끔하게 화이트 톤으로 변경 */
  min-height: 100vh;
  padding-bottom: 100px;
}

.container {
  max-width: 1000px; /* 리스트 집중을 위해 폭을 약간 줄임 */
  margin: 0 auto;
  padding: 0 20px;
}

/* Intro Section */
.intro-section {
  text-align: center;
  margin: 60px 0;
}

.section-title {
  font-size: 26px;
  font-weight: 700;
  color: #222;
  margin: 0 0 15px 0;
}

.intro-text {
  font-size: 15px;
  color: #666;
  line-height: 1.6;
  margin: 0 0 30px 0;
}

/* Keyword Tabs */
.keyword-tabs {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-top: 20px;
  flex-wrap: wrap;
}

.tab-btn {
  padding: 10px 25px;
  border-radius: 30px;
  border: 1px solid #ddd;
  background-color: #fff;
  color: #555;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
  display: flex;
  align-items: center;
  gap: 8px;
}

.rank-badge {
  background-color: #ff3f3f;
  color: white;
  font-size: 12px;
  font-weight: bold;
  padding: 2px 8px;
  border-radius: 12px;
}

.tab-btn.active .rank-badge {
  background-color: #fff;
  color: #333;
}

.tab-btn:hover {
  background-color: #f1f1f1;
}

.tab-btn.active {
  background-color: #333;
  color: #fff;
  border-color: #333;
  box-shadow: 0 4px 10px rgba(0,0,0,0.15);
}

/* Recommend List */
.recommend-groups {
  display: flex;
  flex-direction: column;
  gap: 60px;
  margin-top: 40px;
}

.keyword-group {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.keyword-title {
  font-size: 24px;
  font-weight: 700;
  color: #222;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 10px;
  padding-bottom: 10px;
  border-bottom: 2px solid #eaeaea;
}

.keyword-title i {
  color: #ff3f3f;
}

.recommend-list {
  display: flex;
  flex-direction: column;
  gap: 40px; 
}

.product-item {
  display: flex;
  gap: 50px;
  align-items: flex-start;
  cursor: pointer;
  transition: opacity 0.2s;
}

.product-item:hover {
  opacity: 0.8;
}

/* Image Section (세로로 길게) */
.image-section {
  width: 280px;
  aspect-ratio: 3 / 4; /* 세로로 긴 비율 */
  flex-shrink: 0;
  background-color: #f8f8f8;
  border: 1px solid #eaeaea; /* 설계도 느낌처럼 아주 연한 테두리 */
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

.image-section img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Info Section */
.info-section {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  padding-top: 20px;
  flex: 1;
}

.product-basic-info {
  margin-bottom: 40px;
}

.brand {
  font-size: 14px;
  color: #888;
  margin-bottom: 8px;
}

.title {
  font-size: 22px;
  font-weight: 600;
  color: #222;
  margin: 0 0 12px 0;
  line-height: 1.4;
  word-break: keep-all;
}

.price {
  font-size: 20px;
  font-weight: 700;
  color: #222;
}

.login-required-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 0;
  background-color: #f8f9fa;
  border-radius: 12px;
  text-align: center;
  margin-top: 20px;
}

.login-required-state p {
  font-size: 16px;
  color: #333;
  margin-bottom: 20px;
  font-weight: 500;
}

.login-btn {
  padding: 12px 30px;
  background-color: #000;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.login-btn:hover {
  opacity: 0.9;
  transform: translateY(-2px);
}

/* Loading & Error */
.loading-state, .error-state, .empty-state {
  text-align: center;
  padding: 100px 0;
  color: #777;
  font-size: 16px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #333;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 15px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Responsive */
@media (max-width: 768px) {
  .product-item {
    flex-direction: column;
    gap: 30px;
  }

  .image-section {
    width: 100%;
    max-width: 320px;
    margin: 0 auto;
  }
  
  .info-section {
    padding-top: 0;
    text-align: center;
    align-items: center;
  }
}
</style>
