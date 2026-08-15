# Payments Logic

本文档基于当前后端代码整理每日 payment 的计算逻辑，主要对应 [`y5-backend-flask/blueprints/payment.py`](/Users/codingchan/Documents/work/src/ysj/ysj_5/y5-backend-flask/blueprints/payment.py) 和 [`y5-backend-flask/app.py`](/Users/codingchan/Documents/work/src/ysj/ysj_5/y5-backend-flask/app.py) 中 night mail / summary mail 的调用方式。

## 入口

- 核心计算函数是 `calculate_func(room_id, date_start, date_end)`。
- night mail 在生成每个房间的邮件内容时调用：
  - `date_start = room.activated_at`
  - `date_end = datetime.datetime.now()`
- 也就是说，night mail 中展示的 payment 是“从房间激活时间开始，到当前执行时刻为止”的累计奖励，不是只看当天。

## 统计范围

`calculate_data()` 会先在 SQL 层统计指定房间、指定时间窗口内的每日活跃数据。

统计对象有以下限制：

- 只统计指定 `room_id`。
- 只统计 `tb_room_member` 中 `activated = 1` 的成员。
- 只统计 `tb_post_public.is_system_post != 1` 的非系统帖。
- 时间范围使用原始 `created_at`：
  - `created_at >= date_start`
  - `created_at < date_end`

## 每日统计字段

SQL 最终会按 `room_id + 日期 + user_id` 聚合出以下字段：

- `post_count`
  - 原始定义是用户当天在 `tb_post_public` 中的发帖总数减去分享帖数量。
  - 也就是“原创 public post 数”。
- `share_post_count`
  - 用户当天 `post_shared_id is not null` 的 public post 数量。
- `comment_count`
  - 用户当天对该房间 public post 发表的评论数。
- `total_count`
  - 代码中的总活跃数，计算方式是：
  - `原创帖数 + 分享帖数 + 评论数`
  - 在 SQL 里等价于：
  - `COUNT(public posts) + COUNT(comments)`
  - 如果用户当天只有评论、没有发帖，也会单独补一条记录，确保该用户仍然进入统计。

## 每日奖励规则

`calculate_func()` 会先把 SQL 结果整理成：

- `formatted_data[room_id][date] = [user stats ...]`

然后按“房间 -> 日期”逐天计算奖励。

### 1. 基础奖励

如果用户当天满足以下任一条件，则获得 `$0.25`：

- `post_count > 0`
- 或 `comment_count > 0`
- 或 `share_count > 0`

换句话说，只要当天有有效参与行为，就有基础奖励。

### 2. 活跃度 bonus

系统先按当天的 `total_count` 从高到低排序。

当前代码不是“严格前两名”，而是：

- 找到排序后第 2 名的 `total_count`
- 把这个值记为 `reward_cutoff`
- 所有 `total_count >= reward_cutoff` 的用户，都额外获得 `$1.0`

因此当前实现的规则是：

- 只有 1 个活跃用户时，这个人拿 bonus。
- 有 2 个及以上活跃用户时，所有“并列前二分数线以上”的人都拿 bonus。
- 如果第 2 名和第 3 名并列，则两人都会拿 bonus。
- 如果多人并列第 1，且他们的分数都等于第 2 名分数线，则这些人都会拿 bonus。

### 3. 单个用户累计上限

`total_rewards[user_id]` 是该用户在当前时间窗口内的累计奖励。

代码会在每天累加时检查总额是否超过 `$10.0`：

- 如果未超过，则当天奖励全额计入。
- 如果超过，则只补足到 `$10.0`。
- 因此当前实现里，单个用户的累计互动奖励上限是 `$10`。

## 返回结果结构

`calculate_func()` 返回：

```python
{
    "reward_summary": {
        "YYYY-MM-DD": [
            {
                "user_id": ...,
                "post_count": ...,
                "share_count": ...,
                "comment_count": ...,
                "total_count": ...,
                "daily_reward": ...,
                "is_top_two": ...
            }
        ]
    },
    "total_rewards": {
        user_id: reward
    }
}
```

其中：

- `reward_summary` 是逐日明细。
- `total_rewards` 是每个用户在本次计算时间窗口内的累计奖励。

## 在邮件中的使用方式

### Night Mail

night mail 对每个房间执行：

1. `calculate_func(room.id, room.activated_at, now)`
2. 读取 `payments['total_rewards'][member.user_id]`
3. 将该值作为 `payment` 注入 night mail 模板

因此 night mail 中的 payment 代表：

- 该成员从房间激活开始，到 night mail 生成时为止的累计互动奖励
- 不包含 pre-survey / post-survey 的固定补偿
- night mail 会遍历 `RoomMember.query.filter_by(room_id=room.id).all()` 查出的全部成员发信；如果某成员不在 `payments['total_rewards']` 中，则模板里注入 `payment = 0`

### Post-Experiment Summary

`format_data_for_user()` 会把：

- `reward_summary`
- `total_rewards`
- `pre_survey_base`
- `post_survey_base`

组装成模板数据。

其中：

- `base` 字段当前写法是：`daily_reward > 0` 就显示 `0.25`
- `bonus` 字段当前写法是：`is_top_two` 就显示 `1`
- summary mail 在进入 `format_data_for_user()` 之前，会先判断 `member.user_id in payments['total_rewards']`
- 因此当前实现只会给“在当前统计窗口内至少拿到过一次奖励”的成员发送 summary mail；完全没有奖励记录的成员会被直接跳过

这意味着它是按当前代码结构来展示 daily breakdown，不是重新独立计算。

## 当前代码语义上的注意点

- `total_count` 虽然叫 total count，但本质是“原创帖 + 分享帖 + 评论”的总活跃度。
- `post_count` 不包含分享帖；分享帖单独记在 `share_count`。
- payment 统计已经排除了系统帖，也只统计已激活成员。
- night mail 读到的是累计奖励，不是“当日新增奖励”。
- summary mail 和 night mail 都是按“从激活时刻到当前时刻”的累计窗口取数，不是按自然日结算。
- `format_data_for_user()` 展示 `base`/`bonus` 时，不会因为 `$10` 封顶而重新拆分金额：
  - 只要该日 `daily_reward > 0`，就展示 `base = 0.25`
  - 只要该日 `is_top_two = True`，就展示 `bonus = 1`
  - 但 `total` 仍然使用封顶后的实际 `daily_reward`
  - 所以在接近或达到 `$10` 上限时，页面上的 `base + bonus` 视觉含义可能与 `total` 不完全一致
