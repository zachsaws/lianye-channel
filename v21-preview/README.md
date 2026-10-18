# 联野 V2.1 独立预览

本机预览：http://127.0.0.1:8821/
审阅页：http://127.0.0.1:8821/review.html

新版本仅在v21-preview/。site/、site-preview/和v2-preview/保持原样。无外部部署或推送。

服务器停止时，在此目录运行：

```sh
python3 -m http.server 8821 --bind 127.0.0.1
```

静态HTML、CSS、JavaScript，无构建依赖。不要将localhost链接当公网分享链接。预览含预设演示和公开市场通路资料，不是真实AI执行或交易系统。

交付说明在docs/；原设计状态板与图像来源在design/；浏览器截图、录屏和检查记录在qa/。部分参考交互仍未完成直接核验，见QA报告。
