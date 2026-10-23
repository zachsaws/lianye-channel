# 联野 V2 独立预览

本目录是完整、无构建依赖的静态网站，独立于生产site/与原site-preview/。当前处于首批合作验证阶段；不包含实际交易、合作背书或成熟AI能力声明。

## 查看

当前本机预览：http://127.0.0.1:8818/ ；全部交付材料：http://127.0.0.1:8818/review.html 。仅本机可访问，不是外部发布链接。预览服务关闭、电脑休眠或重启后需要重新启动。

在本目录启动：

```sh
python3 -m http.server 8818 --bind 127.0.0.1
```

也可双击index.html离线浏览；浏览器可能限制本机剪贴板，页面会提供手动复制提示。

## 交付
- index.html / style.css / app.js / assets/：实际官网。
- design/direction-a.png、direction-b.png：两套原创高保真方向。
- design/storyboard-desktop.png、storyboard-mobile.png：开发前故事板。
- design/design-system.md：色彩、字体、版式、响应式和动效规范。
- design/narrative.md：叙事概要、事实边界和研究来源。
- design/selection.md：视觉选择与自审理由。
- design/image-prompts.md：内置image_gen提示词与素材来源。
- qa/full-1440.png、full-390.png：浏览器全站截图。
- qa/report.md：QA、自审与已知限制。

未更改生产站，未推送或部署。不得把研究条目当合作网络、把设计演示当实际产品能力，正式替换仍需用户最终授权。
