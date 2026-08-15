#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试数据导出功能
"""

def test_import():
    """测试导入是否成功"""
    try:
        from y5_backend_flask.views import DataExportView
        print("✅ DataExportView 导入成功")
        
        from y5_backend_flask.models import (
            PublicPost, PostComment, PostLike, 
            PostFlag, PostFactcheck, Room, RoomMember, User
        )
        print("✅ 所有模型导入成功")
        
        return True
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False


def test_view_structure():
    """测试视图结构"""
    try:
        from y5_backend_flask.views import DataExportView
        from flask_admin import BaseView
        
        # 检查是否继承自 BaseView
        assert issubclass(DataExportView, BaseView), "DataExportView 应该继承自 BaseView"
        print("✅ DataExportView 正确继承 BaseView")
        
        # 检查是否有必要的方法
        view = DataExportView()
        assert hasattr(view, 'index'), "应该有 index 方法"
        assert hasattr(view, 'export'), "应该有 export 方法"
        assert hasattr(view, '_export_table'), "应该有 _export_table 方法"
        print("✅ DataExportView 包含所有必要方法")
        
        return True
    except Exception as e:
        print(f"❌ 视图结构测试失败: {e}")
        return False


def main():
    print("=" * 60)
    print("数据导出功能测试")
    print("=" * 60)
    
    print("\n1. 测试模块导入")
    print("-" * 60)
    if not test_import():
        return
    
    print("\n2. 测试视图结构")
    print("-" * 60)
    if not test_view_structure():
        return
    
    print("\n" + "=" * 60)
    print("✅ 所有测试通过！")
    print("=" * 60)
    
    print("\n功能说明：")
    print("1. 在 Flask-Admin 后台菜单中新增了 'System' 分类")
    print("2. 在 'System' 分类下添加了 '数据导出' 菜单项")
    print("3. 点击后可导出以下表的数据：")
    print("   - tb_post_public (公开帖子)")
    print("   - tb_post_comment (评论)")
    print("   - tb_post_like (点赞)")
    print("   - tb_post_flag (举报)")
    print("   - tb_post_factcheck (Fact Check)")
    print("   - tb_room (房间)")
    print("   - tb_room_member (房间成员)")
    print("   - tb_user (用户，不含密码)")
    print("4. 数据以 CSV 格式导出，打包为 ZIP 文件")
    print("5. 文件名包含时间戳，如: chattera_data_export_20260103_120000.zip")
    
    print("\n使用方法：")
    print("1. 启动 Flask 应用")
    print("2. 访问后台管理页面 (通常是 /admin)")
    print("3. 在左侧菜单找到 'System' -> '数据导出'")
    print("4. 点击 '开始导出数据' 按钮")
    print("5. 浏览器会自动下载 ZIP 文件")


if __name__ == '__main__':
    main()
