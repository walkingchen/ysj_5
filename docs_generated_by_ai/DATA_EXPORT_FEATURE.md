# 数据导出功能说明

## 功能概述

在 Flask-Admin 后台管理系统中新增了数据导出功能，允许管理员一键导出数据库中的关键数据表，并打包为 ZIP 文件下载。

## 功能特性

### 1. 导出的数据表

- **tb_post_public** - 公开帖子数据
- **tb_post_comment** - 评论数据  
- **tb_post_like** - 点赞数据
- **tb_post_flag** - 举报数据
- **tb_post_factcheck** - Fact Check 数据
- **tb_room** - 房间数据
- **tb_room_member** - 房间成员数据
- **tb_user** - 用户数据（**自动过滤掉 password 字段**）

### 2. 导出格式

- **文件格式**: CSV（逗号分隔值）
- **编码**: UTF-8 with BOM（支持 Excel 直接打开，中文不乱码）
- **打包格式**: ZIP 压缩包
- **文件命名**: `chattera_data_export_YYYYMMDD_HHMMSS.zip`（带时间戳）

### 3. 数据安全

- ✅ 自动过滤 `tb_user` 表的 `password` 字段
- ✅ 导出页面提供安全警告提示
- ✅ 仅管理员可访问

## 使用方法

### 步骤 1: 访问后台管理

1. 启动 Flask 应用
2. 访问后台管理页面（通常是 `/admin`）
3. 使用管理员账号登录

### 步骤 2: 导出数据

1. 在左侧菜单中找到 **System** 分类
2. 点击 **数据导出** 菜单项
3. 查看导出说明页面
4. 点击 **开始导出数据** 按钮
5. 浏览器会自动下载 ZIP 文件

### 步骤 3: 查看导出数据

1. 解压下载的 ZIP 文件
2. 每个表对应一个 CSV 文件
3. 可使用 Excel、Numbers 或文本编辑器打开

## 技术实现

### 文件修改清单

#### 1. `/y5-backend-flask/views.py`

**新增**:
- `DataExportView` 类 - 数据导出视图
- `index()` 方法 - 显示导出页面
- `export()` 方法 - 执行数据导出
- `_export_table()` 方法 - 导出单个表

**新增导入**:
```python
import io
import zipfile
import csv
from datetime import datetime
from flask import send_file, flash, redirect
from flask_admin import BaseView, expose
from models import PostFactcheck
```

#### 2. `/y5-backend-flask/app.py`

**修改**:
```python
# 导入 DataExportView
from views import (..., DataExportView)

# 注册数据导出视图
admin.add_view(DataExportView(name='数据导出', endpoint='dataexport', category='System'))
```

#### 3. `/y5-backend-flask/templates/admin/data_export.html`

**新增**: 数据导出页面模板

## 代码示例

### DataExportView 核心逻辑

```python
class DataExportView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/data_export.html')
    
    @expose('/export')
    def export(self):
        memory_file = io.BytesIO()
        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            self._export_table(zf, 'tb_user', User, exclude_fields=['password'])
            # ... 导出其他表
        
        memory_file.seek(0)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'chattera_data_export_{timestamp}.zip'
        
        return send_file(
            memory_file,
            mimetype='application/zip',
            as_attachment=True,
            attachment_filename=filename
        )
```

### 导出单表逻辑

```python
def _export_table(self, zipfile_obj, table_name, model_class, exclude_fields=None):
    records = model_class.query.all()
    columns = [col.name for col in model_class.__table__.columns 
               if col.name not in (exclude_fields or [])]
    
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=columns)
    writer.writeheader()
    
    for record in records:
        row_data = {col: getattr(record, col, '') for col in columns}
        writer.writerow(row_data)
    
    zipfile_obj.writestr(f'{table_name}.csv', output.getvalue().encode('utf-8-sig'))
```

## 兼容性说明

- **Flask 版本**: 兼容 Flask 1.0.2+
- **Python 版本**: Python 3.6+
- **数据库**: 兼容 SQLAlchemy 支持的所有数据库

## 注意事项

1. **大数据量**: 如果数据表非常大（数百万行），导出可能需要较长时间，建议优化或分批导出
2. **内存占用**: 当前实现将所有数据加载到内存中，对于超大数据集可能需要流式处理
3. **权限控制**: 确保只有授权的管理员才能访问此功能
4. **数据敏感性**: 导出的数据包含敏感信息，请妥善保管

## 未来改进方向

- [ ] 支持选择性导出（只导出指定的表）
- [ ] 支持日期范围过滤
- [ ] 支持更多导出格式（JSON, Excel, SQL）
- [ ] 添加导出进度显示
- [ ] 支持后台异步导出（大数据量场景）
- [ ] 添加导出历史记录

## 测试

运行测试脚本：
```bash
python3 test_data_export.py
```

## 作者

实现日期: 2026-01-03
