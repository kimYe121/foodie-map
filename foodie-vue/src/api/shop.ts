import http from './index'
import type { Shop, PageResult, Spot } from '@/types'

/** 店铺详情 */
export function getShopDetail(shopId: string) {
  return http.get<Shop>(`/shop/${shopId}`)
}

/** 店铺列表 */
export function getShopList(params: {
  page?: number
  size?: number
  keyword?: string
  category?: string
  minRating?: number
  maxPrice?: number
  minPrice?: number
  sortBy?: string
  sortOrder?: string
}) {
  return http.get<PageResult<Shop>>('/shop/list', { params })
}

/** 搜索店铺 */
export function searchShops(keyword: string, page = 1, size = 20) {
  return http.get<PageResult<Shop>>('/shop/search', { params: { keyword, page, size } })
}

/** 景点列表 */
export function getSpotList() {
  return http.get<Spot[]>('/spot/list')
}

/** 景点周边美食 */
export function getNearbyShops(spotId: string, radius = 3, limit = 50, sortBy = 'distance') {
  return http.get<{ spot: Spot; radius: number; list: Shop[]; total: number }>(
    `/spot/${spotId}/nearby`,
    { params: { radius, limit, sortBy } },
  )
}
