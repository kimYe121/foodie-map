/** 店铺信息 */
export interface Shop {
  shopId: string
  name: string
  category: string
  categoryName: string
  rating: number
  priceAvg: number
  address: string
  longitude: number
  latitude: number
  phone: string
  businessHours: string
  tags: string[]
  source: string
  viewCount: number
  shopImage: string
  images: string[]
  foodImages: string[]
  videoUrl: string
  likeCount: number
  commentCount: number
  distance?: number
  costPerformance?: number
  rank?: number
  createTime: string
  updateTime: string
}

/** 景点信息 */
export interface Spot {
  spotId: string
  name: string
  longitude: number
  latitude: number
  description: string
  hotScore: number
  createTime: string
}

/** 排行榜项 */
export interface RankItem {
  shopId: string
  name: string
  category: string
  categoryName: string
  rating: number
  priceAvg: number
  address: string
  tags: string[]
  rank: number
  costPerformance?: number
  viewCount?: number
  distance?: number
}

/** 分页结果 */
export interface PageResult<T> {
  list: T[]
  page: number
  size: number
  total: number
  pages: number
}

/** API 统一响应 */
export interface ApiResponse<T = any> {
  code: number
  message: string
  data: T
  timestamp: number
  traceId: string
}

/** 分类统计 */
export interface CategoryStat {
  category: string
  categoryName: string
  count: number
}

/** 价格统计 */
export interface PriceStat {
  range: string
  count: number
}

/** 评分统计 */
export interface RatingStat {
  avgRating: number
  highRatingCount: number
  totalRatingCount: number
}

/** 首页统计 */
export interface OverviewStats {
  totalShops: number
  totalSpots: number
  categoryStats: CategoryStat[]
  priceStats: PriceStat[]
  ratingStats: RatingStat
}

/** 消费场景 */
export type ConsumScene = 'economic' | 'popular' | 'quality' | 'premium'

/** 消费场景配置 */
export interface SceneConfig {
  key: ConsumScene
  label: string
  range: string
  icon: string
  color: string
}

/** 地图店铺点 */
export interface MapShopPoint {
  shopId: string
  name: string
  longitude: number
  latitude: number
  rating: number
  priceAvg: number
  category: string
}

/** 当地特色分析数据 */
export interface LocalFeatureData {
  topDishes: { name: string; count: number }[]
  categoryRating: { category: string; avgRating: number; count: number }[]
  priceRatingScatter: { name: string; price: number; rating: number; category: string }[]
  sentimentSummary: { positive: number; neutral: number; negative: number }
}

/** 多城市对比数据 */
export interface CityCompareData {
  cities: string[]
  priceComparison: { city: string; avgPrice: number; medianPrice: number }[]
  ratingComparison: { city: string; avgRating: number }[]
  categoryComparison: { category: string; data: { city: string; count: number }[] }[]
}
