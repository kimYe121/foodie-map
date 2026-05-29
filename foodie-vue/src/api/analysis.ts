import http from './index'
import type { OverviewStats, LocalFeatureData, CityCompareData, MapShopPoint } from '@/types'

/** 首页统计 */
export function getOverviewStats() {
  return http.get<OverviewStats>('/stats/overview')
}

/** 当地特色分析 */
export function getLocalFeatureAnalysis() {
  return http.get<LocalFeatureData>('/analysis/local-feature')
}

/** 性价比分析 */
export function getCostPerformanceAnalysis(scene?: string) {
  return http.get<any>('/analysis/cost-performance', { params: { scene } })
}

/** 多城市对比 */
export function getCityCompareData() {
  return http.get<CityCompareData>('/analysis/city-compare')
}

/** 词云数据 */
export function getWordCloudData() {
  return http.get<{ name: string; value: number }[]>('/analysis/word-cloud')
}

/** 地图店铺数据 */
export function getMapShops(params: {
  minLng?: number
  maxLng?: number
  minLat?: number
  maxLat?: number
  category?: string
  limit?: number
}) {
  return http.get<{ list: MapShopPoint[]; total: number }>('/map/shops', { params })
}
