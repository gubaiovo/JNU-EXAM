import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "JNU-EXAM",
  description: "江南大学考试资料站",
    themeConfig: {
    logo: '/logo.png',
    nav: [
      // { text: '这是什么', link: './what' },
      // { text: '怎么使用', link: '/usage' },
      // {
      //   text: 'Dropdown Menu',
      //   items: [
      //     { text: 'Item A', link: '/item-1' },
      //     { text: 'Item B', link: '/item-2' },
      //     { text: 'Item C', link: '/item-3' },
      //   ],
      // },
      // ...
    ],

    sidebar: [
      {
        text: '关于 JNU-EXAM',
        items: [
          { text: '什么是 JNU-EXAM', link: '/about/what' },
          { text: '怎么用 JNU-EXAM', link: '/about/usage' },
          { text: '怎么为 JNU-EXAM 投稿', link: '/about/contribution' },
          { text: '常见问题', link: '/about/qa' },
          // ...
        ],
      },
      {
        text: '关于下载器',
        items: [
          { text: '什么是下载器', link: '/downloader/what' },
          { text: '怎么用下载器', link: '/downloader/usage' },
          { text: '常见问题', link: '/downloader/qa' },
        ],
      },
      {
        text: '对于开发者',
        items: [
          { text: '快速开始', link: '/developer/index' },
          { text: '搭建新的下载源', link: '/developer/build_own_source' },
        ],
      },
      {
        text: '其他',
        items: [
          { text: '公告', link: '/other/announcement' },
          { text: '开源协议', link: '/other/license' },
        ],
      }
    ],
  },
});
