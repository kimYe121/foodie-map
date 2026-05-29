<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import type { RankItem } from '@/types'
import { CATEGORY_COLORS, formatPrice, formatCount } from '@/utils/format'

const route = useRoute()
const rankType = computed(() => route.meta.rankType as string)

const rankTitle = computed(() => {
  const map: Record<string, string> = {
    overall: '综合评分榜',
    costPerformance: '性价比榜',
    hot: '热门榜',
    category: '分类榜',
  }
  return map[rankType.value] || '排行榜'
})

const rankDesc = computed(() => {
  const map: Record<string, string> = {
    overall: '综合评分最高的店铺，口碑之选',
    costPerformance: '花最少的钱，吃最好的饭',
    hot: '最受关注的热门店铺',
    category: '各分类下的顶尖店铺',
  }
  return map[rankType.value] || ''
})

// ── Mock data ──
const mockRankData: RankItem[] = [
  { shopId: 'dp_001', name: '老三样', category: 'jiangxi', categoryName: '江西菜', rating: 4.8, priceAvg: 65, address: '西湖区中山路123号', tags: ['网红店', '排队王', '必吃榜'], rank: 1, costPerformance: 7.4, viewCount: 15234 },
  { shopId: 'dp_002', name: '堂瓦里', category: 'jiangxi', categoryName: '江西菜', rating: 4.7, priceAvg: 80, address: '东湖区胜利路456号', tags: ['正宗赣菜', '环境好'], rank: 2, costPerformance: 5.9, viewCount: 12890 },
  { shopId: 'dp_003', name: '周真真粉面馆', category: 'snack', categoryName: '小吃快餐', rating: 4.5, priceAvg: 25, address: '青山湖区北京东路789号', tags: ['南昌拌粉', '老字号'], rank: 3, costPerformance: 18.0, viewCount: 11234 },
  { shopId: 'dp_004', name: '味福记', category: 'snack', categoryName: '小吃快餐', rating: 4.3, priceAvg: 35, address: '西湖区孺子路456号', tags: ['瓦罐汤', '本地人爱去'], rank: 4, costPerformance: 12.3, viewCount: 9876 },
  { shopId: 'dp_005', name: '民间饭庄', category: 'jiangxi', categoryName: '江西菜', rating: 4.6, priceAvg: 70, address: '东湖区八一大道100号', tags: ['家庭聚餐', '分量足'], rank: 5, costPerformance: 6.6, viewCount: 8765 },
  { shopId: 'dp_006', name: '无名火锅', category: 'hotpot', categoryName: '火锅', rating: 4.4, priceAvg: 95, address: '红谷滩区万达广场', tags: ['川味火锅', '毛肚必点'], rank: 6, costPerformance: 4.6, viewCount: 7654 },
  { shopId: 'dp_007', name: '阿婆烧烤', category: 'bbq', categoryName: '烧烤烤肉', rating: 4.3, priceAvg: 55, address: '青山湖区上海路', tags: ['深夜食堂', '烤串'], rank: 7, costPerformance: 7.8, viewCount: 6543 },
  { shopId: 'dp_008', name: '鹿港小镇', category: 'japan_korea', categoryName: '日韩料理', rating: 4.2, priceAvg: 120, address: '红谷滩区铜锣湾', tags: ['日料', '刺身新鲜'], rank: 8, costPerformance: 3.5, viewCount: 5432 },
  { shopId: 'dp_009', name: '茶百道', category: 'dessert', categoryName: '甜品饮品', rating: 4.1, priceAvg: 18, address: '西湖区中山路', tags: ['奶茶', '杨枝甘露'], rank: 9, costPerformance: 22.8, viewCount: 4321 },
  { shopId: 'dp_010', name: '老南昌白糖糕', category: 'snack', categoryName: '小吃快餐', rating: 4.6, priceAvg: 15, address: '东湖区胜利路', tags: ['传统小吃', '非遗'], rank: 10, costPerformance: 30.7, viewCount: 3210 },
]

const rankData = ref<RankItem[]>(mockRankData)
const selectedCategory = ref('')
const categories = ['jiangxi', 'hotpot', 'snack', 'bbq', 'western', 'japan_korea', 'seafood', 'dessert']
const categoryNames: Record<string, string> = {
  jiangxi: '江西菜', hotpot: '火锅', snack: '小吃快餐', bbq: '烧烤烤肉',
  western: '西餐', japan_korea: '日韩料理', seafood: '海鲜', dessert: '甜品饮品',
}

function getRankBadgeClass(rank: number) {
  if (rank === 1) return 'rank-gold'
  if (rank === 2) return 'rank-silver'
  if (rank === 3) return 'rank-bronze'
  return ''
}

function getCategoryColor(cat: string) {
  return CATEGORY_COLORS[cat] || '#6b6660'
}
</script>

<template>
  <div class="rank-page">
    <!-- Header -->
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">
          <span class="title-icon">🏆</span>
          {{ rankTitle }}
        </h1>
        <p class="page-desc">{{ rankDesc }}</p>
      </div>

      <!-- Category filter for category rank -->
      <div v-if="rankType === 'category'" class="category-filter">
        <button
          v-for="cat in categories"
          :key="cat"
          class="cat-chip"
          :class="{ active: selectedCategory === cat }"
          :style="{ '--cat-color': getCategoryColor(cat) }"
          @click="selectedCategory = cat"
        >
          {{ categoryNames[cat] }}
        </button>
      </div>
    </div>

    <!-- Rank List -->
    <div class="rank-list stagger-reveal">
      <div
        v-for="item in rankData"
        :key="item.shopId"
        class="rank-item"
        :class="{ 'top-three': item.rank <= 3 }"
      >
        <!-- Rank Number -->
        <div class="rank-badge" :class="getRankBadgeClass(item.rank)">
          <span v-if="item.rank <= 3" class="rank-icon">
            {{ item.rank === 1 ? '🥇' : item.rank === 2 ? '🥈' : '🥉' }}
          </span>
          <span v-else class="rank-num">{{ item.rank }}</span>
        </div>

        <!-- Shop Info -->
        <div class="shop-info">
          <div class="shop-main">
            <h3 class="shop-name">{{ item.name }}</h3>
            <div class="shop-tags">
              <span
                class="shop-category"
                :style="{ background: getCategoryColor(item.category) + '20', color: getCategoryColor(item.category) }"
              >
                {{ item.categoryName }}
              </span>
              <span v-for="tag in item.tags.slice(0, 2)" :key="tag" class="shop-tag">
                {{ tag }}
              </span>
            </div>
          </div>
          <p class="shop-address">{{ item.address }}</p>
        </div>

        <!-- Metrics -->
        <div class="shop-metrics">
          <div class="metric">
            <span class="metric-value">{{ item.rating }}</span>
            <span class="metric-label">评分</span>
          </div>
          <div class="metric">
            <span class="metric-value">{{ formatPrice(item.priceAvg) }}</span>
            <span class="metric-label">人均</span>
          </div>
          <div v-if="rankType === 'costPerformance'" class="metric highlight">
            <span class="metric-value">{{ item.costPerformance }}</span>
            <span class="metric-label">性价比</span>
          </div>
          <div v-if="rankType === 'hot'" class="metric highlight">
            <span class="metric-value">{{ formatCount(item.viewCount || 0) }}</span>
            <span class="metric-label">浏览</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.rank-page {
  padding: var(--space-8);
  max-width: 960px;
  margin: 0 auto;
}

/* ── Header ── */
.page-header {
  margin-bottom: var(--space-8);
}

.header-content {
  margin-bottom: var(--space-5);
}

.page-title {
  font-family: var(--font-display);
  font-size: var(--text-3xl);
  font-weight: 800;
  display: flex;
  align-items: center;
  gap: var(--space-3);
  margin-bottom: var(--space-2);
}

.title-icon {
  font-size: var(--text-2xl);
}

.page-desc {
  font-size: var(--text-base);
  color: var(--color-text-secondary);
}

.category-filter {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
}

.cat-chip {
  padding: var(--space-2) var(--space-4);
  border-radius: var(--radius-full);
  border: 1px solid rgba(255, 255, 255, 0.08);
  background: var(--color-bg-card);
  color: var(--color-text-secondary);
  font-size: var(--text-sm);
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-out);
}

.cat-chip:hover {
  border-color: var(--cat-color);
  color: var(--cat-color);
}

.cat-chip.active {
  background: var(--cat-color);
  border-color: var(--cat-color);
  color: #fff;
}

/* ── Rank List ── */
.rank-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.rank-item {
  background: var(--color-bg-card);
  border: 1px solid rgba(255, 255, 255, 0.04);
  border-radius: var(--radius-lg);
  padding: var(--space-5);
  display: flex;
  align-items: center;
  gap: var(--space-5);
  transition: all var(--duration-normal) var(--ease-out);
  cursor: pointer;
}

.rank-item:hover {
  transform: translateX(4px);
  box-shadow: var(--shadow-md);
  border-color: rgba(255, 255, 255, 0.08);
}

.rank-item.top-three {
  border-color: rgba(212, 160, 60, 0.12);
  background: linear-gradient(135deg, var(--color-bg-card), rgba(212, 160, 60, 0.03));
}

/* ── Rank Badge ── */
.rank-badge {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  background: var(--color-bg-elevated);
}

.rank-badge.rank-gold {
  background: linear-gradient(135deg, #d4a03c20, #d4a03c10);
}

.rank-badge.rank-silver {
  background: linear-gradient(135deg, #a8a3a020, #a8a3a010);
}

.rank-badge.rank-bronze {
  background: linear-gradient(135deg, #8b3a1420, #8b3a1410);
}

.rank-icon {
  font-size: 1.5rem;
}

.rank-num {
  font-family: var(--font-display);
  font-size: var(--text-xl);
  font-weight: 700;
  color: var(--color-text-muted);
}

/* ── Shop Info ── */
.shop-info {
  flex: 1;
  min-width: 0;
}

.shop-main {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  margin-bottom: var(--space-1);
  flex-wrap: wrap;
}

.shop-name {
  font-family: var(--font-chinese);
  font-size: var(--text-lg);
  font-weight: 600;
}

.shop-tags {
  display: flex;
  gap: var(--space-1);
  flex-wrap: wrap;
}

.shop-category {
  font-size: var(--text-xs);
  padding: 1px 8px;
  border-radius: var(--radius-full);
  font-weight: 500;
}

.shop-tag {
  font-size: var(--text-xs);
  padding: 1px 8px;
  border-radius: var(--radius-full);
  background: rgba(255, 255, 255, 0.04);
  color: var(--color-text-muted);
}

.shop-address {
  font-size: var(--text-sm);
  color: var(--color-text-muted);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* ── Metrics ── */
.shop-metrics {
  display: flex;
  gap: var(--space-6);
  flex-shrink: 0;
}

.metric {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
}

.metric-value {
  font-family: var(--font-display);
  font-size: var(--text-lg);
  font-weight: 700;
  color: var(--color-text-primary);
}

.metric.highlight .metric-value {
  color: var(--color-primary-light);
}

.metric-label {
  font-size: var(--text-xs);
  color: var(--color-text-muted);
}
</style>
