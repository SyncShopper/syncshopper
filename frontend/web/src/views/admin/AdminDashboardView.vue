<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'
import { Bar, Doughnut } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement)

const authStore = useAuthStore()

// KPI Data
const kpiData = ref([
  { title: '수익', value: '$10.0k', icon: 'fa-solid fa-dollar-sign', color: '#4361ee' },
  { title: '새로운 고객', value: '2,000', icon: 'fa-solid fa-user-plus', color: '#2dc447' },
  { title: '주문', value: '1,500', icon: 'fa-solid fa-box', color: '#f39c12' },
  { title: '전환율', value: '10.5%', icon: 'fa-solid fa-chart-line', color: '#e74c3c' }
])

// Chart Data (Mock)
const barChartData = ref({
  labels: ['1월', '2월', '3월', '4월', '5월', '6월'],
  datasets: [
    {
      label: '월별 수익',
      backgroundColor: '#4361ee',
      data: [4000, 2000, 12000, 3900, 10000, 8000]
    }
  ]
})

const barChartOptions = ref({
  responsive: true,
  maintainAspectRatio: false,
})

const doughnutChartData = ref({
  labels: ['의류', '전자제품', '식품', '기타'],
  datasets: [
    {
      backgroundColor: ['#4361ee', '#2dc447', '#f39c12', '#e74c3c'],
      data: [40, 20, 30, 10]
    }
  ]
})

const doughnutChartOptions = ref({
  responsive: true,
  maintainAspectRatio: false,
})

// List Data
const recentUsers = ref([])
const recentPosts = ref([])

const fetchRecentUsers = async () => {
  try {
    const token = localStorage.getItem('accessToken')
    const response = await axios.get('/api/admin/users', {
      params: { page: 1, size: 5 },
      headers: { Authorization: `Bearer ${token}` }
    })
    
    if (response.data && response.data.data) {
      const users = response.data.data.content || []
      recentUsers.value = users.slice(0, 5).map(user => ({
        id: user.id,
        date: formatDate(user.createdAt),
        name: user.nickname || 'Unknown',
        email: user.email,
        phone: user.phone || '없음',
        status: user.status === 'ACTIVE' ? '정상' : '삭제',
      }))
    }
  } catch (error) {
    console.error('Failed to fetch recent users:', error)
  }
}

const fetchRecentPosts = async () => {
  try {
    const response = await axios.get('/api/posts', {
      params: { page: 1, size: 5 }
    })
    
    if (response.data && response.data.data) {
      const posts = response.data.data.content || []
      recentPosts.value = posts.slice(0, 5).map(post => ({
        id: post.postId,
        date: formatDate(post.createdAt),
        title: post.title,
        category: formatCategory(post.postType),
        status: post.visibleYn === 'Y' ? '정상' : '숨김',
      }))
    }
  } catch (error) {
    console.error('Failed to fetch recent posts:', error)
  }
}

const formatCategory = (type) => {
  switch (type) {
    case 'NOTICE': return '공지사항'
    case 'EVENT': return '이벤트'
    case 'FAQ': return 'FAQ'
    default: return type
  }
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
}

onMounted(() => {
  fetchRecentUsers()
  fetchRecentPosts()
})

</script>

<template>
  <div class="admin-dashboard">
    <div class="page-header">
      <h1 class="page-title">Dashboard</h1>
    </div>

    <!-- KPI Cards -->
    <div class="kpi-grid">
      <div class="kpi-card shadow-sm" v-for="(item, index) in kpiData" :key="index">
        <div class="kpi-info">
          <div class="kpi-title">{{ item.title }}</div>
          <div class="kpi-value">{{ item.value }}</div>
        </div>
        <div class="kpi-icon" :style="{ backgroundColor: item.color + '1A', color: item.color }">
          <i :class="item.icon"></i>
        </div>
      </div>
    </div>

    <!-- Charts -->
    <div class="chart-grid">
      <div class="chart-card shadow-sm">
        <h3 class="chart-title">수익 막대 그래프</h3>
        <div class="chart-container">
          <Bar :data="barChartData" :options="barChartOptions" />
        </div>
      </div>
      <div class="chart-card shadow-sm">
        <h3 class="chart-title">품목별 매출 비중</h3>
        <div class="chart-container">
          <Doughnut :data="doughnutChartData" :options="doughnutChartOptions" />
        </div>
      </div>
      <div class="chart-card shadow-sm map-placeholder">
        <h3 class="chart-title">지역별 접속 트래픽 (준비중)</h3>
        <div class="map-dummy">
          <i class="fa-solid fa-map-location-dot map-icon"></i>
          <p>지역별 데이터 연동 예정</p>
        </div>
      </div>
    </div>

    <!-- Lists -->
    <div class="list-grid">
      <!-- Recent Users -->
      <div class="list-card shadow-sm">
        <div class="list-header">
          <h3 class="list-title">최신 고객 추가 리스트</h3>
        </div>
        <div class="table-responsive">
          <table class="table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Date</th>
                <th>User</th>
                <th>Email</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in recentUsers" :key="user.id" class="table-row-static">
                <td class="text-center font-weight-bold text-muted">#{{ user.id }}</td>
                <td class="text-muted">{{ user.date }}</td>
                <td class="font-weight-bold text-dark">{{ user.name }}</td>
                <td class="text-muted">{{ user.email }}</td>
                <td>
                  <span class="status-indicator" :class="user.status === '정상' ? 'status-active' : 'status-danger'"></span>
                  {{ user.status }}
                </td>
              </tr>
              <tr v-if="recentUsers.length === 0">
                <td colspan="5" class="text-center py-4 text-muted">데이터가 없습니다.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Recent Data (Posts) -->
      <div class="list-card shadow-sm">
        <div class="list-header">
          <h3 class="list-title">최신 게시글 (공지사항/FAQ/이벤트)</h3>
        </div>
        <div class="table-responsive">
          <table class="table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Date</th>
                <th>Title</th>
                <th>Category</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="post in recentPosts" :key="post.id" class="table-row-static">
                <td class="text-center font-weight-bold text-muted">#{{ post.id }}</td>
                <td class="text-muted">{{ post.date }}</td>
                <td class="font-weight-bold text-dark text-truncate" style="max-width: 150px;">{{ post.title }}</td>
                <td class="text-muted">
                  <span class="category-badge" :class="{
                    'bg-notice': post.category === '공지사항',
                    'bg-event': post.category === '이벤트',
                    'bg-faq': post.category === 'FAQ'
                  }">
                    {{ post.category }}
                  </span>
                </td>
                <td>
                  <span class="status-indicator" :class="post.status === '정상' ? 'status-active' : 'status-danger'"></span>
                  {{ post.status }}
                </td>
              </tr>
              <tr v-if="recentPosts.length === 0">
                <td colspan="5" class="text-center py-4 text-muted">데이터가 없습니다.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.admin-dashboard {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.page-title {
  font-size: 24px;
  font-weight: 700;
  color: #2c2c2c;
  margin: 0;
}

/* Card UI */
.shadow-sm {
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
}

/* KPI Grid */
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
}

.kpi-card {
  background-color: #ffffff;
  border-radius: 16px;
  padding: 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.kpi-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.kpi-title {
  font-size: 14px;
  color: #888;
  font-weight: 500;
}

.kpi-value {
  font-size: 28px;
  font-weight: 700;
  color: #333;
}

.kpi-icon {
  width: 54px;
  height: 54px;
  border-radius: 12px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 24px;
}

/* Chart Grid */
.chart-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.chart-card {
  background-color: #ffffff;
  border-radius: 16px;
  padding: 24px;
  height: 350px;
  display: flex;
  flex-direction: column;
}

.chart-title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin-bottom: 20px;
  margin-top: 0;
}

.chart-container {
  flex: 1;
  position: relative;
  width: 100%;
}

.map-dummy {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%;
  color: #a0a0a0;
  background-color: #fafbfc;
  border-radius: 12px;
  border: 1px dashed #e1e1e1;
}

.map-icon {
  font-size: 48px;
  margin-bottom: 16px;
  color: #e1e1e1;
}

/* List Grid */
.list-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}

.list-card {
  background-color: #ffffff;
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.list-header {
  padding: 20px 24px;
  border-bottom: 1px solid #f2f2f2;
}

.list-title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.table-responsive {
  width: 100%;
  overflow-x: auto;
}

.table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

.table th {
  padding: 16px 24px;
  font-size: 13px;
  font-weight: 600;
  color: #888;
  background-color: #fafbfc;
  border-bottom: 1px solid #f2f2f2;
}

.table td {
  padding: 16px 24px;
  font-size: 14px;
  border-bottom: 1px solid #f2f2f2;
  vertical-align: middle;
}

.table-row-static {
  transition: background-color 0.2s;
}

.table-row-static:hover {
  background-color: #f8f9fe;
}

.table-row-static:last-child td {
  border-bottom: none;
}

/* Helpers */
.text-center { text-align: center; }
.font-weight-bold { font-weight: 600; }
.text-muted { color: #888; }
.text-dark { color: #333; }
.py-4 { padding-top: 1.5rem; padding-bottom: 1.5rem; }

.status-indicator {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-right: 6px;
}

.status-active { background-color: #2dc447; }
.status-danger { background-color: #e74c3c; }
.status-warning { background-color: #f39c12; }

/* Responsive adjustments */
@media (max-width: 1400px) {
  .chart-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .map-placeholder {
    grid-column: span 2;
  }
}

@media (max-width: 1200px) {
  .kpi-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .list-grid {
    grid-template-columns: 1fr;
  }
}
</style>
