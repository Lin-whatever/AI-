# Travel Search Query Templates

## 基础搜索
- {city} {days}日游 旅游攻略
- {city} 自由行攻略 {days}天
- {city} 必去景点 行程安排

## 深度搜索
- {city} 美食攻略 本地人推荐
- {city} 交通攻略 景点之间怎么走
- {city} 住宿推荐 {budget}元预算
- {city} 门票价格 2025 最新

## 避坑搜索
- {city} 旅游避坑 注意事项
- {city} 旅游骗局 防坑指南
- {city} 景点闭馆时间 开放时间

## 特定场景搜索
- {city} 带父母旅游攻略
- {city} 情侣旅游攻略
- {city} 独自旅行攻略
- {city} {companions} 旅游路线

## Usage in SKILL.md
The agent uses web_search with these templates, substituting {city}, {days}, {budget}, {companions} with collected values.
Search at least 2-3 different query types before generating the itinerary.
