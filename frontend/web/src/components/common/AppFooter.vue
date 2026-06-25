<script setup>
import logoImage from '@/assets/logo.png'
</script>

<template>
  <footer>
    <div class="container">
      <div class="footer-grid">
        <div class="footer-col">
          <div class="footer-logo">
            <img :src="logoImage" alt="CapShop Logo" class="footer-logo-img" />
          </div>
          <p class="footer-desc">CapShop은 스크린샷 한 장으로 원하는 상품을 똑같이 찾아주고, AI 기반 개인 맞춤형 추천을 통해 가장 스마트하고 편리한 쇼핑 경험을 제공하는 혁신적인 플랫폼입니다.</p>
          <div class="footer-checks">
            <label><input type="checkbox" checked disabled> 주소: 서울특별시 강남구</label>
            <label><input type="checkbox" checked disabled> 이메일: contact@domain.com</label>
            <label><input type="checkbox" checked disabled> 핸드폰 번호: 010-1234-5678</label>
          </div>
        </div>
        <div class="footer-col">
          <h4>정보</h4>
          <ul>
            <li><a href="#">회사 소개 문장</a></li>
            <li><a href="#">이용약관 문장</a></li>
            <li><a href="#">개인정보처리방침 문장</a></li>
            <li><a href="#">채용 정보 문장</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4>고객 서비스</h4>
          <ul>
            <li><a href="#">고객센터 문의 문장</a></li>
            <li><a href="#">배송 안내 문장</a></li>
            <li><a href="#">반품 및 교환 안내 문장</a></li>
            <li><a href="#">공지사항 / FAQ 문장</a></li>
          </ul>
        </div>
      </div>

      <div class="footer-bottom">
        <p>Copyright © 2026 CapShop All rights reserved.</p>
        <div class="socials">
          <a href="#"><i class="fa-brands fa-facebook-f"></i></a>
          <a href="#"><i class="fa-brands fa-twitter"></i></a>
          <a href="#"><i class="fa-brands fa-instagram"></i></a>
        </div>
      </div>
    </div>
  </footer>
</template>

<style scoped>
footer {
  background-color: #111111;
  color: #ffffff;
  padding: 80px 0 40px;
}

.footer-grid {
  display: grid;
  grid-template-columns: 1.5fr 1fr 1fr;
  gap: 50px;
  margin-bottom: 60px;
  border-bottom: 1px solid #333333;
  padding-bottom: 60px;
}

.footer-logo {
  margin-bottom: 20px;
}

.footer-logo-img {
  max-height: 35px;
  object-fit: contain;
  filter: brightness(0) invert(1); /* 푸터 배경이 어두우므로 로고를 흰색으로 반전 */
}

.footer-desc {
  font-size: 14px;
  color: #999999;
  margin-bottom: 30px;
  line-height: 1.8;
  max-width: 90%;
}

.footer-checks label {
  display: block;
  margin-bottom: 10px;
  font-size: 14px;
  color: #cccccc;
  cursor: pointer;
}

.footer-checks input {
  margin-right: 8px;
  accent-color: var(--accent-color);
}

.footer-col h4 {
  font-size: 18px;
  font-weight: 500;
  margin-bottom: 25px;
  color: #ffffff;
}

.footer-col ul li {
  margin-bottom: 15px;
  font-size: 14px;
  color: #999999;
}

.footer-col ul li a:hover {
  color: #ffffff;
}

.footer-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 14px;
  color: #777777;
}

.socials {
  display: flex;
  gap: 15px;
}

.socials a {
  color: #777777;
  font-size: 18px;
}

.socials a:hover {
  color: #ffffff;
}
</style>
