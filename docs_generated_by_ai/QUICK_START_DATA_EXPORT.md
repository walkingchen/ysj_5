# 数据导出功能 - 快速启动指南

## ✅ 功能已实现

数据导出功能已经完全实现并可以使用！

## 🚀 立即使用

### 1. 重启 Flask 应用

```bash
cd y5-backend-flask
# 如果使用 gunicorn
pkill gunicorn
gunicorn -c gunicorn.py app:app

# 或者如果使用 flask run
flask run
```

### 2. 访问后台管理

打开浏览器访问：
```
http://your-server:port/admin
```

### 3. 导出数据

1. 登录管理员账号
2. 在左侧菜单找到 **System** → **数据导出**
3. 点击 **开始导出数据** 按钮
4. 自动下载 `chattera_data_export_YYYYMMDD_HHMMSS.zip`

### 4. 解压查看

```bash
unzip chattera_data_export_20260103_120000.zip
ls -lh *.csv
```

你会看到：
- `tb_post_public.csv` - 公开帖子
- `tb_post_comment.csv` - 评论
- `tb_post_like.csv` - 点赞
- `tb_post_flag.csv` - 举报
- `tb_post_factcheck.csv` - Fact Check
- `tb_room.csv` - 房间
- `tb_room_member.csv` - 房间成员
- `tb_user.csv` - 用户（不含密码）

## 📋 实现清单

### ✅ 已完成

- [x] 创建 `DataExportView` 类
- [x] 实现 8 个表的导出逻辑
- [x] 自动过滤 `tb_user.password` 字段
- [x] CSV 格式导出（UTF-8 with BOM）
- [x] ZIP 打包压缩
- [x] 文件名时间戳
- [x] 前端导出页面（Bootstrap 3）
- [x] 注册到 Flask-Admin
- [x] 兼容 Flask 1.0.2
- [x] 语法检查通过

### 📝 修改的文件

1. **y5-backend-flask/views.py** ⬅️ 新增 `DataExportView` 类
2. **y5-backend-flask/app.py** ⬅️ 注册导出视图
3. **y5-backend-flask/templates/admin/data_export.html** ⬅️ 新建模板

### 📄 新增的文件

1. **DATA_EXPORT_FEATURE.md** - 完整功能文档
2. **QUICK_START_DATA_EXPORT.md** - 本文件
3. **test_data_export.py** - 测试脚本

## 🔍 功能验证

### 检查语法（已通过）

```bash
cd y5-backend-flask
python3 -m py_compile views.py app.py
# 无错误输出 = 通过 ✅
```

### 测试导入

```python
from views import DataExportView
from models import PublicPost, PostComment, PostLike, PostFlag, PostFactcheck
# 无错误 = 通过 ✅
```

## 📸 效果预览

### 后台菜单
```
Flask Admin
├── User
├── Room
│   ├── Room
│   ├── Room Prototype
│   └── Room Member
├── Post
│   ├── Public Post
│   ├── Post Comment
│   ├── Post Flag
│   └── Post Like
├── Private Message
│   ├── Private Message Pool
│   └── Private Message Assign
├── System Message
│   └── System Message Pool
├── Daily Poll
│   └── Daily Poll Assign
└── System  ⬅️ 新增分类
    └── 数据导出 ⬅️ 新增菜单
```

### 导出页面内容

- 📋 导出说明
- 📦 8 个表的列表
- ⬇️ "开始导出数据" 按钮
- ⚠️ 安全警告提示

### 导出的 ZIP 文件结构

```
chattera_data_export_20260103_120000.zip
├── tb_post_public.csv
├── tb_post_comment.csv
├── tb_post_like.csv
├── tb_post_flag.csv
├── tb_post_factcheck.csv
├── tb_room.csv
├── tb_room_member.csv
└── tb_user.csv  (不含 password 列)
```

## ⚠️ 注意事项

1. **首次使用前请备份数据库**
2. **导出的文件包含敏感数据，请妥善保管**
3. **大数据量可能需要较长时间**
4. **确保磁盘空间充足**

## 🐛 故障排除

### 问题 1: 找不到 "数据导出" 菜单

**原因**: Flask 应用未重启

**解决**: 
```bash
# 重启应用
pkill gunicorn
gunicorn -c gunicorn.py app:app
```

### 问题 2: 下载失败

**原因**: 可能是数据量过大或超时

**解决**: 
- 检查服务器日志
- 增加超时时间
- 考虑分批导出

### 问题 3: CSV 乱码

**原因**: 编码问题

**解决**: 
- 使用 Excel 时选择 "数据" → "从文本/CSV" → 选择 UTF-8 编码
- 或使用 Google Sheets（自动识别 UTF-8）

## 📞 支持

如有问题，请查看：
- 详细文档: `DATA_EXPORT_FEATURE.md`
- 服务器日志: `y5-backend-flask/logs/`
- 错误信息: Flask Admin 页面的错误提示

## ✨ 功能完成！

🎉 恭喜！数据导出功能已经完全实现并可以立即使用！

只需要重启 Flask 应用，然后访问后台管理页面即可。
