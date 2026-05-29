<script setup lang="ts">
import { useAppStore } from '@/stores/app'

const route = useRoute()
const appStore = useAppStore()

const menuItems = [
  { path: '/home', icon: 'House', title: '首页总览' },
  {
    path: '/rank',
    icon: 'Trophy',
    title: '排行榜',
    children: [
      { path: '/rank/overall', title: '综合评分榜' },
      { path: '/rank/cost-performance', title: '性价比榜' },
      { path: '/rank/hot', title: '热门榜' },
      { path: '/rank/category', title: '分类榜' },
    ],
  },
  { path: '/map', icon: 'MapLocation', title: '美食地图' },
  {
    path: '/analysis',
    icon: 'DataAnalysis',
    title: '数据分析',
    children: [
      { path: '/analysis/local', title: '当地特色分析' },
      { path: '/analysis/cost-performance', title: '性价比分析' },
      { path: '/analysis/city-compare', title: '多城市对比' },
    ],
  },
]

const isCollapsed = computed(() => appStore.sidebarCollapsed)
</script>

<template>
  <div class="layout">
    <!-- Sidebar -->
    <aside class="sidebar" :class="{ collapsed: isCollapsed }">
      <!-- Logo -->
      <div class="sidebar-logo">
        <div class="logo-icon">
          <svg viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="16" cy="16" r="14" fill="url(#logo-grad)" opacity="0.9"/>
            <path d="M10 20c2-4 4-6 6-6s4 2 6 6" stroke="#fff" stroke-width="2" stroke-linecap="round"/>
            <circle cx="16" cy="11" r="3" fill="#fff" opacity="0.9"/>
            <defs>
              <linearGradient id="logo-grad" x1="4" y1="4" x2="28" y2="28">
                <stop stop-color="#c05621"/>
                <stop offset="1" stop-color="#d4a03c"/>
              </linearGradient>
            </defs>
          </svg>
        </div>
        <transition name="fade">
          <div v-if="!isCollapsed" class="logo-text">
            <span class="logo-title">FoodieMap</span>
            <span class="logo-sub">南昌美食可视化</span>
          </div>
        </transition>
      </div>

      <div class="divider" />

      <!-- Navigation -->
      <nav class="sidebar-nav">
        <template v-for="item in menuItems" :key="item.path">
          <!-- Single item -->
          <router-link
            v-if="!item.children"
            :to="item.path"
            class="nav-item"
            :class="{ active: route.path === item.path }"
          >
            <el-icon :size="20"><component :is="item.icon" /></el-icon>
            <transition name="fade">
              <span v-if="!isCollapsed" class="nav-label">{{ item.title }}</span>
            </transition>
          </router-link>

          <!-- Group with children -->
          <div v-else class="nav-group">
            <div class="nav-group-header">
              <el-icon :size="20"><component :is="item.icon" /></el-icon>
              <transition name="fade">
                <span v-if="!isCollapsed" class="nav-label">{{ item.title }}</span>
              </transition>
            </div>
            <transition name="expand">
              <div v-if="!isCollapsed" class="nav-group-children">
                <router-link
                  v-for="child in item.children"
                  :key="child.path"
                  :to="child.path"
                  class="nav-child"
                  :class="{ active: route.path === child.path }"
                >
                  {{ child.title }}
                </router-link>
              </div>
            </transition>
          </div>
        </template>
      </nav>

      <!-- Collapse toggle -->
      <div class="sidebar-footer">
        <button class="collapse-btn" @click="appStore.toggleSidebar()">
          <el-icon :size="18">
            <component :is="isCollapsed ? 'Expand' : 'Fold'" />
          </el-icon>
        </button>
      </div>
    </aside>

    <!-- Main content -->
    <main class="main-content" :class="{ expanded: isCollapsed }">
      <router-view v-slot="{ Component }">
        <transition name="page" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
  </div>
</template>

<style scoped>
.layout {
  display: flex;
  min-height: 100vh;
}

/* ── Sidebar ── */
.sidebar {
  width: var(--sidebar-width);
  background: var(--color-bg-primary);
  border-right: 1px solid rgba(255, 255, 255, 0.04);
  display: flex;
  flex-direction: column;
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  z-index: 100;
  transition: width var(--duration-normal) var(--ease-out);
  overflow: hidden;
}

.sidebar.collapsed {
  width: var(--sidebar-collapsed);
}

.sidebar-logo {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-5) var(--space-4);
  min-height: 72px;
}

.logo-icon svg {
  width: 36px;
  height: 36px;
  flex-shrink: 0;
}

.logo-text {
  display: flex;
  flex-direction: column;
  white-space: nowrap;
}

.logo-title {
  font-family: var(--font-display);
  font-size: var(--text-lg);
  font-weight: 700;
  background: linear-gradient(135deg, var(--color-primary-light), var(--color-gold));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.logo-sub {
  font-size: var(--text-xs);
  color: var(--color-text-muted);
  letter-spacing: 0.05em;
}

/* ── Navigation ── */
.sidebar-nav {
  flex: 1;
  padding: var(--space-3) var(--space-2);
  overflow-y: auto;
  overflow-x: hidden;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  border-radius: var(--radius-md);
  color: var(--color-text-secondary);
  font-size: var(--text-sm);
  font-weight: 500;
  transition: all var(--duration-fast) var(--ease-out);
  text-decoration: none;
  margin-bottom: 2px;
  white-space: nowrap;
}

.nav-item:hover {
  color: var(--color-text-primary);
  background: var(--color-bg-hover);
}

.nav-item.active {
  color: var(--color-primary-light);
  background: var(--color-primary-glow);
}

.nav-item.active::before {
  content: '';
  position: absolute;
  left: 0;
  width: 3px;
  height: 20px;
  background: var(--color-primary);
  border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
}

.nav-group {
  margin-bottom: var(--space-2);
}

.nav-group-header {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  color: var(--color-text-muted);
  font-size: var(--text-xs);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  white-space: nowrap;
}

.nav-group-children {
  padding-left: var(--space-10);
}

.nav-child {
  display: block;
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-sm);
  color: var(--color-text-secondary);
  font-size: var(--text-sm);
  transition: all var(--duration-fast) var(--ease-out);
  text-decoration: none;
  margin-bottom: 1px;
  white-space: nowrap;
  position: relative;
}

.nav-child:hover {
  color: var(--color-text-primary);
  background: var(--color-bg-hover);
}

.nav-child.active {
  color: var(--color-primary-light);
  background: var(--color-primary-glow);
}

.nav-child.active::before {
  content: '';
  position: absolute;
  left: -12px;
  top: 50%;
  transform: translateY(-50%);
  width: 3px;
  height: 16px;
  background: var(--color-primary);
  border-radius: var(--radius-sm);
}

/* ── Footer ── */
.sidebar-footer {
  padding: var(--space-4);
  border-top: 1px solid rgba(255, 255, 255, 0.04);
}

.collapse-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-2);
  background: none;
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: var(--radius-md);
  color: var(--color-text-muted);
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-out);
}

.collapse-btn:hover {
  color: var(--color-text-primary);
  border-color: rgba(255, 255, 255, 0.12);
  background: var(--color-bg-hover);
}

/* ── Main Content ── */
.main-content {
  flex: 1;
  margin-left: var(--sidebar-width);
  min-height: 100vh;
  transition: margin-left var(--duration-normal) var(--ease-out);
  background: var(--color-bg-deep);
}

.main-content.expanded {
  margin-left: var(--sidebar-collapsed);
}

/* ── Transitions ── */
.fade-enter-active,
.fade-leave-active {
  transition: opacity var(--duration-fast) var(--ease-out);
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.expand-enter-active,
.expand-leave-active {
  transition: all var(--duration-normal) var(--ease-out);
  overflow: hidden;
}

.expand-enter-from,
.expand-leave-to {
  opacity: 0;
  max-height: 0;
}

.expand-enter-to,
.expand-leave-from {
  opacity: 1;
  max-height: 300px;
}

.page-enter-active {
  animation: fadeInUp 0.4s var(--ease-out);
}

.page-leave-active {
  animation: fadeIn 0.15s var(--ease-out) reverse;
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(16px); }
  to   { opacity: 1; transform: translateY(0); }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to   { opacity: 1; }
}
</style>
