<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import * as echarts from 'echarts'
import type { OverviewStats } from '@/types'

// ── Mock data (replace with API call when backend is ready) ──
const stats = ref<OverviewStats>({
  totalShops: 1256,
  totalSpots: 7,
  categoryStats: [
    { category: 'jiangxi', categoryName: '江西菜', count: 234 },
    { category: 'snack', categoryName: '小吃快餐', count: 456 },
    { category: 'hotpot', categoryName: '火锅', count: 123 },
    { category: 'bbq', categoryName: '烧烤烤肉', count: 98 },
    { category: 'dessert', categoryName: '甜品饮品', count: 167 },
    { category: 'western', categoryName: '西餐', count: 65 },
    { category: 'japan_korea', categoryName: '日韩料理', count: 45 },
    { category: 'seafood', categoryName: '海鲜', count: 68 },
  ],
  priceStats: [
    { range: '<30元', count: 234 },
    { range: '30-60元', count: 567 },
    { range: '60-100元', count: 345 },
    { range: '>100元', count: 110 },
  ],
  ratingStats: {
    avgRating: 4.2,
    highRatingCount: 456,
    totalRatingCount: 1256,
  },
})

const spots = [
  { name: '滕王阁', score: 100, desc: '江南三大名楼之一' },
  { name: '八一广场', score: 95, desc: '南昌市中心广场' },
  { name: '绳金塔', score: 85, desc: '千年古塔' },
  { name: '秋水广场', score: 90, desc: '亚洲最大音乐喷泉' },
  { name: '八一起义纪念馆', score: 88, desc: '国家一级博物馆' },
  { name: '梅岭', score: 80, desc: '南昌后花园' },
]

const statCards = computed(() => [
  { label: '收录店铺', value: stats.value.totalShops, suffix: '家', icon: 'Shop', color: '#c05621' },
  { label: '热门景点', value: stats.value.totalSpots, suffix: '处', icon: 'Location', color: '#5a7247' },
  { label: '平均评分', value: stats.value.ratingStats.avgRating, suffix: '分', icon: 'Star', color: '#d4a03c' },
  { label: '高分店铺', value: stats.value.ratingStats.highRatingCount, suffix: '家', icon: 'Trophy', color: '#a03030' },
])

const categoryChartRef = ref<HTMLElement>()
const priceChartRef = ref<HTMLElement>()
const trendChartRef = ref<HTMLElement>()

onMounted(() => {
  initCategoryChart()
  initPriceChart()
  initTrendChart()
})

function initCategoryChart() {
  if (!categoryChartRef.value) return
  const chart = echarts.init(categoryChartRef.value)
  const data = stats.value.categoryStats
  chart.setOption({
    tooltip: {
      trigger: 'item',
      backgroundColor: '#1e1e2e',
      borderColor: 'rgba(255,255,255,0.06)',
      textStyle: { color: '#f0ece4' },
    },
    series: [{
      type: 'pie',
      radius: ['42%', '72%'],
      center: ['50%', '50%'],
      avoidLabelOverlap: true,
      itemStyle: {
        borderRadius: 6,
        borderColor: '#161621',
        borderWidth: 2,
      },
      label: {
        color: '#a8a3a0',
        fontSize: 12,
        fontFamily: 'Outfit, Noto Serif SC, sans-serif',
      },
      emphasis: {
        label: { show: true, fontSize: 14, fontWeight: '600', color: '#f0ece4' },
        itemStyle: { shadowBlur: 20, shadowColor: 'rgba(192, 86, 33, 0.3)' },
      },
      data: data.map((d, i) => ({
        name: d.categoryName,
        value: d.count,
        itemStyle: { color: ['#c05621', '#d4a03c', '#a03030', '#8b3a14', '#c07090', '#4a7090', '#6a5a8c', '#3a7a7a'][i] },
      })),
    }],
  })
  window.addEventListener('resize', () => chart.resize())
}

function initPriceChart() {
  if (!priceChartRef.value) return
  const chart = echarts.init(priceChartRef.value)
  const data = stats.value.priceStats
  chart.setOption({
    tooltip: {
      trigger: 'axis',
      backgroundColor: '#1e1e2e',
      borderColor: 'rgba(255,255,255,0.06)',
      textStyle: { color: '#f0ece4' },
    },
    grid: { top: 20, right: 20, bottom: 30, left: 50 },
    xAxis: {
      type: 'category',
      data: data.map(d => d.range),
      axisLine: { lineStyle: { color: 'rgba(255,255,255,0.06)' } },
      axisLabel: { color: '#a8a3a0', fontSize: 11 },
    },
    yAxis: {
      type: 'value',
      splitLine: { lineStyle: { color: 'rgba(255,255,255,0.04)' } },
      axisLabel: { color: '#6b6660', fontSize: 11 },
    },
    series: [{
      type: 'bar',
      data: data.map((d, i) => ({
        value: d.count,
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: ['#5a7247', '#d4a03c', '#c05621', '#a03030'][i] },
            { offset: 1, color: ['#5a724780', '#d4a03c80', '#c0562180', '#a0303080'][i] },
          ]),
          borderRadius: [4, 4, 0, 0],
        },
      })),
      barWidth: '45%',
    }],
  })
  window.addEventListener('resize', () => chart.resize())
}

function initTrendChart() {
  if (!trendChartRef.value) return
  const chart = echarts.init(trendChartRef.value)
  const months = ['1月', '2月', '3月', '4月', '5月', '6月']
  chart.setOption({
    tooltip: {
      trigger: 'axis',
      backgroundColor: '#1e1e2e',
      borderColor: 'rgba(255,255,255,0.06)',
      textStyle: { color: '#f0ece4' },
    },
    grid: { top: 20, right: 20, bottom: 30, left: 50 },
    xAxis: {
      type: 'category',
      data: months,
      axisLine: { lineStyle: { color: 'rgba(255,255,255,0.06)' } },
      axisLabel: { color: '#a8a3a0', fontSize: 11 },
    },
    yAxis: {
      type: 'value',
      splitLine: { lineStyle: { color: 'rgba(255,255,255,0.04)' } },
      axisLabel: { color: '#6b6660', fontSize: 11 },
    },
    series: [
      {
        name: '新增店铺',
        type: 'line',
        smooth: true,
        data: [45, 62, 78, 95, 120, 156],
        lineStyle: { color: '#c05621', width: 2 },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(192, 86, 33, 0.25)' },
            { offset: 1, color: 'rgba(192, 86, 33, 0.02)' },
          ]),
        },
        itemStyle: { color: '#c05621' },
        symbol: 'circle',
        symbolSize: 6,
      },
      {
        name: '数据采集量',
        type: 'line',
        smooth: true,
        data: [120, 280, 450, 680, 920, 1256],
        lineStyle: { color: '#d4a03c', width: 2 },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(212, 160, 60, 0.15)' },
            { offset: 1, color: 'rgba(212, 160, 60, 0.02)' },
          ]),
        },
        itemStyle: { color: '#d4a03c' },
        symbol: 'circle',
        symbolSize: 6,
      },
    ],
    legend: {
      data: ['新增店铺', '数据采集量'],
      textStyle: { color: '#a8a3a0', fontSize: 11 },
      right: 0,
      top: 0,
    },
  })
  window.addEventListener('resize', () => chart.resize())
}
</script>

<template>
  <div class="home-page">
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-bg">
        <div class="hero-gradient" />
        <div class="hero-dots" />
      </div>
      <div class="hero-content">
        <div class="hero-badge">
          <el-icon><Location /></el-icon>
          <span>南昌 · 江西南昌</span>
        </div>
        <h1 class="hero-title">
          <span class="hero-title-line">发现</span>
          <span class="hero-title-line accent">南昌味道</span>
        </h1>
        <p class="hero-desc">
          从滕王阁下的拌粉小店，到秋水广场旁的赣菜盛宴<br />
          用数据探索这座城市最真实的美食地图
        </p>
        <div class="hero-actions">
          <el-button type="primary" size="large" round>
            <el-icon><MapLocation /></el-icon>
            探索美食地图
          </el-button>
          <el-button size="large" round plain>
            <el-icon><Trophy /></el-icon>
            查看排行榜
          </el-button>
        </div>
      </div>
    </section>

    <!-- Stats Cards -->
    <section class="stats-section stagger-reveal">
      <div
        v-for="card in statCards"
        :key="card.label"
        class="stat-card"
      >
        <div class="stat-icon" :style="{ background: card.color + '18', color: card.color }">
          <el-icon :size="24"><component :is="card.icon" /></el-icon>
        </div>
        <div class="stat-info">
          <span class="stat-value stat-number">{{ card.value }}</span>
          <span class="stat-suffix">{{ card.suffix }}</span>
        </div>
        <span class="stat-label">{{ card.label }}</span>
      </div>
    </section>

    <!-- Charts Row -->
    <section class="charts-section">
      <div class="chart-card category-chart">
        <div class="chart-header">
          <h3>美食分类分布</h3>
          <span class="chart-sub">按店铺数量统计</span>
        </div>
        <div ref="categoryChartRef" class="chart-body" />
      </div>

      <div class="chart-card price-chart">
        <div class="chart-header">
          <h3>价格区间分布</h3>
          <span class="chart-sub">人均消费水平</span>
        </div>
        <div ref="priceChartRef" class="chart-body" />
      </div>

      <div class="chart-card trend-chart">
        <div class="chart-header">
          <h3>数据增长趋势</h3>
          <span class="chart-sub">近6个月采集数据</span>
        </div>
        <div ref="trendChartRef" class="chart-body" />
      </div>
    </section>

    <!-- Spots Section -->
    <section class="spots-section">
      <div class="section-header">
        <h2>热门景点</h2>
        <span class="section-sub">发现景点周边的隐藏美食</span>
      </div>
      <div class="spots-grid stagger-reveal">
        <div
          v-for="spot in spots"
          :key="spot.name"
          class="spot-card"
        >
          <div class="spot-rank">
            <span class="spot-score">{{ spot.score }}</span>
            <span class="spot-score-label">热度</span>
          </div>
          <div class="spot-info">
            <h4 class="spot-name">{{ spot.name }}</h4>
            <p class="spot-desc">{{ spot.desc }}</p>
          </div>
          <el-icon class="spot-arrow"><ArrowRight /></el-icon>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.home-page {
  padding: var(--space-8);
  max-width: var(--content-max);
  margin: 0 auto;
}

/* ── Hero ── */
.hero {
  position: relative;
  border-radius: var(--radius-xl);
  overflow: hidden;
  padding: var(--space-16) var(--space-12);
  margin-bottom: var(--space-8);
  min-height: 320px;
  display: flex;
  align-items: center;
}

.hero-bg {
  position: absolute;
  inset: 0;
  z-index: 0;
}

.hero-gradient {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse at 20% 50%, rgba(192, 86, 33, 0.2) 0%, transparent 60%),
    radial-gradient(ellipse at 80% 20%, rgba(212, 160, 60, 0.12) 0%, transparent 50%),
    radial-gradient(ellipse at 60% 80%, rgba(90, 114, 71, 0.1) 0%, transparent 50%),
    var(--color-bg-card);
}

.hero-dots {
  position: absolute;
  inset: 0;
  background-image: radial-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px);
  background-size: 24px 24px;
}

.hero-content {
  position: relative;
  z-index: 1;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-1) var(--space-3);
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: var(--radius-full);
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  margin-bottom: var(--space-6);
  animation: fadeInUp 0.6s var(--ease-out) 0.1s both;
}

.hero-title {
  font-family: var(--font-display);
  font-size: var(--text-5xl);
  font-weight: 800;
  line-height: 1.15;
  margin-bottom: var(--space-5);
}

.hero-title-line {
  display: block;
  animation: fadeInUp 0.6s var(--ease-out) 0.2s both;
}

.hero-title-line.accent {
  background: linear-gradient(135deg, var(--color-primary-light), var(--color-gold), var(--color-primary));
  background-size: 200% 200%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: fadeInUp 0.6s var(--ease-out) 0.3s both, gradient-shift 4s ease infinite;
}

.hero-desc {
  font-size: var(--text-lg);
  color: var(--color-text-secondary);
  line-height: 1.8;
  margin-bottom: var(--space-8);
  max-width: 520px;
  animation: fadeInUp 0.6s var(--ease-out) 0.4s both;
}

.hero-actions {
  display: flex;
  gap: var(--space-3);
  animation: fadeInUp 0.6s var(--ease-out) 0.5s both;
}

/* ── Stats Cards ── */
.stats-section {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--space-5);
  margin-bottom: var(--space-8);
}

.stat-card {
  background: var(--color-bg-card);
  border: 1px solid rgba(255, 255, 255, 0.04);
  border-radius: var(--radius-lg);
  padding: var(--space-6);
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  transition: all var(--duration-normal) var(--ease-out);
  position: relative;
  overflow: hidden;
}

.stat-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, var(--color-primary), var(--color-gold));
  opacity: 0;
  transition: opacity var(--duration-normal) var(--ease-out);
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
  border-color: rgba(255, 255, 255, 0.08);
}

.stat-card:hover::before {
  opacity: 1;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-info {
  display: flex;
  align-items: baseline;
  gap: var(--space-1);
}

.stat-value {
  font-size: var(--text-3xl);
  font-weight: 700;
  color: var(--color-text-primary);
}

.stat-suffix {
  font-size: var(--text-sm);
  color: var(--color-text-muted);
}

.stat-label {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
}

/* ── Charts ── */
.charts-section {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: var(--space-5);
  margin-bottom: var(--space-8);
}

.chart-card {
  background: var(--color-bg-card);
  border: 1px solid rgba(255, 255, 255, 0.04);
  border-radius: var(--radius-lg);
  padding: var(--space-5);
  animation: fadeInUp 0.6s var(--ease-out) 0.3s both;
}

.chart-header {
  margin-bottom: var(--space-3);
}

.chart-header h3 {
  font-family: var(--font-chinese);
  font-size: var(--text-base);
  font-weight: 600;
  color: var(--color-text-primary);
}

.chart-sub {
  font-size: var(--text-xs);
  color: var(--color-text-muted);
}

.chart-body {
  width: 100%;
  height: 260px;
}

/* ── Spots ── */
.spots-section {
  margin-bottom: var(--space-8);
}

.section-header {
  margin-bottom: var(--space-5);
}

.section-header h2 {
  font-family: var(--font-chinese);
  font-size: var(--text-2xl);
  font-weight: 700;
}

.section-sub {
  font-size: var(--text-sm);
  color: var(--color-text-muted);
}

.spots-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-4);
}

.spot-card {
  background: var(--color-bg-card);
  border: 1px solid rgba(255, 255, 255, 0.04);
  border-radius: var(--radius-lg);
  padding: var(--space-5);
  display: flex;
  align-items: center;
  gap: var(--space-4);
  cursor: pointer;
  transition: all var(--duration-normal) var(--ease-out);
}

.spot-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
  border-color: rgba(255, 255, 255, 0.08);
}

.spot-rank {
  width: 56px;
  height: 56px;
  border-radius: var(--radius-md);
  background: var(--color-primary-glow);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.spot-score {
  font-family: var(--font-display);
  font-size: var(--text-xl);
  font-weight: 700;
  color: var(--color-primary-light);
  line-height: 1;
}

.spot-score-label {
  font-size: var(--text-xs);
  color: var(--color-text-muted);
}

.spot-info {
  flex: 1;
  min-width: 0;
}

.spot-name {
  font-family: var(--font-chinese);
  font-size: var(--text-base);
  font-weight: 600;
  margin-bottom: var(--space-1);
}

.spot-desc {
  font-size: var(--text-sm);
  color: var(--color-text-muted);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.spot-arrow {
  color: var(--color-text-muted);
  transition: transform var(--duration-fast) var(--ease-out);
}

.spot-card:hover .spot-arrow {
  transform: translateX(4px);
  color: var(--color-primary-light);
}
</style>
