<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import * as echarts from 'echarts'
import type { Shop } from '@/types'
import { formatPrice, getRatingLevel, SOURCE_LABELS, CATEGORY_COLORS } from '@/utils/format'

const route = useRoute()
const router = useRouter()
const shopId = computed(() => route.params.shopId as string)

// ── Mock data ──
const shop = ref<Shop>({
  shopId: 'dp_001',
  name: '老三样',
  category: 'jiangxi',
  categoryName: '江西菜',
  rating: 4.8,
  priceAvg: 65,
  address: '南昌市西湖区中山路123号',
  longitude: 115.889,
  latitude: 28.684,
  phone: '0791-12345678',
  businessHours: '11:00-14:00, 17:00-21:00',
  tags: ['网红店', '江西菜', '排队王', '必吃榜', '赣菜'],
  source: 'dianping',
  viewCount: 15234,
  shopImage: '',
  images: [],
  foodImages: [],
  videoUrl: '',
  likeCount: 2345,
  commentCount: 890,
  costPerformance: 7.4,
  rank: 1,
  createTime: '2025-05-20 10:00:00',
  updateTime: '2025-05-29 15:30:00',
})

const nearbySpots = [
  { name: '滕王阁', distance: 1.2 },
  { name: '八一广场', distance: 2.1 },
  { name: '绳金塔', distance: 3.5 },
]

const similarShops = [
  { name: '堂瓦里', rating: 4.7, price: 80, category: '江西菜' },
  { name: '民间饭庄', rating: 4.6, price: 70, category: '江西菜' },
  { name: '小厨娘', rating: 4.4, price: 55, category: '江西菜' },
]

const ratingLevel = computed(() => getRatingLevel(shop.value.rating))
const catColor = computed(() => CATEGORY_COLORS[shop.value.category] || '#6b6660')

const radarRef = ref<HTMLElement>()

onMounted(() => {
  initRadar()
})

function initRadar() {
  if (!radarRef.value) return
  const chart = echarts.init(radarRef.value)
  chart.setOption({
    radar: {
      indicator: [
        { name: '口味', max: 5 },
        { name: '环境', max: 5 },
        { name: '服务', max: 5 },
        { name: '性价比', max: 5 },
        { name: '位置', max: 5 },
      ],
      axisName: { color: '#a8a3a0', fontSize: 11 },
      splitArea: { areaStyle: { color: ['rgba(255,255,255,0.01)', 'rgba(255,255,255,0.02)'] } },
      splitLine: { lineStyle: { color: 'rgba(255,255,255,0.04)' } },
      axisLine: { lineStyle: { color: 'rgba(255,255,255,0.06)' } },
    },
    series: [{
      type: 'radar',
      data: [{
        value: [4.8, 4.2, 4.0, 4.5, 4.6],
        areaStyle: { color: 'rgba(192, 86, 33, 0.2)' },
        lineStyle: { color: '#c05621', width: 2 },
        itemStyle: { color: '#c05621' },
      }],
    }],
  })
  window.addEventListener('resize', () => chart.resize())
}
</script>

<template>
  <div class="detail-page">
    <!-- Back button -->
    <button class="back-btn" @click="router.back()">
      <el-icon><ArrowLeft /></el-icon>
      <span>返回</span>
    </button>

    <!-- Hero Section -->
    <div class="shop-hero">
      <div class="hero-bg">
        <div class="hero-gradient" :style="{ '--cat-color': catColor }" />
      </div>
      <div class="hero-content">
        <div class="shop-badges">
          <span
            class="badge-category"
            :style="{ background: catColor + '20', color: catColor }"
          >
            {{ shop.categoryName }}
          </span>
          <span class="badge-source">
            {{ SOURCE_LABELS[shop.source] || shop.source }}
          </span>
          <span v-if="shop.rank && shop.rank <= 3" class="badge-rank">
            🏆 TOP {{ shop.rank }}
          </span>
        </div>

        <h1 class="shop-name">{{ shop.name }}</h1>

        <div class="shop-meta">
          <div class="meta-rating">
            <span class="rating-value" :style="{ color: ratingLevel.color }">{{ shop.rating }}</span>
            <span class="rating-label" :style="{ color: ratingLevel.color }">{{ ratingLevel.label }}</span>
          </div>
          <div class="meta-divider" />
          <div class="meta-price">
            <span class="price-value">{{ formatPrice(shop.priceAvg) }}</span>
            <span class="price-label">人均</span>
          </div>
          <div class="meta-divider" />
          <div class="meta-views">
            <span class="views-value">{{ shop.viewCount.toLocaleString() }}</span>
            <span class="views-label">浏览</span>
          </div>
        </div>

        <div class="shop-tags">
          <span v-for="tag in shop.tags" :key="tag" class="tag">{{ tag }}</span>
        </div>
      </div>
    </div>

    <!-- Content Grid -->
    <div class="content-grid">
      <!-- Left Column -->
      <div class="content-left">
        <!-- Info Card -->
        <div class="info-card">
          <h3 class="card-title">
            <el-icon><InfoFilled /></el-icon>
            基本信息
          </h3>
          <div class="info-rows">
            <div class="info-row">
              <span class="info-label">地址</span>
              <span class="info-value">{{ shop.address }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">电话</span>
              <span class="info-value">{{ shop.phone }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">营业时间</span>
              <span class="info-value">{{ shop.businessHours }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">互动数据</span>
              <span class="info-value">
                👍 {{ shop.likeCount.toLocaleString() }} · 💬 {{ shop.commentCount.toLocaleString() }}
              </span>
            </div>
          </div>
        </div>

        <!-- Radar Chart -->
        <div class="info-card">
          <h3 class="card-title">
            <el-icon><DataAnalysis /></el-icon>
            多维度评分
          </h3>
          <div ref="radarRef" class="radar-chart" />
        </div>
      </div>

      <!-- Right Column -->
      <div class="content-right">
        <!-- Nearby Spots -->
        <div class="info-card">
          <h3 class="card-title">
            <el-icon><Location /></el-icon>
            周边景点
          </h3>
          <div class="nearby-list">
            <div v-for="spot in nearbySpots" :key="spot.name" class="nearby-item">
              <span class="nearby-name">{{ spot.name }}</span>
              <span class="nearby-distance">{{ spot.distance }}km</span>
            </div>
          </div>
        </div>

        <!-- Similar Shops -->
        <div class="info-card">
          <h3 class="card-title">
            <el-icon><Shop /></el-icon>
            相似推荐
          </h3>
          <div class="similar-list">
            <div v-for="s in similarShops" :key="s.name" class="similar-item">
              <div class="similar-info">
                <span class="similar-name">{{ s.name }}</span>
                <span class="similar-meta">
                  <span class="similar-rating">★ {{ s.rating }}</span>
                  <span class="similar-price">{{ formatPrice(s.price) }}/人</span>
                </span>
              </div>
              <el-icon class="similar-arrow"><ArrowRight /></el-icon>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.detail-page {
  padding: var(--space-8);
  max-width: 1100px;
  margin: 0 auto;
}

.back-btn {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-4);
  background: var(--color-bg-card);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: var(--radius-full);
  color: var(--color-text-secondary);
  font-size: var(--text-sm);
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-out);
  margin-bottom: var(--space-5);
}

.back-btn:hover {
  color: var(--color-text-primary);
  border-color: rgba(255, 255, 255, 0.12);
}

/* ── Hero ── */
.shop-hero {
  position: relative;
  border-radius: var(--radius-xl);
  overflow: hidden;
  padding: var(--space-10) var(--space-8);
  margin-bottom: var(--space-6);
}

.hero-bg {
  position: absolute;
  inset: 0;
}

.hero-gradient {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse at 30% 50%, color-mix(in srgb, var(--cat-color) 20%, transparent) 0%, transparent 60%),
    radial-gradient(ellipse at 70% 30%, rgba(212, 160, 60, 0.1) 0%, transparent 50%),
    var(--color-bg-card);
}

.hero-content {
  position: relative;
  z-index: 1;
}

.shop-badges {
  display: flex;
  gap: var(--space-2);
  margin-bottom: var(--space-4);
}

.badge-category,
.badge-source,
.badge-rank {
  font-size: var(--text-xs);
  padding: 2px 10px;
  border-radius: var(--radius-full);
  font-weight: 500;
}

.badge-source {
  background: rgba(255, 255, 255, 0.06);
  color: var(--color-text-secondary);
}

.badge-rank {
  background: linear-gradient(135deg, #d4a03c20, #d4a03c10);
  color: var(--color-gold);
}

.shop-name {
  font-family: var(--font-chinese);
  font-size: var(--text-4xl);
  font-weight: 800;
  margin-bottom: var(--space-5);
  animation: fadeInUp 0.6s var(--ease-out) 0.1s both;
}

.shop-meta {
  display: flex;
  align-items: center;
  gap: var(--space-5);
  margin-bottom: var(--space-5);
  animation: fadeInUp 0.6s var(--ease-out) 0.2s both;
}

.meta-rating,
.meta-price,
.meta-views {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.rating-value,
.price-value,
.views-value {
  font-family: var(--font-display);
  font-size: var(--text-2xl);
  font-weight: 700;
  line-height: 1;
}

.price-value {
  color: var(--color-primary-light);
}

.views-value {
  color: var(--color-text-primary);
}

.rating-label,
.price-label,
.views-label {
  font-size: var(--text-xs);
  color: var(--color-text-muted);
  margin-top: 2px;
}

.meta-divider {
  width: 1px;
  height: 32px;
  background: rgba(255, 255, 255, 0.06);
}

.shop-tags {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
  animation: fadeInUp 0.6s var(--ease-out) 0.3s both;
}

.tag {
  font-size: var(--text-xs);
  padding: var(--space-1) var(--space-3);
  border-radius: var(--radius-full);
  background: rgba(255, 255, 255, 0.06);
  color: var(--color-text-secondary);
  border: 1px solid rgba(255, 255, 255, 0.04);
}

/* ── Content Grid ── */
.content-grid {
  display: grid;
  grid-template-columns: 1.2fr 1fr;
  gap: var(--space-6);
}

.info-card {
  background: var(--color-bg-card);
  border: 1px solid rgba(255, 255, 255, 0.04);
  border-radius: var(--radius-lg);
  padding: var(--space-5);
  margin-bottom: var(--space-5);
}

.card-title {
  font-family: var(--font-chinese);
  font-size: var(--text-base);
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: var(--space-2);
  margin-bottom: var(--space-4);
  color: var(--color-text-primary);
}

.info-rows {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.info-row {
  display: flex;
  align-items: flex-start;
  gap: var(--space-4);
}

.info-label {
  font-size: var(--text-sm);
  color: var(--color-text-muted);
  width: 80px;
  flex-shrink: 0;
}

.info-value {
  font-size: var(--text-sm);
  color: var(--color-text-primary);
}

.radar-chart {
  width: 100%;
  height: 280px;
}

/* ── Nearby ── */
.nearby-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.nearby-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-3);
  border-radius: var(--radius-md);
  background: var(--color-bg-elevated);
}

.nearby-name {
  font-size: var(--text-sm);
  color: var(--color-text-primary);
}

.nearby-distance {
  font-size: var(--text-xs);
  color: var(--color-primary-light);
  font-weight: 500;
}

/* ── Similar ── */
.similar-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.similar-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-3);
  border-radius: var(--radius-md);
  background: var(--color-bg-elevated);
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-out);
}

.similar-item:hover {
  background: var(--color-bg-hover);
}

.similar-info {
  display: flex;
  flex-direction: column;
}

.similar-name {
  font-size: var(--text-sm);
  font-weight: 500;
  color: var(--color-text-primary);
}

.similar-meta {
  display: flex;
  gap: var(--space-3);
  font-size: var(--text-xs);
  color: var(--color-text-muted);
}

.similar-rating {
  color: var(--color-gold);
}

.similar-arrow {
  color: var(--color-text-muted);
}
</style>
