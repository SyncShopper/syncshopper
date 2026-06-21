<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const boardList = ref([])
const searchQuery = ref('')
const currentPage = ref(1)
const totalPages = ref(1)

const fetchPosts = async (page = 1) => {
  try {
    const response = await axios.get('/api/posts', {
      params: {
        page: page,
        size: 10,
        keyword: searchQuery.value
      }
    })
    
    if (response.data && response.data.data) {
      const pageData = response.data.data
      boardList.value = pageData.content.map(post => {
        return {
          id: post.postId,
          date: formatDate(post.createdAt),
          title: post.title,
          detail: post.content || '내용 없음',
          username: '관리자',
          status: post.visibleYn === 'Y' ? '정상' : '숨김',
          category: formatCategory(post.postType)
        }
      })
      currentPage.value = pageData.pageNumber
      totalPages.value = pageData.totalPages || 1
    }
  } catch (error) {
    console.error('Failed to fetch posts:', error)
  }
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
}

const formatCategory = (type) => {
  switch (type) {
    case 'NOTICE': return '공지사항'
    case 'EVENT': return '이벤트'
    case 'FAQ': return 'FAQ'
    default: return type
  }
}

const search = () => {
  fetchPosts(1)
}

const changePage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    fetchPosts(page)
  }
}

onMounted(() => {
  fetchPosts()
})

</script>

<template>
  <div class="admin-board">
    <div class="page-header">
      <h1 class="page-title">Board</h1>
    </div>

    <!-- 데이터 테이블 카드 -->
    <div class="card shadow-sm">
      <div class="card-header">
        <div class="search-area">
          <div class="search-input-wrapper">
            <i class="fa-solid fa-magnifying-glass search-icon"></i>
            <input 
              type="text" 
              class="form-control" 
              placeholder="제목 검색" 
              v-model="searchQuery"
            />
          </div>
          <button class="btn-search" @click="search">검색</button>
        </div>
        <div class="action-area">
          <button class="btn-primary" @click="$router.push('/admin/board/write')">
            <i class="fa-solid fa-pen-to-square"></i> 글 작성 버튼
          </button>
        </div>
      </div>
      
      <div class="card-body p-0">
        <div class="table-responsive">
          <table class="table">
            <thead>
              <tr>
                <th width="8%">ID</th>
                <th width="12%">Date</th>
                <th width="25%">Title</th>
                <th width="25%">Detail</th>
                <th width="10%">Username</th>
                <th width="10%" class="sortable">Status <i class="fa-solid fa-caret-down"></i></th>
                <th width="10%" class="sortable">Category <i class="fa-solid fa-caret-down"></i></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in boardList" :key="item.id" class="table-row">
                <td class="text-center font-weight-bold text-muted">#{{ item.id }}</td>
                <td class="text-muted">{{ item.date }}</td>
                <td class="font-weight-bold text-dark">{{ item.title }}</td>
                <td class="text-truncate text-muted">{{ item.detail }}</td>
                <td>
                  <span class="badge-user">{{ item.username }}</span>
                </td>
                <td>
                  <span class="status-indicator" :class="item.status === '정상' ? 'status-active' : 'status-danger'"></span>
                  {{ item.status }}
                </td>
                <td>
                  <span class="category-badge" :class="{
                    'bg-notice': item.category === '공지사항',
                    'bg-event': item.category === '이벤트',
                    'bg-faq': item.category === 'FAQ'
                  }">
                    {{ item.category }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      
      <!-- 페이지네이션 임시 UI -->
      <div class="card-footer">
        <div class="pagination-wrapper">
          <ul class="pagination">
            <li class="page-item" :class="{ disabled: currentPage === 1 }">
              <a class="page-link" href="#" @click.prevent="changePage(currentPage - 1)">이전</a>
            </li>
            <li class="page-item" v-for="page in totalPages" :key="page" :class="{ active: currentPage === page }">
              <a class="page-link" href="#" @click.prevent="changePage(page)">{{ page }}</a>
            </li>
            <li class="page-item" :class="{ disabled: currentPage === totalPages }">
              <a class="page-link" href="#" @click.prevent="changePage(currentPage + 1)">다음</a>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.admin-board {
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
.card {
  background-color: #ffffff;
  border-radius: 16px;
  border: none;
  display: flex;
  flex-direction: column;
}

.shadow-sm {
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px;
  border-bottom: 1px solid #f2f2f2;
}

/* Search Area */
.search-area {
  display: flex;
  gap: 12px;
}

.search-input-wrapper {
  position: relative;
  width: 250px;
}

.search-icon {
  position: absolute;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  color: #a0a0a0;
  font-size: 14px;
}

.form-control {
  width: 100%;
  padding: 10px 14px 10px 40px;
  border: 1px solid #e1e1e1;
  border-radius: 8px;
  font-size: 14px;
  color: #333;
  transition: border-color 0.2s;
  box-sizing: border-box;
}

.form-control:focus {
  outline: none;
  border-color: #3b4cb8;
}

/* Buttons */
.btn-search {
  padding: 10px 20px;
  background-color: #f0f2f5;
  color: #555;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-search:hover {
  background-color: #e4e6eb;
}

.btn-primary {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background-color: #3b4cb8;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 4px 10px rgba(59, 76, 184, 0.2);
  transition: all 0.2s;
}

.btn-primary:hover {
  background-color: #2f3e9c;
  transform: translateY(-1px);
}

/* Table Styles */
.card-body.p-0 {
  padding: 0;
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

.table th.sortable {
  cursor: pointer;
}

.table th.sortable:hover {
  color: #3b4cb8;
}

.table td {
  padding: 18px 24px;
  font-size: 14px;
  border-bottom: 1px solid #f2f2f2;
  vertical-align: middle;
}

.table-row {
  cursor: pointer;
  transition: background-color 0.2s;
}

.table-row:hover {
  background-color: #f8f9fe;
}

.table-row:last-child td {
  border-bottom: none;
}

/* Text & Badges Helpers */
.text-center { text-align: center; }
.font-weight-bold { font-weight: 600; }
.text-muted { color: #888; }
.text-dark { color: #333; }
.text-truncate {
  max-width: 200px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  display: inline-block;
}

.badge-user {
  display: inline-block;
  padding: 4px 10px;
  background-color: #f0f2f5;
  color: #555;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
}

.status-indicator {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-right: 6px;
}

.status-active { background-color: #2dc447; }
.status-danger { background-color: #e74c3c; }

.category-badge {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
}

.bg-notice { background-color: #eef2ff; color: #4361ee; }
.bg-event { background-color: #fff0f6; color: #eb2f96; }
.bg-faq { background-color: #f6ffed; color: #52c41a; }

/* Pagination */
.card-footer {
  padding: 20px 24px;
  border-top: 1px solid #f2f2f2;
  display: flex;
  justify-content: flex-end;
}

.pagination {
  display: flex;
  list-style: none;
  padding: 0;
  margin: 0;
  gap: 8px;
}

.page-link {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background-color: #ffffff;
  border: 1px solid #e1e1e1;
  color: #555;
  text-decoration: none;
  font-size: 13px;
  font-weight: 500;
  transition: all 0.2s;
}

.page-link:hover {
  background-color: #f0f2f5;
}

.page-item.active .page-link {
  background-color: #3b4cb8;
  color: white;
  border-color: #3b4cb8;
}

.page-item.disabled .page-link {
  color: #ccc;
  background-color: #fafbfc;
  cursor: not-allowed;
}
</style>
