# V4.1 独立线上预览

2026-10-22 已发布，部署状态 succeeded。

- 在线地址：https://lianye-v41-preview.zachsaw.chatgpt.site
- 访问：所有者私有，需使用所有者账号访问。
- 源码：https://github.com/zachsaws/lianye-channel/tree/preview/design-v4-20261022/v4-preview
- GitHub 发布导出分支：gh-pages，仅含网页文件，不包含研究文档、QA和设计文件。
- GitHub Pages 创建返回 422：当前套餐不支持此私有仓库开通 Pages。因此 gh-pages 目前只是网页文件的备份分支，没有 GitHub Pages 在线站点。没有把仓库改为公开。
- 实际发布：通过 Sites 的独立站点完成，未改原正式站。
- Sites project_id：appgprj_6ada1e2b77f08191bc7262c1a70d1b28
- version_id：appgprj_6ada1e2b77f08191bc7262c1a70d1b28~appgver_97f894afe980819187a7db60926827f6
- deployment_id：appgdep_6ada2074097c8191bdc7be2b999a7240
- 托管源码提交：41cc0803b96eae36f37b9482401d4fd5b6946bda

## 后续更新

网站源文件继续维护在 v4-preview/。托管项目单独位于本机相邻目录 lianye-v41-hosted-preview-20261022，其 .openai/hosting.json 已保存站点 ID。

发布时只同步 index.html、style.css、app.js、scene.js、assets/、data/、vendor/ 到托管项目 dist/。保留托管身份和原访问权限，使用官方源仓库及打包流程保存、部署。不要复制仓库历史、研究文件或凭据进 dist/。修改不会自动上线，后续发布需遵循用户当轮授权。

原生产 site/、site-preview/、旧预览和 https://lianye-channel.zachsaw.chatgpt.site/ 均保留。
