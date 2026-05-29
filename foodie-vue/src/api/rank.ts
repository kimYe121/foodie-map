import http from './index'
import type { RankItem, PageResult } from '@/types'

/** 综合评分榜 */
export function getOverallRank(limit = 10, category?: string) {
  return http.get<RankItem[]>('/rank/overall', { params: { limit, category } })
}

/** 性价比榜 */
export function getCostPerfRank(limit = 10, maxPrice?: number, category?: string) {
  return http.get<RankItem[]>('/rank/cost-performance', { params: { limit, maxPrice, category } })
}

/** 热门榜 */
export function getHotRank(limit = 10, period = 'week') {
  return http.get<RankItem[]>('/rank/hot', { params: { limit, period } })
}

/** 分类榜 */
export function getCategoryRank(category: string, limit = 10, sortBy = 'rating') {
  return http.get<{ category: string; categoryName: string; list: RankItem[]; total: number }>(
    `/rank/category/${category}`,
    { params: { limit, sortBy } },
  )
}
