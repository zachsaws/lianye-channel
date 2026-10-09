# 研究资料导航

这里保留项目判断背后的证据和推导，供后续研究与迭代使用。公开渠道资料不代表已签约的合作网络；历史文件可能已被后续审查修正。

## 从这里开始

1. [经销商视角：差异化研究](strategy/经销商视角_差异化研究结论_v1.md)：对照成熟分销商，明确真正值得检验的 AI 增量。
2. [渠道目录](channels/channel-directory.csv)：当前官网展示主体、产品方向与来源链接，可直接筛选。
3. [当前来源映射](channels/source-map-current.json)：99 个展示主体的来源；219 为该轮研究记录口径，不能当作签约渠道数量。
4. [AI 产品与软件销售通路](strategy/AI产品范围与软件销售通路.md)：避免将项目边界收窄为硬件。
5. [渠道角色与权限](strategy/渠道经营角色与合作权限_归一审查_v30.md)：区分品牌、分销商、零售与场景采购的经营角色。

## 文件结构

- `channels/`：渠道主体、补充研究、覆盖检查、身份去重与证据审查。版本号代表研究轮次，不代表现行结论。`oct08` 文件为 2026-10-08 的专题研究。
- `strategy/`：项目差异化、AI 经验复用、分类与表达原则。

当前范围为国内渠道，海外扩展留待后续版本。此次未收录网页整页抓取、第三方报告全文、部署凭证及本地运行日志。来源链接保留在资料中，引用前应重新核对时效与原文。

## 2026-10-09 新一轮研究

[结论与下一阶段判断](next-stage-oct09/research-conclusions.md) · [24条分类候选](next-stage-oct09/channel-candidates.csv) · [历史长期目标草案](next-stage-oct09/long-term-goal-draft.md)

## 当前工作资料

[current/coverage-report.md](current/coverage-report.md)记录覆盖缺口；[current/channel-asset.json](current/channel-asset.json)区分已有展示主体和候选；[current/reviewed-profile-details.json](current/reviewed-profile-details.json)保留逐字段来源及未知项；[current/business-definition-v1.md](current/business-definition-v1.md)是待验证的业务定义。数据完整性检查不能代替商业验证。

## 判断原型与当前结论

[原型说明](prototype/README.md) · [规则基线](prototype/baseline-results.json) · [探索性AI审查](prototype/exploratory-review.md) · [合作交付v2](current/cooperation-deliverables-v2.md) · [经营字段深度审查](current/depth-audit.json)。当前仅有部分主体完成逐字段复核。早期探索性分析受到历史上下文影响；后续已完成五次隔离研究运行，仍没有等成本或真实业务效果证明，详见原型说明。

[当前阶段判断](current/interim-decision.md)汇总已支持结论、官网表达候选和未完成验证，作为后续决策入口。

[经营信息覆盖复查](current/operating-coverage-review.md)按六个产品方向检查有来源的字段，避免总量掩盖分类深度失衡。可通过 `python3 scripts/review_channel_depth.py` 更新；不代表合作网络或商业效果。

## 当前阶段审查入口

[决策与剩余证据](current/decision-review.md)连接渠道、业务、AI原型与本地预览，明确各阶段未完成内容。原公开官网未被本轮预览替换。

[完整工作独立测试](prototype/full-work-findings-v1.md)与[一页交付样稿](../generated-md/新品渠道开拓_一页交付样稿.md)是最新表达研究；不将被否定的反馈到行动预览当作现行方向。

## 最新收敛与反例

- [当前阶段状态](current/stage-status.json)：核心方向尚未获认可，目标仍进行中。
- [AI合作产品对照](current/ai-partnership-products-review.md)：具体工作、系统权限与真实网络依赖。
- [成熟分销反例及交付检验](current/distribution-counterexample-and-delivery-test.md)：不能把AI建议和自动化当独有差异。
- [三类合作提案样稿](../generated-md/会议Agent_三类渠道合作提案样稿.md)：实际草稿与版本修订；产品准备不足限制了成果。
- [内容电商角色边界](current/content-commerce-boundary-review.md)：购买运营服务不等于渠道采购商品。
- [权限规则原型](prototype/proposal-permissions-findings-v1.md)：可运行、确定性规则，非AI效果实验。

## 最新业务说明

[业务定义v3](current/business-definition-v3.md)按客户交来的事和拟交回成果重写，分开近期服务、有限AI证据和长期复用假设。尚未获用户认可，不替换官网。
