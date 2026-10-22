# V4.2 独立线上预览

## 当前入口：GitHub Pages

2026-10-22 用户明确授权将仓库改为公有并开通 GitHub Pages。

- 地址：https://zachsaws.github.io/lianye-channel/
- 仓库：https://github.com/zachsaws/lianye-channel ，现为 public。
- 发布来源：gh-pages 分支根目录，只含网页运行文件。
- V4.2 发布于 2026-10-23；当前发布提交：a1f0f514fb1a0dd87204bb80296526a51e30bcd7。
- 页面、样式、脚本与提纲已在线核对，均返回200且内容与源文件一致。
- V4.1 历史发布内容提交：e6dc9e924e7b95c924a2d68c6ae7c517720ef6b7。
- 访问：公开，无需登录。
- 原生产站继续保留，默认分支仍为 main。
- 更新时从 v4-preview/ 导出运行文件到 gh-pages，提交并推送后由 GitHub Pages 自动发布。当前 PR 的合并与正式官网替换仍未执行。

## 先前 Sites 私有备份与开通记录

以下记录的是仓库改为公有之前的部署与套餐限制；现在 GitHub Pages 已成功创建，原 422 限制不再适用于当前公有仓库。

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
