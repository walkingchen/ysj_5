#!/usr/bin/env python3
"""
测试定时邮件修复后的功能
"""
import sys
import os
sys.path.insert(0, '/Users/codingchan/Documents/work/src/ysj/ysj_5/y5-backend-flask')

print("=" * 80)
print("测试定时邮件功能修复")
print("=" * 80)

# 导入必要的模块
from app import app, scheduler, logger
from models import Room, RoomMember, User, MailTemplate
import time

with app.app_context():
    print("\n✓ 1. 检查调度器状态")
    print("-" * 80)
    print(f"调度器运行状态: {scheduler.running}")
    
    print("\n✓ 2. 检查注册的定时任务")
    print("-" * 80)
    jobs = scheduler.get_jobs()
    print(f"定时任务数量: {len(jobs)}")
    
    for job in jobs:
        print(f"\n任务ID: {job.id}")
        print(f"  名称: {job.name}")
        print(f"  触发器: {job.trigger}")
        print(f"  下次运行: {job.next_run_time}")
        print(f"  函数: {job.func}")
    
    print("\n✓ 3. 检查激活的Room")
    print("-" * 80)
    activated_rooms = Room.query.filter_by(activated=1).all()
    print(f"激活的Room数量: {len(activated_rooms)}")
    
    if not activated_rooms:
        print("⚠️ 警告: 没有激活的Room")
    else:
        for room in activated_rooms:
            if not room.activated_at:
                print(f"  Room {room.id}: activated_at为None ❌")
                continue
            
            # 计算天数
            local_time = time.localtime(int(room.activated_at.timestamp()))
            activated_day = local_time.tm_yday
            activated_year = local_time.tm_year
            now = time.localtime(time.time())
            now_day = now.tm_yday
            now_year = now.tm_year
            
            if now_year > activated_year:
                n = now_day + 365 - activated_day + 1
            else:
                n = now_day - activated_day + 1
            
            # 检查邮件模板
            morning_template = MailTemplate.query.filter_by(
                room_id=room.id, day=n, mail_type=1
            ).first()
            night_template = MailTemplate.query.filter_by(
                room_id=room.id, day=n, mail_type=2
            ).first()
            
            # 检查成员
            members = RoomMember.query.filter_by(room_id=room.id).all()
            valid_emails = 0
            for m in members:
                user = User.query.get(m.user_id)
                if user and user.email:
                    valid_emails += 1
            
            day_status = "✅" if n <= 8 else "⚠️ (超过8天)"
            template_status = "✅" if morning_template and night_template else "❌"
            member_status = "✅" if valid_emails > 0 else "❌"
            
            print(f"  Room {room.id}:")
            print(f"    - 第{n}天 {day_status}")
            print(f"    - 邮件模板 {template_status}")
            print(f"    - 有效邮箱成员 {member_status} ({valid_emails}人)")
    
    print("\n✓ 4. 测试建议")
    print("-" * 80)
    print("1. 手动测试morning mail:")
    print("   curl http://localhost:5000/mail_morning")
    print()
    print("2. 手动测试night mail:")
    print("   curl http://localhost:5000/mail_night")
    print()
    print("3. 查看日志文件:")
    print("   tail -f y5-backend-flask/logs/app.log")
    print()
    print("4. 等待定时触发（22:00），然后检查日志")
    print()
    print("5. 预期日志输出:")
    print("   ================================================================================")
    print("   Night mail task started")
    print("   ================================================================================")
    print("   Found X activated rooms")
    print("   ...")
    print("   Night mail task completed successfully")

print("\n" + "=" * 80)
print("测试完成")
print("=" * 80)


