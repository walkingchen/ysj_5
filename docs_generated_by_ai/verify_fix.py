#!/usr/bin/env python3
"""
快速验证定时邮件修复是否生效
"""
import sys
sys.path.insert(0, '/Users/codingchan/Documents/work/src/ysj/ysj_5/y5-backend-flask')

from app import app
from models import Room, RoomMember, User, MailTemplate
import time

print("=" * 80)
print("验证定时邮件功能修复")
print("=" * 80)

with app.app_context():
    print("\n✓ 检查代码修复...")
    
    # 读取app.py检查修复
    with open('/Users/codingchan/Documents/work/src/ysj/ysj_5/y5-backend-flask/app.py', 'r') as f:
        content = f.read()
        
        # 检查1: morning mail 模板检查
        if 'if mail_template_morning is None:' in content and 'print(f\'No morning mail template found' in content:
            print("✅ Morning mail 模板检查已添加")
        else:
            print("❌ Morning mail 模板检查未正确添加")
        
        # 检查2: night mail return改为continue
        if 'if day > 8:' in content and 'exceeds 8 days, skipping' in content and 'continue' in content:
            print("✅ Night mail 的 return 已改为 continue")
        else:
            print("❌ Night mail 的 return 未正确修复")
        
        # 检查3: activated_at检查
        if 'if day_activated is None:' in content and 'has no activated_at timestamp' in content:
            print("✅ activated_at 检查已添加")
        else:
            print("❌ activated_at 检查未正确添加")
    
    print("\n✓ 检查数据库状态...")
    
    # 检查激活的rooms
    activated_rooms = Room.query.filter_by(activated=1).all()
    print(f"\n激活的 Room 数量: {len(activated_rooms)}")
    
    for room in activated_rooms:
        if not room.activated_at:
            print(f"  ⚠️ Room {room.id} 缺少 activated_at")
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
        valid_emails = sum(1 for m in members if User.query.get(m.user_id) and User.query.get(m.user_id).email)
        
        status = "✅" if n <= 8 else "⚠️"
        template_status = "✅" if morning_template and night_template else "❌"
        member_status = "✅" if valid_emails > 0 else "⚠️"
        
        print(f"  {status} Room {room.id} - 第{n}天 | 模板:{template_status} | 成员:{member_status}({valid_emails}人)")
        
        if n > 8:
            print(f"      注意: 已超过8天，将被跳过（这是预期行为）")
        if not morning_template or not night_template:
            print(f"      警告: 缺少第{n}天的邮件模板")
        if valid_emails == 0:
            print(f"      警告: 没有有效邮箱的成员")

    print("\n" + "=" * 80)
    print("修复验证完成！")
    print("=" * 80)
    print("\n建议:")
    print("  1. 重启应用以使修改生效")
    print("  2. 等待到定时时间（7:00或22:00）观察是否自动发送")
    print("  3. 或手动测试: curl http://localhost:5000/mail_morning")
    print("  4. 查看应用日志确认邮件发送状态")
    print()



