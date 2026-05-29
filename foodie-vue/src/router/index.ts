import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: () => import('@/layouts/MainLayout.vue'),
      redirect: '/home',
      children: [
        {
          path: 'home',
          name: 'Home',
          component: () => import('@/views/home/index.vue'),
          meta: { title: '首页总览', icon: 'House' },
        },
        {
          path: 'rank',
          name: 'Rank',
          redirect: '/rank/overall',
          meta: { title: '排行榜', icon: 'Trophy' },
          children: [
            {
              path: 'overall',
              name: 'RankOverall',
              component: () => import('@/views/rank/index.vue'),
              meta: { title: '综合评分榜', rankType: 'overall' },
            },
            {
              path: 'cost-performance',
              name: 'RankCostPerf',
              component: () => import('@/views/rank/index.vue'),
              meta: { title: '性价比榜', rankType: 'costPerformance' },
            },
            {
              path: 'hot',
              name: 'RankHot',
              component: () => import('@/views/rank/index.vue'),
              meta: { title: '热门榜', rankType: 'hot' },
            },
            {
              path: 'category/:category?',
              name: 'RankCategory',
              component: () => import('@/views/rank/index.vue'),
              meta: { title: '分类榜', rankType: 'category' },
            },
          ],
        },
        {
          path: 'map',
          name: 'Map',
          component: () => import('@/views/map/index.vue'),
          meta: { title: '美食地图', icon: 'MapLocation' },
        },
        {
          path: 'analysis',
          name: 'Analysis',
          redirect: '/analysis/local',
          meta: { title: '数据分析', icon: 'DataAnalysis' },
          children: [
            {
              path: 'local',
              name: 'AnalysisLocal',
              component: () => import('@/views/analysis/index.vue'),
              meta: { title: '当地特色分析', analysisType: 'local' },
            },
            {
              path: 'cost-performance',
              name: 'AnalysisCostPerf',
              component: () => import('@/views/analysis/index.vue'),
              meta: { title: '性价比分析', analysisType: 'costPerformance' },
            },
            {
              path: 'city-compare',
              name: 'AnalysisCityCompare',
              component: () => import('@/views/analysis/index.vue'),
              meta: { title: '多城市对比', analysisType: 'cityCompare' },
            },
          ],
        },
        {
          path: 'shop/:shopId',
          name: 'ShopDetail',
          component: () => import('@/views/shop/detail.vue'),
          meta: { title: '店铺详情', hidden: true },
        },
      ],
    },
  ],
})

router.beforeEach((to, _from, next) => {
  document.title = `${to.meta.title || '美食地图'} — FoodieMap`
  next()
})

export default router
