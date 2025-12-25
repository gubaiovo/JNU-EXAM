// docs/.vitepress/theme/index.ts
import { watch } from 'vue'
import DefaultTheme from 'vitepress/theme'
// 引入新的 scss 入口文件（注意这里不再引入 custom.css 了，因为我们用 index.scss 替代了）
import './style/index.scss' 

let homePageStyle: HTMLStyleElement | undefined

export default {
  extends: DefaultTheme,
  enhanceApp({ router }) {
    // 确保在浏览器环境下运行
    if (typeof window !== 'undefined') {
      watch(
        () => router.route.data.relativePath,
        () => updateHomePageStyle(location.pathname === '/'), 
        { immediate: true }
      )
    }
  },
}

// 彩虹背景动画样式注入函数
function updateHomePageStyle(value: boolean) {
  if (value) {
    if (homePageStyle) return
    homePageStyle = document.createElement('style')
    // 这里使用了 rainbow.scss 中定义的 'rainbow' 关键帧
    homePageStyle.innerHTML = `
    :root {
      animation: rainbow 12s linear infinite;
    }`
    document.body.appendChild(homePageStyle)
  } else {
    if (!homePageStyle) return
    homePageStyle.remove()
    homePageStyle = undefined
  }
}