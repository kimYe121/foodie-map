import { defineStore } from 'pinia'
import type { OverviewStats, CategoryStat } from '@/types'

export const useAppStore = defineStore('app', () => {
  const sidebarCollapsed = ref(false)
  const loading = ref(false)
  const overviewStats = ref<OverviewStats | null>(null)
  const categories = ref<CategoryStat[]>([])

  function toggleSidebar() {
    sidebarCollapsed.value = !sidebarCollapsed.value
  }

  function setLoading(val: boolean) {
    loading.value = val
  }

  function setOverviewStats(stats: OverviewStats) {
    overviewStats.value = stats
    categories.value = stats.categoryStats || []
  }

  return {
    sidebarCollapsed,
    loading,
    overviewStats,
    categories,
    toggleSidebar,
    setLoading,
    setOverviewStats,
  }
})
