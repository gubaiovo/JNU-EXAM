<script setup lang="ts">
import DefaultTheme from 'vitepress/theme'
import { useData } from 'vitepress'
import { nextTick, provide } from 'vue'

const { isDark } = useData()

// 判断浏览器是否支持 View Transition API
const enableTransitions = () =>
  'startViewTransition' in document &&
  window.matchMedia('(prefers-reduced-motion: no-preference)').matches

// 核心逻辑：拦截默认的切换行为
provide('toggle-appearance', async ({ clientX: x, clientY: y }: MouseEvent) => {
  if (!enableTransitions()) {
    isDark.value = !isDark.value
    return
  }

  const clipPath = [
    `circle(0px at ${x}px ${y}px)`,
    `circle(${Math.hypot(
      Math.max(x, innerWidth - x),
      Math.max(y, innerHeight - y)
    )}px at ${x}px ${y}px)`
  ]

  // @ts-ignore: View Transitions API 是新特性，TS 可能报错，忽略即可
  await document.startViewTransition(async () => {
    isDark.value = !isDark.value
    await nextTick()
  }).ready

  document.documentElement.animate(
    { clipPath: isDark.value ? clipPath.reverse() : clipPath },
    {
      duration: 300,
      easing: 'ease-in',
      pseudoElement: `::view-transition-${isDark.value ? 'old' : 'new'}(root)`
    }
  )
})
</script>

<template>
  <DefaultTheme.Layout>
    </DefaultTheme.Layout>
</template>

<style>
/* 确保旧视图和新视图都不执行浏览器默认的淡入淡出动画 */
::view-transition-old(root),
::view-transition-new(root) {
  animation: none; 
  mix-blend-mode: normal; /* 关键：防止混合模式导致的颜色异常 */
}

/* 这里的 z-index 保证了新旧视图的层级关系 */
::view-transition-old(root),
.dark::view-transition-new(root) {
  z-index: 1;
}

::view-transition-new(root),
.dark::view-transition-old(root) {
  z-index: 9999;
}

.VPSwitchAppearance .check {
  transform: none !important;
}
.VPSwitchAppearance .check .icon {
  top: -2px;
}
</style>