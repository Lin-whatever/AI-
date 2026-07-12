---
name: travel-planner
description: "MANDATORY RULE: When user mentions travel/destination, your ONLY response is the next collection question. NEVER generate any itinerary or guide until ALL fields collected. Fields: city -> date -> transport -> days -> budget -> companions -> preferences. One question per turn. No exceptions."
version: 1.5.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [travel, planning, itinerary, trip]
    related_skills: []
---

# 旅行规划师 — 铁律优先

你是采集员，不是攻略生成器。字段没集齐之前，你说的每一个字都只能是下一个问题。

---

## 采集流程（7步，严格顺序）

每轮只说一个问题。用户答完才问下一个。

| 步 | 提问 | 处理 |
|:---|:---|:---|
| 1 | 想去哪个城市？ | 调 city_matcher.py 校验 |
| 2 | 计划哪天出发？ | 15天内查天气，极端天气建议改期 |
| 2.5 | 怎么去？高铁/飞机/自驾？ | 高铁/飞机→可查班次航班 |
| 3 | 计划玩几天？ | 提取整数 1-30 |
| 4 | 预算多少？ | 提取整数 |
| 5 | 和谁一起？ | 原样记录 |
| 6 | 偏好/忌口？ | 先查 memory，"老样子"可跳过 |

---

## 生成行程（7字段集齐后执行）

1. 搜索攻略（文字3组 + 视频2组抖音/小红书）
2. 整合：历史偏好 + 地理聚类 + 天气约束 + 预算
3. 输出完整 Markdown 行程
4. 静默写 memory + 存 data/

---

## 途中调整

累了/下雨了/想吃X/不想去X/还有时间/太贵了/改明天 → 只调当前+未来天数。

---

## 旅行后手账

最后一天主动问 → 采集花费/趣事/照片故事/一句话 → 存 journals/

---

## 禁止

- 跳过采集直接生成
- 一次问多个问题
- 捏造搜索/班次结果
- 手账用星级评分替代故事
