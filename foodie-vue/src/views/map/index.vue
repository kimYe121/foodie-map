<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import type { MapShopPoint, Spot } from '@/types'
import { CATEGORY_COLORS, formatPrice } from '@/utils/format'

// ── Mock data ──
const mockShops: MapShopPoint[] = [
  { shopId: 'dp_001', name: '老三样', longitude: 115.889, latitude: 28.684, rating: 4.8, priceAvg: 65, category: 'jiangxi' },
  { shopId: 'dp_002', name: '堂瓦里', longitude: 115.912, latitude: 28.682, rating: 4.7, priceAvg: 80, category: 'jiangxi' },
  { shopId: 'dp_003', name: '周真真粉面馆', longitude: 115.898, latitude: 28.674, rating: 4.5, priceAvg: 25, category: 'snack' },
  { shopId: 'dp_004', name: '味福记', longitude: 115.876, latitude: 28.690, rating: 4.3, priceAvg: 35, category: 'snack' },
  { shopId: 'dp_005', name: '民间饭庄', longitude: 115.910, latitude: 28.680, rating: 4.6, priceAvg: 70, category: 'jiangxi' },
  { shopId: 'dp_006', name: '无名火锅', longitude: 115.900, latitude: 28.688, rating: 4.4, priceAvg: 95, category: 'hotpot' },
  { shopId: 'dp_007', name: '阿婆烧烤', longitude: 115.895, latitude: 28.678, rating: 4.3, priceAvg: 55, category: 'bbq' },
]

const mockSpots: Spot[] = [
  { spotId: 'tengwangge', name: '滕王阁', longitude: 115.889, latitude: 28.684, description: '江南三大名楼之一', hotScore: 100, createTime: '' },
  { spotId: 'bayi', name: '八一广场', longitude: 115.912, latitude: 28.682, description: '南昌市中心广场', hotScore: 95, createTime: '' },
  { spotId: 'shengjin', name: '绳金塔', longitude: 115.898, latitude: 28.674, description: '千年古塔', hotScore: 85, createTime: '' },
  { spotId: 'qiushui', name: '秋水广场', longitude: 115.876, latitude: 28.690, description: '亚洲最大音乐喷泉', hotScore: 90, createTime: '' },
]

const selectedCategory = ref('')
const selectedSpot = ref<string>('')
const mapRef = ref<HTMLElement>()
const showShopDetail = ref(false)
const activeShop = ref<MapShopPoint | null>(null)

const categories = [
  { key: '', label: '全部' },
  { key: 'jiangxi', label: '江西菜' },
  { key: 'snack', label: '小吃' },
  { key: 'hotpot', label: '火锅' },
  { key: 'bbq', label: '烧烤' },
  { key: 'dessert', label: '甜品' },
]

const filteredShops = computed(() => {
  let shops = mockShops
  if (selectedCategory.value) {
    shops = shops.filter(s => s.category === selectedCategory.value)
  }
  return shops
})

function selectShop(shop: MapShopPoint) {
  activeShop.value = shop
  showShopDetail.value = true
}

function getCatColor(cat: string) {
  return CATEGORY_COLORS[cat] || '#6b6660'
}

// Map placeholder — AMap integration requires API key
const mapReady = ref(false)
onMounted(() => {
  // Simulate map loading
  setTimeout(() => { mapReady.value = true }, 800)
})
</script>

<template>
  <div class="map-page">
    <!-- Map Controls -->
    <div class="map-controls glass">
      <div class="control-section">
        <h3 class="control-title">分类筛选</h3>
        <div class="filter-chips">
          <button
            v-for="cat in categories"
            :key="cat.key"
            class="chip"
            :class="{ active: selectedCategory === cat.key }"
            @click="selectedCategory = cat.key"
          >
            {{ cat.label }}
          </button>
        </div>
      </div>

      <div class="divider" />

      <div class="control-section">
        <h3 class="control-title">景点周边</h3>
        <div class="spot-list">
          <button
            v-for="spot in mockSpots"
            :key="spot.spotId"
            class="spot-btn"
            :class="{ active: selectedSpot === spot.spotId }"
            @click="selectedSpot = selectedSpot === spot.spotId ? '' : spot.spotId"
          >
            <span class="spot-name">{{ spot.name }}</span>
            <span class="spot-hot">🔥 {{ spot.hotScore }}</span>
          </button>
        </div>
      </div>

      <div class="divider" />

      <div class="control-section">
        <h3 class="control-title">店铺列表 <span class="count">{{ filteredShops.length }}</span></h3>
        <div class="shop-list">
          <div
            v-for="shop in filteredShops"
            :key="shop.shopId"
            class="shop-item"
            :class="{ active: activeShop?.shopId === shop.shopId }"
            @click="selectShop(shop)"
          >
            <div class="shop-dot" :style="{ background: getCatColor(shop.category) }" />
            <div class="shop-info">
              <span class="shop-name">{{ shop.name }}</span>
              <span class="shop-meta">
                <span class="rating">★ {{ shop.rating }}</span>
                <span class="price">{{ formatPrice(shop.priceAvg) }}/人</span>
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Map Area -->
    <div class="map-area">
      <div ref="mapRef" class="map-container">
        <!-- Map placeholder with visual representation -->
        <div v-if="!mapReady" class="map-loading">
          <div class="loading-spinner" />
          <span>地图加载中...</span>
        </div>

        <div v-else class="map-placeholder">
          <!-- Visual dot map as placeholder -->
          <svg viewBox="0 0 800 600" class="dot-map">
            <!-- Grid lines -->
            <defs>
              <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
                <path d="M 40 0 L 0 0 0 40" fill="none" stroke="rgba(255,255,255,0.02)" stroke-width="1"/>
              </pattern>
            </defs>
            <rect width="100%" height="100%" fill="url(#grid)" />

            <!-- Spot markers -->
            <g v-for="(spot, i) in mockSpots" :key="spot.spotId">
              <circle
                :cx="200 + i * 150"
                :cy="300 + (i % 2 === 0 ? -80 : 80)"
                r="20"
                fill="rgba(192, 86, 33, 0.15)"
                stroke="var(--color-primary)"
                stroke-width="1.5"
                class="spot-marker"
              />
              <circle
                :cx="200 + i * 150"
                :cy="300 + (i % 2 === 0 ? -80 : 80)"
                r="6"
                fill="var(--color-primary)"
              />
              <text
                :x="200 + i * 150"
                :y="300 + (i % 2 === 0 ? -80 : 80) + 35"
                text-anchor="middle"
                fill="var(--color-text-secondary)"
                font-size="12"
                font-family="var(--font-chinese)"
              >
                {{ spot.name }}
              </text>
            </g>

            <!-- Shop markers -->
            <g v-for="(shop, i) in filteredShops" :key="shop.shopId">
              <circle
                :cx="120 + (i * 97) % 600"
                :cy="180 + (i * 73) % 300"
                r="8"
                :fill="getCatColor(shop.category)"
                class="shop-marker"
                :class="{ active: activeShop?.shopId === shop.shopId }"
                @click="selectShop(shop)"
              />
            </g>
          </svg>

          <!-- Map overlay info -->
          <div class="map-overlay">
            <div class="overlay-badge">
              <el-icon><MapLocation /></el-icon>
              <span>南昌市 · {{ filteredShops.length }} 家店铺</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Shop Detail Panel -->
      <transition name="slide">
        <div v-if="showShopDetail && activeShop" class="detail-panel glass">
          <div class="detail-header">
            <h3>{{ activeShop.name }}</h3>
            <button class="close-btn" @click="showShopDetail = false">
              <el-icon><Close /></el-icon>
            </button>
          </div>
          <div class="detail-body">
            <div class="detail-rating">
              <span class="rating-value">{{ activeShop.rating }}</span>
              <span class="rating-label">评分</span>
            </div>
            <div class="detail-price">
              <span class="price-value">{{ formatPrice(activeShop.priceAvg) }}</span>
              <span class="price-label">人均</span>
            </div>
            <div class="detail-category">
              <span
                class="cat-badge"
                :style="{ background: getCatColor(activeShop.category) + '20', color: getCatColor(activeShop.category) }"
              >
                {{ activeShop.category }}
              </span>
            </div>
          </div>
          <el-button type="primary" round class="detail-btn">
            查看详情
            <el-icon><ArrowRight /></el-icon>
          </el-button>
        </div>
      </transition>
    </div>
  </div>
</template>

<style scoped>
.map-page {
  display: flex;
  height: calc(100vh - var(--header-height, 0px));
  overflow: hidden;
}

/* ── Controls Panel ── */
.map-controls {
  width: 320px;
  flex-shrink: 0;
  padding: var(--space-5);
  overflow-y: auto;
  border-right: 1px solid rgba(255, 255, 255, 0.04);
  background: var(--color-bg-primary);
}

.control-section {
  margin-bottom: var(--space-4);
}

.control-title {
  font-family: var(--font-chinese);
  font-size: var(--text-sm);
  font-weight: 600;
  color: var(--color-text-secondary);
  margin-bottom: var(--space-3);
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.control-title .count {
  font-size: var(--text-xs);
  padding: 1px 6px;
  background: var(--color-primary-glow);
  color: var(--color-primary-light);
  border-radius: var(--radius-full);
}

.filter-chips {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
}

.chip {
  padding: var(--space-1) var(--space-3);
  border-radius: var(--radius-full);
  border: 1px solid rgba(255, 255, 255, 0.08);
  background: var(--color-bg-card);
  color: var(--color-text-secondary);
  font-size: var(--text-xs);
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-out);
}

.chip:hover {
  border-color: var(--color-primary);
  color: var(--color-primary-light);
}

.chip.active {
  background: var(--color-primary);
  border-color: var(--color-primary);
  color: #fff;
}

.spot-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.spot-btn {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-md);
  border: 1px solid rgba(255, 255, 255, 0.04);
  background: var(--color-bg-card);
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-out);
}

.spot-btn:hover {
  border-color: rgba(255, 255, 255, 0.08);
  background: var(--color-bg-hover);
}

.spot-btn.active {
  border-color: var(--color-primary);
  background: var(--color-primary-glow);
}

.spot-btn .spot-name {
  font-size: var(--text-sm);
  color: var(--color-text-primary);
}

.spot-btn .spot-hot {
  font-size: var(--text-xs);
  color: var(--color-text-muted);
}

.shop-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
  max-height: 300px;
  overflow-y: auto;
}

.shop-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-out);
}

.shop-item:hover {
  background: var(--color-bg-hover);
}

.shop-item.active {
  background: var(--color-primary-glow);
}

.shop-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}

.shop-item .shop-info {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.shop-item .shop-name {
  font-size: var(--text-sm);
  color: var(--color-text-primary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.shop-meta {
  display: flex;
  gap: var(--space-3);
  font-size: var(--text-xs);
  color: var(--color-text-muted);
}

.shop-meta .rating {
  color: var(--color-gold);
}

/* ── Map Area ── */
.map-area {
  flex: 1;
  position: relative;
  background: var(--color-bg-deep);
}

.map-container {
  width: 100%;
  height: 100%;
}

.map-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  gap: var(--space-4);
  color: var(--color-text-muted);
}

.loading-spinner {
  width: 32px;
  height: 32px;
  border: 2px solid rgba(255, 255, 255, 0.06);
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.map-placeholder {
  width: 100%;
  height: 100%;
  position: relative;
}

.dot-map {
  width: 100%;
  height: 100%;
}

.spot-marker {
  animation: pulse-glow 3s ease-in-out infinite;
}

.shop-marker {
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-out);
}

.shop-marker:hover,
.shop-marker.active {
  r: 12;
  filter: drop-shadow(0 0 8px currentColor);
}

.map-overlay {
  position: absolute;
  top: var(--space-4);
  left: var(--space-4);
}

.overlay-badge {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-4);
  background: rgba(30, 30, 46, 0.8);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: var(--radius-full);
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
}

/* ── Detail Panel ── */
.detail-panel {
  position: absolute;
  right: var(--space-4);
  top: var(--space-4);
  width: 300px;
  padding: var(--space-5);
  border-radius: var(--radius-lg);
  z-index: 10;
}

.detail-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-4);
}

.detail-header h3 {
  font-family: var(--font-chinese);
  font-size: var(--text-lg);
  font-weight: 600;
}

.close-btn {
  background: none;
  border: none;
  color: var(--color-text-muted);
  cursor: pointer;
  padding: var(--space-1);
  border-radius: var(--radius-sm);
  transition: all var(--duration-fast) var(--ease-out);
}

.close-btn:hover {
  color: var(--color-text-primary);
  background: var(--color-bg-hover);
}

.detail-body {
  display: flex;
  gap: var(--space-5);
  margin-bottom: var(--space-5);
}

.detail-rating,
.detail-price {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.rating-value,
.price-value {
  font-family: var(--font-display);
  font-size: var(--text-2xl);
  font-weight: 700;
}

.rating-value {
  color: var(--color-gold);
}

.price-value {
  color: var(--color-primary-light);
}

.rating-label,
.price-label {
  font-size: var(--text-xs);
  color: var(--color-text-muted);
}

.cat-badge {
  font-size: var(--text-xs);
  padding: 2px 10px;
  border-radius: var(--radius-full);
  font-weight: 500;
}

.detail-btn {
  width: 100%;
}

/* ── Slide transition ── */
.slide-enter-active,
.slide-leave-active {
  transition: all var(--duration-normal) var(--ease-out);
}

.slide-enter-from,
.slide-leave-to {
  opacity: 0;
  transform: translateX(20px);
}
</style>
