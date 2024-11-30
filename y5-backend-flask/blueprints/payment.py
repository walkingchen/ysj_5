from collections import defaultdict
from datetime import datetime, timedelta

from flask import Blueprint, request, jsonify, render_template
from flask_restful import Api
from sqlalchemy import text

from extensions import db

bp_payment = Blueprint('api/payment', __name__, url_prefix='/api/payment')
# api = Api(bp_payment, '/api/payment')


def calculate_data_by_user(room_id, user_id, date_start, date_end):
    query = text('''
        SELECT mc.room_id, mc.date, mc.total_count, mc.post_count, mc.comment_count, mc.share_post_count
        FROM (
            SELECT
                pc.room_id,
                pc.date,
                pc.user_id,
                ((pc.post_count - pc.share_post_count) + COALESCE(cc.comment_count, 0)) AS total_count,  -- 更新total_count的计算
                (pc.post_count - pc.share_post_count) AS post_count,  -- 使用post_count - share_post_count
                COALESCE(cc.comment_count, 0) AS comment_count,
                pc.share_post_count
            FROM (
                SELECT
                    pp.room_id,
                    DATE(pp.created_at) AS date,
                    pp.user_id,
                    COUNT(pp.id) AS post_count,
                    COUNT(pp.post_shared_id) AS share_post_count  -- 使用正确的字段名 post_shared_id
                FROM tb_post_public pp
                WHERE pp.room_id = :room_id
                GROUP BY pp.room_id, DATE(pp.created_at), pp.user_id
            ) AS pc
            LEFT JOIN (
                SELECT
                    pp.room_id,
                    DATE(pc.created_at) AS date,
                    pc.user_id,
                    COUNT(pc.id) AS comment_count
                FROM tb_post_comment pc
                JOIN tb_post_public pp ON pc.post_id = pp.id
                WHERE pp.room_id = :room_id
                GROUP BY pp.room_id, DATE(pc.created_at), pc.user_id
            ) AS cc
            ON pc.room_id = cc.room_id
            AND pc.date = cc.date
            AND pc.user_id = cc.user_id
        
            UNION ALL
        
            SELECT
                cc.room_id,
                cc.date,
                cc.user_id,
                cc.comment_count AS total_count,
                0 AS post_count,
                cc.comment_count,
                0 AS share_post_count  -- 没有post的情况，设置分享数为0
            FROM (
                SELECT
                    pp.room_id,
                    DATE(pc.created_at) AS date,
                    pc.user_id,
                    COUNT(pc.id) AS comment_count
                FROM tb_post_comment pc
                JOIN tb_post_public pp ON pc.post_id = pp.id
                WHERE pp.room_id = :room_id
                GROUP BY pp.room_id, DATE(pc.created_at), pc.user_id
            ) AS cc
            LEFT JOIN (
                SELECT
                    pp.room_id,
                    DATE(pp.created_at) AS date,
                    pp.user_id,
                    COUNT(pp.id) AS post_count
                FROM tb_post_public pp
                WHERE pp.room_id = :room_id
                GROUP BY pp.room_id, DATE(pp.created_at), pp.user_id
            ) AS pc
            ON cc.room_id = pc.room_id
            AND cc.date = pc.date
            AND cc.user_id = pc.user_id
            WHERE pc.user_id IS NULL
        ) AS mc
        WHERE mc.date >= :date_start AND mc.date < :date_end AND mc.user_id = :user_id
        ORDER BY mc.room_id, mc.date, mc.total_count DESC;
    ''')

    # 执行 SQL 查询
    results = db.session.execute(query, {'room_id': room_id, 'date_start': date_start, 'date_end': date_end}).fetchall()

    return results

def calculate_data(room_id, date_start, date_end):
    # 定义 SQL 查询语句
    query = text("""
        SELECT mc.room_id, mc.date, mc.user_id, mc.total_count, mc.post_count, mc.comment_count
        FROM (
            SELECT
                pc.room_id,
                pc.date,
                pc.user_id,
                (pc.post_count + COALESCE(cc.comment_count, 0)) AS total_count,
                pc.post_count,
                COALESCE(cc.comment_count, 0) AS comment_count
            FROM (
                SELECT 
                    pp.room_id,
                    DATE(pp.created_at) AS date,
                    pp.user_id,
                    COUNT(pp.id) AS post_count
                FROM tb_post_public pp
                WHERE pp.room_id = :room_id
                GROUP BY pp.room_id, DATE(pp.created_at), pp.user_id
            ) AS pc
            LEFT JOIN (
                SELECT 
                    pp.room_id,
                    DATE(pc.created_at) AS date,
                    pc.user_id,
                    COUNT(pc.id) AS comment_count
                FROM tb_post_comment pc
                JOIN tb_post_public pp ON pc.post_id = pp.id
                WHERE pp.room_id = :room_id
                GROUP BY pp.room_id, DATE(pc.created_at), pc.user_id
            ) AS cc
            ON pc.room_id = cc.room_id 
            AND pc.date = cc.date 
            AND pc.user_id = cc.user_id

            UNION ALL

            SELECT
                cc.room_id,
                cc.date,
                cc.user_id,
                cc.comment_count AS total_count,
                0 AS post_count,
                cc.comment_count
            FROM (
                SELECT 
                    pp.room_id,
                    DATE(pc.created_at) AS date,
                    pc.user_id,
                    COUNT(pc.id) AS comment_count
                FROM tb_post_comment pc
                JOIN tb_post_public pp ON pc.post_id = pp.id
                WHERE pp.room_id = :room_id
                GROUP BY pp.room_id, DATE(pc.created_at), pc.user_id
            ) AS cc
            LEFT JOIN (
                SELECT 
                    pp.room_id,
                    DATE(pp.created_at) AS date,
                    pp.user_id,
                    COUNT(pp.id) AS post_count
                FROM tb_post_public pp
                WHERE pp.room_id = :room_id
                GROUP BY pp.room_id, DATE(pp.created_at), pp.user_id
            ) AS pc
            ON cc.room_id = pc.room_id 
            AND cc.date = pc.date 
            AND cc.user_id = pc.user_id
            WHERE pc.user_id IS NULL
        ) AS mc
        WHERE mc.date >= :date_start AND mc.date < :date_end
        ORDER BY mc.room_id, mc.date, mc.total_count DESC;
    """)

    query = '''
    SELECT mc.room_id, mc.date, mc.user_id, mc.total_count, mc.post_count, mc.comment_count, mc.share_post_count
FROM (
    SELECT
        pc.room_id,
        pc.date,
        pc.user_id,
        ((pc.post_count - pc.share_post_count) + COALESCE(cc.comment_count, 0)) AS total_count,  -- 更新total_count的计算
        (pc.post_count - pc.share_post_count) AS post_count,  -- 使用post_count - share_post_count
        COALESCE(cc.comment_count, 0) AS comment_count,
        pc.share_post_count
    FROM (
        SELECT
            pp.room_id,
            DATE(pp.created_at) AS date,
            pp.user_id,
            COUNT(pp.id) AS post_count,
            COUNT(pp.post_shared_id) AS share_post_count  -- 使用正确的字段名 post_shared_id
        FROM tb_post_public pp
        WHERE pp.room_id = :room_id
        GROUP BY pp.room_id, DATE(pp.created_at), pp.user_id
    ) AS pc
    LEFT JOIN (
        SELECT
            pp.room_id,
            DATE(pc.created_at) AS date,
            pc.user_id,
            COUNT(pc.id) AS comment_count
        FROM tb_post_comment pc
        JOIN tb_post_public pp ON pc.post_id = pp.id
        WHERE pp.room_id = :room_id
        GROUP BY pp.room_id, DATE(pc.created_at), pc.user_id
    ) AS cc
    ON pc.room_id = cc.room_id
    AND pc.date = cc.date
    AND pc.user_id = cc.user_id

    UNION ALL

    SELECT
        cc.room_id,
        cc.date,
        cc.user_id,
        cc.comment_count AS total_count,
        0 AS post_count,
        cc.comment_count,
        0 AS share_post_count  -- 没有post的情况，设置分享数为0
    FROM (
        SELECT
            pp.room_id,
            DATE(pc.created_at) AS date,
            pc.user_id,
            COUNT(pc.id) AS comment_count
        FROM tb_post_comment pc
        JOIN tb_post_public pp ON pc.post_id = pp.id
        WHERE pp.room_id = :room_id
        GROUP BY pp.room_id, DATE(pc.created_at), pc.user_id
    ) AS cc
    LEFT JOIN (
        SELECT
            pp.room_id,
            DATE(pp.created_at) AS date,
            pp.user_id,
            COUNT(pp.id) AS post_count
        FROM tb_post_public pp
        WHERE pp.room_id = :room_id
        GROUP BY pp.room_id, DATE(pp.created_at), pp.user_id
    ) AS pc
    ON cc.room_id = pc.room_id
    AND cc.date = pc.date
    AND cc.user_id = pc.user_id
    WHERE pc.user_id IS NULL
) AS mc
WHERE mc.date >= :date_start AND mc.date < :date_end
ORDER BY mc.room_id, mc.date, mc.total_count DESC;
    '''

    # 执行 SQL 查询
    results = db.session.execute(query, {'room_id': room_id, 'date_start': date_start, 'date_end': date_end}).fetchall()

    return results


def calculate_func(room_id, date_start, date_end):
    # 计算每日post/comment等数据（调用计算函数或直接编写在此）
    results = calculate_data(room_id, date_start, date_end)  # 假设此函数返回符合要求的奖励数据

    # 处理查询结果，将其格式化为层次结构
    formatted_data = defaultdict(lambda: defaultdict(list))
    for row in results:
        formatted_data[row.room_id][row.date.strftime('%Y-%m-%d')].append({
            'user_id': row.user_id,
            'total_count': row.total_count,
            'post_count': row.post_count,
            'comment_count': row.comment_count,
            'share_count': row.share_post_count
        })

    # 初始化奖励计算
    rewards = defaultdict(float)
    reward_summary = defaultdict(list)  # 存储每日的奖励数据
    total_rewards = defaultdict(float)  # 成员奖励总数

    for room, dates in formatted_data.items():
        for date, users in dates.items():
            # 排序用户，找出最活跃的前两位
            sorted_users = sorted(users, key=lambda x: x['total_count'], reverse=True)
            top_two_users = sorted_users[:2]

            for user in users:
                user_id = user['user_id']
                daily_reward = 0.0

                # 奖励规则：至少一篇帖子、评论或分享
                if user['post_count'] > 0 or user['comment_count'] > 0 or user['share_count'] > 0:
                    daily_reward += 0.25

                # 检查用户是否为最活跃的前两名
                is_top_two = user in top_two_users
                if is_top_two:
                    daily_reward += 1.0

                # 累加用户总奖励并确保不超过 $10
                new_total = total_rewards[user_id] + daily_reward
                if new_total > 10.0:
                    daily_reward = max(0, 10.0 - total_rewards[user_id])  # 仅添加到 $10 的剩余额度

                # 更新 total_rewards 和 daily_reward 仅在限额范围内的数值
                total_rewards[user_id] += daily_reward

                # 存储每日数据到 reward_summary
                reward_summary[date].append({
                    'user_id': user_id,
                    'post_count': user['post_count'],
                    'share_count': user['share_count'],
                    'comment_count': user['comment_count'],
                    'total_count': user['total_count'],
                    'daily_reward': daily_reward,
                    'is_top_two': is_top_two
                })

    formatted_reward_summary = {date: users for date, users in reward_summary.items()}
    formatted_total_rewards = {user_id: reward for user_id, reward in total_rewards.items()}

    return {
        'reward_summary': formatted_reward_summary,
        'total_rewards': formatted_total_rewards
    }


@bp_payment.route('/calculate_rewards', methods=['GET'])
def calculate_rewards():
    data = request.args

    # 获取请求参数
    room_id = data.get('room_id', type=int)
    date_start_str = data.get('start_date')  # 假设日期格式为 YYYY-MM-DD
    date_end_str = data.get('end_date')  # 假设日期格式为 YYYY-MM-DD
    date_start = datetime.strptime(date_start_str, '%Y-%m-%d')
    date_end = datetime.strptime(date_end_str, '%Y-%m-%d')

    return jsonify(calculate_func(room_id, date_start, date_end))


@bp_payment.route('/rewards_summary')
def rewards_summary():
    return render_template('rewards.html')