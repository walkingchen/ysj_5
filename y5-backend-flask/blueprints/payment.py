from collections import defaultdict
from datetime import date, datetime, timedelta
from time import strptime

from flask import Blueprint, request, jsonify, render_template
from flask_restful import Api
from sqlalchemy import text

from extensions import db
from models import Room, RoomMember, Serializer

bp_payment = Blueprint('api/payment', __name__, url_prefix='/api/payment')
# api = Api(bp_payment, '/api/payment')


def parse_date_filter(value):
    if not value:
        return None
    return datetime.strptime(value, '%Y-%m-%d')


def parse_bool(value):
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).lower() in ('1', 'true', 'yes', 'on')


def filter_rooms_by_activated_at(query, start_date=None, end_date=None, include_inactive=False):
    if not include_inactive:
        query = query.filter_by(activated=1)

    if start_date:
        query = query.filter(Room.activated_at >= start_date)
    if end_date:
        query = query.filter(Room.activated_at < end_date + timedelta(days=1))

    return query


def get_rooms_by_activation_range(start_date_str=None, end_date_str=None, include_inactive=False):
    start_date = parse_date_filter(start_date_str)
    end_date = parse_date_filter(end_date_str)

    if start_date and end_date and start_date > end_date:
        raise ValueError('activation start date is after end date')

    rooms_query = Room.query
    rooms_query = filter_rooms_by_activated_at(
        rooms_query,
        start_date,
        end_date,
        include_inactive
    )
    return rooms_query.order_by(Room.activated_at, Room.id).all(), start_date, end_date


def room_matches_activation_range(room, start_date=None, end_date=None, include_inactive=False):
    if not include_inactive and room.activated != 1:
        return False
    if (start_date or end_date) and room.activated_at is None:
        return False

    activated_date = room.activated_at.date() if room.activated_at else None
    if start_date and activated_date < start_date.date():
        return False
    if end_date and activated_date > end_date.date():
        return False
    return True


def build_room_reward_preview(room, date_end=None):
    if room.activated_at is None:
        return {
            'room_id': room.id,
            'room_code': room.room_id,
            'room_name': room.room_name,
            'activated': room.activated,
            'activated_at': None,
            'member_count': RoomMember.query.filter_by(room_id=room.id).count(),
            'payable_user_count': 0,
            'total_reward': 0,
            'status': 'missing activated_at'
        }

    date_end = date_end or datetime.now()
    rewards = calculate_func(room.id, room.activated_at, date_end)
    total_rewards = rewards['total_rewards']

    return {
        'room_id': room.id,
        'room_code': room.room_id,
        'room_name': room.room_name,
        'activated': room.activated,
        'activated_at': room.activated_at.isoformat(),
        'member_count': RoomMember.query.filter_by(room_id=room.id).count(),
        'payable_user_count': len(total_rewards),
        'total_reward': round(sum(total_rewards.values()), 2),
        'status': 'ready'
    }


def calculate_data_by_user(room_id, user_id, date_start, date_end):
    query = text('''
        SELECT mc.room_id, mc.date, mc.total_count, mc.post_count, mc.comment_count, mc.share_post_count
        FROM (
            SELECT
                pc.room_id,
                pc.date,
                pc.user_id,
                (pc.post_count + pc.share_post_count + COALESCE(cc.comment_count, 0)) AS total_count,  -- total = 原创帖 + 分享帖 + 评论
                pc.post_count,
                COALESCE(cc.comment_count, 0) AS comment_count,
                pc.share_post_count
            FROM (
                SELECT
                    pp.room_id,
                    DATE(pp.created_at) AS date,
                    pp.user_id,
                    CAST(SUM(CASE
                        WHEN pp.post_shared_id IS NULL AND COALESCE(pp.is_system_post, 0) != 1 THEN 1
                        ELSE 0
                    END) AS SIGNED) AS post_count,
                    CAST(SUM(CASE WHEN pp.post_shared_id IS NOT NULL THEN 1 ELSE 0 END) AS SIGNED) AS share_post_count  -- 分享帖不排除对 system post 的分享
                FROM tb_post_public pp
                JOIN tb_room_member rm
                    ON rm.room_id = pp.room_id
                    AND rm.user_id = pp.user_id
                    AND rm.activated = 1
                WHERE pp.room_id = :room_id
                    AND (
                        pp.post_shared_id IS NOT NULL
                        OR COALESCE(pp.is_system_post, 0) != 1
                    )
                    AND pp.created_at >= :date_start
                    AND pp.created_at < :date_end
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
                JOIN tb_room_member rm
                    ON rm.room_id = pp.room_id
                    AND rm.user_id = pc.user_id
                    AND rm.activated = 1
                WHERE pp.room_id = :room_id
                    AND pc.created_at >= :date_start
                    AND pc.created_at < :date_end
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
                cc.comment_count AS total_count,  -- 只有评论的情况，total = comment
                0 AS post_count,  -- 没有原创帖子
                cc.comment_count,
                0 AS share_post_count  -- 没有分享帖
            FROM (
                SELECT
                    pp.room_id,
                    DATE(pc.created_at) AS date,
                    pc.user_id,
                    COUNT(pc.id) AS comment_count
                FROM tb_post_comment pc
                JOIN tb_post_public pp ON pc.post_id = pp.id
                JOIN tb_room_member rm
                    ON rm.room_id = pp.room_id
                    AND rm.user_id = pc.user_id
                    AND rm.activated = 1
                WHERE pp.room_id = :room_id
                    AND pc.created_at >= :date_start
                    AND pc.created_at < :date_end
                GROUP BY pp.room_id, DATE(pc.created_at), pc.user_id
            ) AS cc
            LEFT JOIN (
                SELECT
                    pp.room_id,
                    DATE(pp.created_at) AS date,
                    pp.user_id,
                    CAST(SUM(CASE
                        WHEN pp.post_shared_id IS NULL AND COALESCE(pp.is_system_post, 0) != 1 THEN 1
                        ELSE 0
                    END) AS SIGNED) AS post_count,
                    CAST(SUM(CASE WHEN pp.post_shared_id IS NOT NULL THEN 1 ELSE 0 END) AS SIGNED) AS share_post_count
                FROM tb_post_public pp
                JOIN tb_room_member rm
                    ON rm.room_id = pp.room_id
                    AND rm.user_id = pp.user_id
                    AND rm.activated = 1
                WHERE pp.room_id = :room_id
                    AND (
                        pp.post_shared_id IS NOT NULL
                        OR COALESCE(pp.is_system_post, 0) != 1
                    )
                    AND pp.created_at >= :date_start
                    AND pp.created_at < :date_end
                GROUP BY pp.room_id, DATE(pp.created_at), pp.user_id
            ) AS pc
            ON cc.room_id = pc.room_id
            AND cc.date = pc.date
            AND cc.user_id = pc.user_id
            WHERE pc.user_id IS NULL
        ) AS mc
        WHERE mc.user_id = :user_id
        ORDER BY mc.room_id, mc.date, mc.total_count DESC;
    ''')

    # 执行 SQL 查询
    results = db.session.execute(
        query,
        {
            'room_id': room_id,
            'user_id': user_id,
            'date_start': date_start,
            'date_end': date_end,
        }
    ).fetchall()

    return results

def calculate_data(room_id, date_start, date_end):
    # 定义 SQL 查询语句
    query = text('''
    SELECT mc.room_id, mc.date, mc.user_id, mc.total_count, mc.post_count, mc.comment_count, mc.share_post_count
FROM (
    SELECT
        pc.room_id,
        pc.date,
        pc.user_id,
        (pc.post_count + pc.share_post_count + COALESCE(cc.comment_count, 0)) AS total_count,  -- total = 原创帖 + 分享帖 + 评论
        pc.post_count,
        COALESCE(cc.comment_count, 0) AS comment_count,
        pc.share_post_count
    FROM (
        SELECT
            pp.room_id,
            DATE(pp.created_at) AS date,
            pp.user_id,
            CAST(SUM(CASE
                WHEN pp.post_shared_id IS NULL AND COALESCE(pp.is_system_post, 0) != 1 THEN 1
                ELSE 0
            END) AS SIGNED) AS post_count,
            CAST(SUM(CASE WHEN pp.post_shared_id IS NOT NULL THEN 1 ELSE 0 END) AS SIGNED) AS share_post_count  -- 分享帖不排除对 system post 的分享
        FROM tb_post_public pp
        JOIN tb_room_member rm
            ON rm.room_id = pp.room_id
            AND rm.user_id = pp.user_id
            AND rm.activated = 1
        WHERE pp.room_id = :room_id
            AND (
                pp.post_shared_id IS NOT NULL
                OR COALESCE(pp.is_system_post, 0) != 1
            )
            AND pp.created_at >= :date_start
            AND pp.created_at < :date_end
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
        JOIN tb_room_member rm
            ON rm.room_id = pp.room_id
            AND rm.user_id = pc.user_id
            AND rm.activated = 1
        WHERE pp.room_id = :room_id
            AND pc.created_at >= :date_start
            AND pc.created_at < :date_end
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
        cc.comment_count AS total_count,  -- 只有评论的情况，total = comment
        0 AS post_count,  -- 没有原创帖子
        cc.comment_count,
        0 AS share_post_count  -- 没有分享帖
    FROM (
        SELECT
            pp.room_id,
            DATE(pc.created_at) AS date,
            pc.user_id,
            COUNT(pc.id) AS comment_count
        FROM tb_post_comment pc
        JOIN tb_post_public pp ON pc.post_id = pp.id
        JOIN tb_room_member rm
            ON rm.room_id = pp.room_id
            AND rm.user_id = pc.user_id
            AND rm.activated = 1
        WHERE pp.room_id = :room_id
            AND pc.created_at >= :date_start
            AND pc.created_at < :date_end
        GROUP BY pp.room_id, DATE(pc.created_at), pc.user_id
    ) AS cc
    LEFT JOIN (
        SELECT
            pp.room_id,
            DATE(pp.created_at) AS date,
            pp.user_id,
            CAST(SUM(CASE
                WHEN pp.post_shared_id IS NULL AND COALESCE(pp.is_system_post, 0) != 1 THEN 1
                ELSE 0
            END) AS SIGNED) AS post_count,
            CAST(SUM(CASE WHEN pp.post_shared_id IS NOT NULL THEN 1 ELSE 0 END) AS SIGNED) AS share_post_count
        FROM tb_post_public pp
        JOIN tb_room_member rm
            ON rm.room_id = pp.room_id
            AND rm.user_id = pp.user_id
            AND rm.activated = 1
        WHERE pp.room_id = :room_id
            AND (
                pp.post_shared_id IS NOT NULL
                OR COALESCE(pp.is_system_post, 0) != 1
            )
            AND pp.created_at >= :date_start
            AND pp.created_at < :date_end
        GROUP BY pp.room_id, DATE(pp.created_at), pp.user_id
    ) AS pc
    ON cc.room_id = pc.room_id
    AND cc.date = pc.date
    AND cc.user_id = pc.user_id
    WHERE pc.user_id IS NULL
) AS mc
ORDER BY mc.room_id, mc.date, mc.total_count DESC;
    ''')

    # 执行 SQL 查询
    results = db.session.execute(query, {'room_id': room_id, 'date_start': date_start, 'date_end': date_end}).fetchall()

    return results


def calculate_func(room_id, date_start, date_end):
    if isinstance(date_start, datetime):
        date_start = date_start.replace(microsecond=0)
    elif isinstance(date_start, date):
        date_start = datetime.combine(date_start, datetime.min.time())

    if isinstance(date_end, datetime):
        date_end = date_end.replace(microsecond=0)
    elif isinstance(date_end, date):
        date_end = datetime.combine(date_end, datetime.min.time())

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
            if not sorted_users:
                continue

            second_place_index = min(1, len(sorted_users) - 1)
            reward_cutoff = sorted_users[second_place_index]['total_count']

            for user in users:
                user_id = user['user_id']
                daily_reward = 0.0

                # 奖励规则：至少一篇帖子、评论或分享
                if user['post_count'] > 0 or user['comment_count'] > 0 or user['share_count'] > 0:
                    daily_reward += 0.25

                # 检查用户是否为最活跃的前两名
                is_top_two = user['total_count'] >= reward_cutoff
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
    date_start = strptime(date_start_str, '%Y-%m-%d')
    date_end = strptime(date_end_str, '%Y-%m-%d')

    return jsonify(calculate_func(room_id, date_start, date_end))


@bp_payment.route('/rewards_summary')
def rewards_summary():
    activation_start_date = request.args.get('activation_start_date')
    activation_end_date = request.args.get('activation_end_date')
    include_inactive = parse_bool(request.args.get('include_inactive'))

    try:
        rooms, _, _ = get_rooms_by_activation_range(
            activation_start_date,
            activation_end_date,
            include_inactive
        )
    except ValueError:
        rooms = []

    rooms_serialized = Serializer.serialize_list(rooms)
    return render_template(
        'rewards.html',
        rooms=rooms_serialized,
        activation_start_date=activation_start_date or '',
        activation_end_date=activation_end_date or '',
        include_inactive=include_inactive
    )


@bp_payment.route('/rewards_summary/batch_preview', methods=['GET'])
def rewards_summary_batch_preview():
    activation_start_date = request.args.get('activation_start_date')
    activation_end_date = request.args.get('activation_end_date')
    include_inactive = parse_bool(request.args.get('include_inactive'))

    try:
        rooms, _, _ = get_rooms_by_activation_range(
            activation_start_date,
            activation_end_date,
            include_inactive
        )
    except ValueError as exc:
        return jsonify({'error': str(exc)}), 400

    date_end = datetime.now()
    room_previews = [build_room_reward_preview(room, date_end) for room in rooms]

    return jsonify({
        'rooms': room_previews,
        'summary': {
            'room_count': len(room_previews),
            'payable_user_count': sum(room['payable_user_count'] for room in room_previews),
            'total_reward': round(sum(room['total_reward'] for room in room_previews), 2)
        }
    })
