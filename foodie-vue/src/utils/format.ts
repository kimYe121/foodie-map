/** 格式化价格 */
export function formatPrice(price: number): string {
  return `¥${price}`
}

/** 格式化评分 */
export function formatRating(rating: number): string {
  return rating.toFixed(1)
}

/** 计算性价比指数 */
export function calcCostPerf(rating: number, price: number): number {
  if (!price || !rating) return 0
  return Math.round((rating / price) * 1000) / 10
}

/** 消费场景定义 */
export const SCENE_CONFIG = [
  { key: 'economic', label: '经济型', range: '< ¥30', icon: 'Coin', color: '#5a7247' },
  { key: 'popular', label: '大众型', range: '¥30 - 80', icon: 'Bowl', color: '#d4a03c' },
  { key: 'quality', label: '品质型', range: '¥80 - 150', icon: 'Dish', color: '#c05621' },
  { key: 'premium', label: '高端型', range: '> ¥150', icon: 'Goblet', color: '#a03030' },
] as const

/** 分类配色 */
export const CATEGORY_COLORS: Record<string, string> = {
  jiangxi: '#c05621',
  hotpot: '#a03030',
  snack: '#d4a03c',
  bbq: '#8b3a14',
  western: '#4a7090',
  japan_korea: '#6a5a8c',
  seafood: '#3a7a7a',
  dessert: '#c07090',
  cantonese: '#5a7247',
  sichuan: '#c04040',
  hunan: '#e07a3a',
  buffet: '#7090a0',
  noodles: '#b08040',
  other: '#6b6660',
}

/** 格式化数字（万） */
export function formatCount(count: number): string {
  if (count >= 10000) return (count / 10000).toFixed(1) + '万'
  if (count >= 1000) return (count / 1000).toFixed(1) + 'k'
  return String(count)
}

/** 获取评分等级 */
export function getRatingLevel(rating: number): { label: string; color: string } {
  if (rating >= 4.5) return { label: '优秀', color: '#4a8c5c' }
  if (rating >= 4.0) return { label: '良好', color: '#5a7247' }
  if (rating >= 3.5) return { label: '一般', color: '#d4a03c' }
  if (rating >= 3.0) return { label: '较差', color: '#c05621' }
  return { label: '差', color: '#a03030' }
}

/** 数据来源标签 */
export const SOURCE_LABELS: Record<string, string> = {
  dianping: '大众点评',
  meituan: '美团',
  xiaohongshu: '小红书',
  douyin: '抖音',
  manual: '手动录入',
}
