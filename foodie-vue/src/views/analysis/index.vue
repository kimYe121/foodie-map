<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import * as echarts from 'echarts'
import { SCENE_CONFIG, CATEGORY_COLORS } from '@/utils/format'

const route = useRoute()
const analysisType = computed(() => route.meta.analysisType as string)

const pageTitle = computed(() => {
  const map: Record<string, string> = {
    local: '当地特色分析',
    costPerformance: '性价比分析',
    cityCompare: '多城市对比',
  }
  return map[analysisType.value] || '数据分析'
})

// ── Chart refs ──
const wordCloudRef = ref<HTMLElement>()
const scatterRef = ref<HTMLElement>()
const radarRef = ref<HTMLElement>()
const barRef = ref<HTMLElement>()
const cityPriceRef = ref<HTMLElement>()
const cityRatingRef = ref<HTMLElement>()

onMounted(() => {
  if (analysisType.value === 'local') {
    initWordCloud()
    initScatter()
  } else if (analysisType.value === 'costPerformance') {
    initRadar()
    initBar()
  } else if (analysisType.value === 'cityCompare') {
    initCityPrice()
    initCityRating()
  }
})

// ── Local Feature Analysis ──
function initWordCloud() {
  if (!wordCloudRef.value) return
  const chart = echarts.init(wordCloudRef.value)
  const data = [
    { name: '南昌拌粉', value: 100 },
    { name: '瓦罐汤', value: 90 },
    { name: '白糖糕', value: 70 },
    { name: '藜蒿炒腊肉', value: 85 },
    { name: '三杯鸡', value: 75 },
    { name: '米粉蒸肉', value: 65 },
    { name: '南昌炒粉', value: 80 },
    { name: '酒糟鱼', value: 55 },
    { name: '辣椒饼', value: 45 },
    { name: '油炸桧', value: 40 },
    { name: '石头街麻花', value: 50 },
    { name: '风味烤卤', value: 60 },
  ]

  chart.setOption({
    tooltip: {
      backgroundColor: '#1e1e2e',
      borderColor: 'rgba(255,255,255,0.06)',
      textStyle: { color: '#f0ece4' },
    },
    series: [{
      type: 'wordCloud',
      shape: 'circle',
      left: 'center',
      top: 'center',
      width: '90%',
      height: '90%',
      sizeRange: [14, 48],
      rotationRange: [-30, 30],
      rotationStep: 15,
      gridSize: 12,
      drawOutOfBound: false,
      textStyle: {
        fontFamily: 'Noto Serif SC, serif',
        fontWeight: 600,
        color: () => {
          const colors = ['#c05621', '#d4a03c', '#5a7247', '#a03030', '#4a7090', '#8b3a14']
          return colors[Math.floor(Math.random() * colors.length)]
        },
      },
      emphasis: {
        textStyle: { textShadowBlur: 10, textShadowColor: 'rgba(192, 86, 33, 0.5)' },
      },
      data,
    }],
  })
  window.addEventListener('resize', () => chart.resize())
}

function initScatter() {
  if (!scatterRef.value) return
  const chart = echarts.init(scatterRef.value)
  const data = [
    { name: '老三样', price: 65, rating: 4.8, category: '江西菜' },
    { name: '堂瓦里', price: 80, rating: 4.7, category: '江西菜' },
    { name: '周真真粉面馆', price: 25, rating: 4.5, category: '小吃' },
    { name: '味福记', price: 35, rating: 4.3, category: '小吃' },
    { name: '民间饭庄', price: 70, rating: 4.6, category: '江西菜' },
    { name: '无名火锅', price: 95, rating: 4.4, category: '火锅' },
    { name: '阿婆烧烤', price: 55, rating: 4.3, category: '烧烤' },
    { name: '鹿港小镇', price: 120, rating: 4.2, category: '日料' },
    { name: '茶百道', price: 18, rating: 4.1, category: '甜品' },
    { name: '老南昌白糖糕', price: 15, rating: 4.6, category: '小吃' },
  ]

  const catColors: Record<string, string> = {
    '江西菜': '#c05621', '小吃': '#d4a03c', '火锅': '#a03030',
    '烧烤': '#8b3a14', '日料': '#6a5a8c', '甜品': '#c07090',
  }

  chart.setOption({
    tooltip: {
      backgroundColor: '#1e1e2e',
      borderColor: 'rgba(255,255,255,0.06)',
      textStyle: { color: '#f0ece4' },
      formatter: (p: any) => `${p.data[3]}<br/>价格: ¥${p.data[0]}/人<br/>评分: ${p.data[1]}`,
    },
    grid: { top: 40, right: 40, bottom: 50, left: 60 },
    xAxis: {
      name: '人均消费 (元)',
      nameTextStyle: { color: '#a8a3a0', fontSize: 11 },
      axisLine: { lineStyle: { color: 'rgba(255,255,255,0.06)' } },
      axisLabel: { color: '#6b6660' },
      splitLine: { lineStyle: { color: 'rgba(255,255,255,0.03)' } },
    },
    yAxis: {
      name: '评分',
      nameTextStyle: { color: '#a8a3a0', fontSize: 11 },
      min: 3.8,
      max: 5.0,
      axisLine: { lineStyle: { color: 'rgba(255,255,255,0.06)' } },
      axisLabel: { color: '#6b6660' },
      splitLine: { lineStyle: { color: 'rgba(255,255,255,0.03)' } },
    },
    series: [{
      type: 'scatter',
      symbolSize: (val: number) => Math.max(12, val[1] * 6),
      data: data.map(d => [d.price, d.rating, d.category, d.name]),
      itemStyle: {
        color: (params: any) => catColors[params.data[2]] || '#6b6660',
        shadowBlur: 10,
        shadowColor: 'rgba(0,0,0,0.3)',
      },
      emphasis: {
        itemStyle: { shadowBlur: 20, shadowColor: 'rgba(192, 86, 33, 0.5)' },
      },
    }],
    legend: {
      data: Object.keys(catColors).map(k => ({
        name: k,
        itemStyle: { color: catColors[k] },
      })),
      textStyle: { color: '#a8a3a0', fontSize: 11 },
      bottom: 0,
    },
  })
  window.addEventListener('resize', () => chart.resize())
}

// ── Cost Performance Analysis ──
function initRadar() {
  if (!radarRef.value) return
  const chart = echarts.init(radarRef.value)
  chart.setOption({
    tooltip: {
      backgroundColor: '#1e1e2e',
      borderColor: 'rgba(255,255,255,0.06)',
      textStyle: { color: '#f0ece4' },
    },
    radar: {
      indicator: [
        { name: '口味', max: 5 },
        { name: '环境', max: 5 },
        { name: '服务', max: 5 },
        { name: '性价比', max: 5 },
        { name: '位置', max: 5 },
        { name: '特色', max: 5 },
      ],
      axisName: { color: '#a8a3a0', fontSize: 12 },
      splitArea: { areaStyle: { color: ['rgba(255,255,255,0.01)', 'rgba(255,255,255,0.02)'] } },
      splitLine: { lineStyle: { color: 'rgba(255,255,255,0.04)' } },
      axisLine: { lineStyle: { color: 'rgba(255,255,255,0.06)' } },
    },
    legend: {
      data: ['经济型 TOP', '大众型 TOP', '品质型 TOP'],
      textStyle: { color: '#a8a3a0', fontSize: 11 },
      bottom: 0,
    },
    series: [{
      type: 'radar',
      data: [
        {
          name: '经济型 TOP',
          value: [4.5, 3.8, 4.0, 4.8, 4.2, 4.6],
          areaStyle: { color: 'rgba(90, 114, 71, 0.15)' },
          lineStyle: { color: '#5a7247', width: 2 },
          itemStyle: { color: '#5a7247' },
        },
        {
          name: '大众型 TOP',
          value: [4.7, 4.2, 4.3, 4.5, 4.0, 4.4],
          areaStyle: { color: 'rgba(212, 160, 60, 0.15)' },
          lineStyle: { color: '#d4a03c', width: 2 },
          itemStyle: { color: '#d4a03c' },
        },
        {
          name: '品质型 TOP',
          value: [4.8, 4.6, 4.5, 3.8, 4.5, 4.2],
          areaStyle: { color: 'rgba(192, 86, 33, 0.15)' },
          lineStyle: { color: '#c05621', width: 2 },
          itemStyle: { color: '#c05621' },
        },
      ],
    }],
  })
  window.addEventListener('resize', () => chart.resize())
}

function initBar() {
  if (!barRef.value) return
  const chart = echarts.init(barRef.value)
  const scenes = SCENE_CONFIG
  chart.setOption({
    tooltip: {
      trigger: 'axis',
      backgroundColor: '#1e1e2e',
      borderColor: 'rgba(255,255,255,0.06)',
      textStyle: { color: '#f0ece4' },
    },
    grid: { top: 30, right: 20, bottom: 50, left: 60 },
    xAxis: {
      type: 'category',
      data: ['周真真粉面馆', '老南昌白糖糕', '茶百道', '味福记', '老三样', '民间饭庄', '无名火锅', '鹿港小镇'],
      axisLine: { lineStyle: { color: 'rgba(255,255,255,0.06)' } },
      axisLabel: { color: '#a8a3a0', fontSize: 10, rotate: 30 },
    },
    yAxis: {
      name: '性价比指数',
      nameTextStyle: { color: '#a8a3a0', fontSize: 11 },
      axisLine: { lineStyle: { color: 'rgba(255,255,255,0.06)' } },
      axisLabel: { color: '#6b6660' },
      splitLine: { lineStyle: { color: 'rgba(255,255,255,0.03)' } },
    },
    series: [{
      type: 'bar',
      data: [
        { value: 18.0, itemStyle: { color: '#5a7247' } },
        { value: 30.7, itemStyle: { color: '#5a7247' } },
        { value: 22.8, itemStyle: { color: '#5a7247' } },
        { value: 12.3, itemStyle: { color: '#d4a03c' } },
        { value: 7.4, itemStyle: { color: '#d4a03c' } },
        { value: 6.6, itemStyle: { color: '#d4a03c' } },
        { value: 4.6, itemStyle: { color: '#c05621' } },
        { value: 3.5, itemStyle: { color: '#c05621' } },
      ],
      barWidth: '50%',
      itemStyle: { borderRadius: [4, 4, 0, 0] },
    }],
  })
  window.addEventListener('resize', () => chart.resize())
}

// ── City Compare ──
function initCityPrice() {
  if (!cityPriceRef.value) return
  const chart = echarts.init(cityPriceRef.value)
  chart.setOption({
    tooltip: {
      trigger: 'axis',
      backgroundColor: '#1e1e2e',
      borderColor: 'rgba(255,255,255,0.06)',
      textStyle: { color: '#f0ece4' },
    },
    legend: {
      data: ['平均消费', '中位数'],
      textStyle: { color: '#a8a3a0', fontSize: 11 },
      right: 0,
    },
    grid: { top: 40, right: 20, bottom: 30, left: 60 },
    xAxis: {
      type: 'category',
      data: ['南昌', '武汉', '长沙'],
      axisLine: { lineStyle: { color: 'rgba(255,255,255,0.06)' } },
      axisLabel: { color: '#a8a3a0', fontSize: 12 },
    },
    yAxis: {
      name: '元/人',
      nameTextStyle: { color: '#a8a3a0', fontSize: 11 },
      axisLine: { lineStyle: { color: 'rgba(255,255,255,0.06)' } },
      axisLabel: { color: '#6b6660' },
      splitLine: { lineStyle: { color: 'rgba(255,255,255,0.03)' } },
    },
    series: [
      {
        name: '平均消费',
        type: 'bar',
        data: [52, 68, 61],
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#c05621' },
            { offset: 1, color: '#c0562180' },
          ]),
          borderRadius: [4, 4, 0, 0],
        },
        barWidth: '30%',
      },
      {
        name: '中位数',
        type: 'bar',
        data: [45, 58, 52],
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#d4a03c' },
            { offset: 1, color: '#d4a03c80' },
          ]),
          borderRadius: [4, 4, 0, 0],
        },
        barWidth: '30%',
      },
    ],
  })
  window.addEventListener('resize', () => chart.resize())
}

function initCityRating() {
  if (!cityRatingRef.value) return
  const chart = echarts.init(cityRatingRef.value)
  chart.setOption({
    tooltip: {
      trigger: 'axis',
      backgroundColor: '#1e1e2e',
      borderColor: 'rgba(255,255,255,0.06)',
      textStyle: { color: '#f0ece4' },
    },
    grid: { top: 30, right: 20, bottom: 30, left: 60 },
    xAxis: {
      type: 'category',
      data: ['南昌', '武汉', '长沙'],
      axisLine: { lineStyle: { color: 'rgba(255,255,255,0.06)' } },
      axisLabel: { color: '#a8a3a0', fontSize: 12 },
    },
    yAxis: {
      name: '平均评分',
      min: 3.5,
      max: 5.0,
      nameTextStyle: { color: '#a8a3a0', fontSize: 11 },
      axisLine: { lineStyle: { color: 'rgba(255,255,255,0.06)' } },
      axisLabel: { color: '#6b6660' },
      splitLine: { lineStyle: { color: 'rgba(255,255,255,0.03)' } },
    },
    series: [{
      type: 'bar',
      data: [
        { value: 4.2, itemStyle: { color: '#c05621', borderRadius: [4, 4, 0, 0] } },
        { value: 4.3, itemStyle: { color: '#5a7247', borderRadius: [4, 4, 0, 0] } },
        { value: 4.4, itemStyle: { color: '#d4a03c', borderRadius: [4, 4, 0, 0] } },
      ],
      barWidth: '35%',
    }],
  })
  window.addEventListener('resize', () => chart.resize())
}
</script>

<template>
  <div class="analysis-page">
    <div class="page-header">
      <h1 class="page-title">
        <span class="title-icon">📊</span>
        {{ pageTitle }}
      </h1>
    </div>

    <!-- Local Feature Analysis -->
    <template v-if="analysisType === 'local'">
      <div class="section-title">
        <h2>🍜 当地特色菜品</h2>
        <p>南昌高频出现的特色美食关键词</p>
      </div>
      <div class="chart-card full">
        <div ref="wordCloudRef" class="chart-body tall" />
      </div>

      <div class="section-title">
        <h2>💰 价格与评分关系</h2>
        <p>分析是否存在"名气大但性价比低"的问题</p>
      </div>
      <div class="chart-card full">
        <div ref="scatterRef" class="chart-body tall" />
      </div>
    </template>

    <!-- Cost Performance Analysis -->
    <template v-if="analysisType === 'costPerformance'">
      <div class="scene-cards stagger-reveal">
        <div
          v-for="scene in SCENE_CONFIG"
          :key="scene.key"
          class="scene-card"
          :style="{ '--scene-color': scene.color }"
        >
          <div class="scene-icon">{{ { economic: '🎒', popular: '🍜', quality: '🍽️', premium: '🥂' }[scene.key] }}</div>
          <h3>{{ scene.label }}</h3>
          <p class="scene-range">{{ scene.range }}</p>
        </div>
      </div>

      <div class="charts-row">
        <div class="chart-card">
          <div class="chart-header">
            <h3>多维度性价比雷达图</h3>
            <span class="chart-sub">各消费场景 TOP 店铺对比</span>
          </div>
          <div ref="radarRef" class="chart-body" />
        </div>
        <div class="chart-card">
          <div class="chart-header">
            <h3>性价比指数排行</h3>
            <span class="chart-sub">性价比 = 评分 / 人均消费 × 10</span>
          </div>
          <div ref="barRef" class="chart-body" />
        </div>
      </div>
    </template>

    <!-- City Compare -->
    <template v-if="analysisType === 'cityCompare'">
      <div class="city-cards stagger-reveal">
        <div class="city-card" style="--city-color: #c05621">
          <h3>南昌</h3>
          <div class="city-stats">
            <span class="city-stat"><strong>52</strong>元/人</span>
            <span class="city-stat"><strong>4.2</strong>评分</span>
          </div>
          <p class="city-tag">性价比之王</p>
        </div>
        <div class="city-card" style="--city-color: #5a7247">
          <h3>武汉</h3>
          <div class="city-stats">
            <span class="city-stat"><strong>68</strong>元/人</span>
            <span class="city-stat"><strong>4.3</strong>评分</span>
          </div>
          <p class="city-tag">品类丰富</p>
        </div>
        <div class="city-card" style="--city-color: #d4a03c">
          <h3>长沙</h3>
          <div class="city-stats">
            <span class="city-stat"><strong>61</strong>元/人</span>
            <span class="city-stat"><strong>4.4</strong>评分</span>
          </div>
          <p class="city-tag">网红聚集</p>
        </div>
      </div>

      <div class="charts-row">
        <div class="chart-card">
          <div class="chart-header">
            <h3>消费水平对比</h3>
            <span class="chart-sub">各城市人均消费</span>
          </div>
          <div ref="cityPriceRef" class="chart-body" />
        </div>
        <div class="chart-card">
          <div class="chart-header">
            <h3>评分对比</h3>
            <span class="chart-sub">各城市平均评分</span>
          </div>
          <div ref="cityRatingRef" class="chart-body" />
        </div>
      </div>
    </template>
  </div>
</template>

<style scoped>
.analysis-page {
  padding: var(--space-8);
  max-width: var(--content-max);
  margin: 0 auto;
}

.page-header {
  margin-bottom: var(--space-6);
}

.page-title {
  font-family: var(--font-display);
  font-size: var(--text-3xl);
  font-weight: 800;
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.title-icon {
  font-size: var(--text-2xl);
}

.section-title {
  margin-bottom: var(--space-4);
  margin-top: var(--space-8);
}

.section-title h2 {
  font-family: var(--font-chinese);
  font-size: var(--text-xl);
  font-weight: 600;
  margin-bottom: var(--space-1);
}

.section-title p {
  font-size: var(--text-sm);
  color: var(--color-text-muted);
}

.chart-card {
  background: var(--color-bg-card);
  border: 1px solid rgba(255, 255, 255, 0.04);
  border-radius: var(--radius-lg);
  padding: var(--space-5);
  animation: fadeInUp 0.6s var(--ease-out) 0.2s both;
}

.chart-card.full {
  margin-bottom: var(--space-4);
}

.chart-header {
  margin-bottom: var(--space-3);
}

.chart-header h3 {
  font-family: var(--font-chinese);
  font-size: var(--text-base);
  font-weight: 600;
}

.chart-sub {
  font-size: var(--text-xs);
  color: var(--color-text-muted);
}

.chart-body {
  width: 100%;
  height: 320px;
}

.chart-body.tall {
  height: 400px;
}

.charts-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-5);
  margin-top: var(--space-5);
}

/* ── Scene Cards ── */
.scene-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--space-4);
  margin-bottom: var(--space-6);
}

.scene-card {
  background: var(--color-bg-card);
  border: 1px solid rgba(255, 255, 255, 0.04);
  border-radius: var(--radius-lg);
  padding: var(--space-5);
  text-align: center;
  transition: all var(--duration-normal) var(--ease-out);
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.scene-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: var(--scene-color);
}

.scene-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-md);
}

.scene-icon {
  font-size: 2rem;
  margin-bottom: var(--space-2);
}

.scene-card h3 {
  font-family: var(--font-chinese);
  font-size: var(--text-base);
  font-weight: 600;
  margin-bottom: var(--space-1);
}

.scene-range {
  font-size: var(--text-sm);
  color: var(--color-text-muted);
}

/* ── City Cards ── */
.city-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-5);
  margin-bottom: var(--space-6);
}

.city-card {
  background: var(--color-bg-card);
  border: 1px solid rgba(255, 255, 255, 0.04);
  border-radius: var(--radius-lg);
  padding: var(--space-6);
  text-align: center;
  transition: all var(--duration-normal) var(--ease-out);
  position: relative;
  overflow: hidden;
}

.city-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: var(--city-color);
}

.city-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-md);
}

.city-card h3 {
  font-family: var(--font-chinese);
  font-size: var(--text-2xl);
  font-weight: 700;
  margin-bottom: var(--space-3);
}

.city-stats {
  display: flex;
  justify-content: center;
  gap: var(--space-6);
  margin-bottom: var(--space-3);
}

.city-stat {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
}

.city-stat strong {
  font-family: var(--font-display);
  font-size: var(--text-xl);
  color: var(--color-text-primary);
  margin-right: 2px;
}

.city-tag {
  font-size: var(--text-xs);
  color: var(--color-text-muted);
  padding: 2px 10px;
  background: rgba(255, 255, 255, 0.04);
  border-radius: var(--radius-full);
  display: inline-block;
}
</style>
