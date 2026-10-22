# 联野 V4.2｜四段主线

完整独立预览，不覆盖生产或旧版本。用户认可 V4 的改进，仍认为有提升空间。技术自审已执行，最终审美接受尚未确认。

在线预览：[https://zachsaws.github.io/lianye-channel/](https://zachsaws.github.io/lianye-channel/)（公开访问，无需登录）。原正式官网未替换。

仓库已按用户最新授权改为公有。先前的 Sites 私有预览保留作备份；发布配置见 [DEPLOYMENT.md](DEPLOYMENT.md)。

源代码分支：[`preview/design-v4-20261022`](https://github.com/zachsaws/lianye-channel/tree/preview/design-v4-20261022/v4-preview)。

最新页面结构与验证范围见 [页面结构与验收](docs/页面结构与验收.md)。最新截图和检查在 `qa/clarity/`；V4.1 与原 V4 资料保留为历史记录。

启动：
```sh
python3 -m http.server 8824 --bind 127.0.0.1 --directory v4-preview
```

- 网站：http://127.0.0.1:8824/
- 截图、录屏与说明：http://127.0.0.1:8824/review.html
- 入口：index.html、style.css、app.js、scene.js。
- 依赖：本地固定 Three.js 0.180.0，许可证在 vendor/；不需构建或在线 CDN。
- assets/：四幅原创场景渲染与合作提纲。渲染中的产品与场景均为示意。
- design/：两套原创高保真探索、方向取舍、实施前故事板与生成提示词。
- docs/：设计规范、叙事、诊断取舍、QA和能力边界。
- data/：继承的240条公开市场参考、26个二级经营分类。资料未在本轮逐项重新核验。
- qa/clarity/：当前 V4.2 的1440与390截图、三条路径、展开目录、全站长图与检查记录。其他 qa/ 资料和录像保留作历史对照。

首屏使用实时三维几何而非背景图漂移：样机、按钮、手部、响应表情、资料纸张均为独立对象。其他场景使用静态原创渲染，叠加对焦、快门、试用时间线和记录等预设事件；不是整站人物动画，也不是实际AI或交易系统。

生产site/、site-preview/及V2/V2.1/V2.2/V3均保留；本轮未发布正式官网。
