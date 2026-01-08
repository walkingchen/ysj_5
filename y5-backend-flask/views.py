import ast
import time
import io
import zipfile
import csv
from datetime import datetime

from PIL import Image
from flask import url_for, send_file, flash, redirect
from flask_admin.actions import action
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from markupsafe import Markup
from wtforms.widgets import html_params, HTMLString
from wtforms.utils import unset_value
from flask_admin.helpers import get_url
from flask_admin.form.upload import ImageUploadField, thumbgen_filename
from flask_admin._compat import string_types, urljoin

from extensions import db
from mail import mail_notify
from models import (RoomMember, User, Room, PublicPost, PostComment, 
                   PostLike, PostFlag, PostFactcheck)


class YModelView(ModelView):
    can_create = False
    can_edit = True


class RoomMemberModelView(YModelView):
    can_create = True
    can_edit = True


class PrivateMessageView(YModelView):
    column_list = [
        'id',
        'message_id',
        'message_title',
        'message_content',
        'photo_uri',
        # 'keywords',
        'abstract',
        'updated_at',
        'created_at'
    ]


class UserModelView(ModelView):
    # can_create = False
    # can_edit = True
    column_list = ['id', 'email', 'nickname', 'created_at', 'updated_at']


class RoomModelView(ModelView):
    # can_create = False
    # can_edit = True
    column_list = ['id', 'room_name', 'activated', 'room_desc', 'room_type', 'people_limit', 'created_at']
    column_searchable_list = ['room_id', 'people_limit', 'created_at']
    column_filters = column_searchable_list

    @action('activate', 'Activate Rooms', 'Are you sure you want to start selected rooms?')
    def action_start_rooms(self, ids):
        for id in ids:
            room = Room.query.filter_by(id=id).first()
            room.activated = 1
            room.updated_at = time.time()
            db.session.commit()

    @action('deactivate', 'Deactivate Rooms', 'Are you sure you want to stop selected rooms?')
    def action_stop_rooms(self, ids):
        for id in ids:
            room = Room.query.filter_by(id=id).first()
            room.activated = 0
            room.updated_at = None
            db.session.commit()

    # def after_model_change(self, form, model, is_created):
    #     # if activated, send mail
    #     # if form._obj.activated == 1:
    #     status = form._obj.activated
    #     # send mail
    #     members = RoomMember.query.filter_by(room_id=form._obj.id, activated=1).all()
    #     users = []
    #     for member in members:
    #         user = User.query.filter_by(id=member.user_id).first()
    #         users.append(user)
    #     mail_notify(users, status)


class PostModelView(ModelView):
    can_edit = False
    can_delete = False
    column_list = [
        'id',
        'user_id',
        'message_id',
        'post_title',
        'post_content',
        # 'post_type',
        'photo_uri',
        # 'keywords',
        'abstract',
        'topic',
        # 'timeline_type',
        'room_id',
        'post_shared_id',
        'is_system_post',
        'created_at',
        'updated_at'
    ]

    def _post_content_formatter(view, context, model, name):
        # Format your string here e.g show first 80 characters
        # can return any valid HTML e.g. a link to another view to show the detail or a popup window
        if model.post_content is not None:
            return model.post_content[:200] + '...'
        return None

    def _abstract_formatter(view, context, model, name):
        # Format your string here e.g show first 80 characters
        # can return any valid HTML e.g. a link to another view to show the detail or a popup window
        if model.abstract is not None:
            return model.abstract[:140] + '...'
        return None

    column_formatters = {
        'post_content': _post_content_formatter,
        'abstract': _abstract_formatter
    }

    column_searchable_list = ['post_title', 'abstract', 'room_id']
    column_filters = column_searchable_list


class PublicPostModelView(PostModelView):
    column_searchable_list = ['post_title', 'abstract', 'room_id', 'is_system_post']
    column_filters = column_searchable_list


class MultipleImageUploadInput(object):
    empty_template = "<input %(file)s multiple>"

    # display multiple images in edit view of flask-admin
    data_template = ("<div class='image-thumbnail'>"
                     "   %(images)s"
                     "</div>"
                     "<input %(file)s multiple>")

    def get_attributes(self, field):

        for item in ast.literal_eval(field.data):
            filename = item

            # FIXME not work
            # if field.thumbnail_size:
            #     filename = field.thumbnail_size(filename)

            if field.url_relative_path:
                filename = urljoin(field.url_relative_path, filename)

            yield get_url(field.endpoint, filename=filename), item

    def __call__(self, field, **kwargs):
        kwargs.setdefault("id", field.id)
        kwargs.setdefault("name", field.name)

        args = {
            "file": html_params(type="file", **kwargs),
        }

        if field.data and isinstance(field.data, string_types):
            attributes = self.get_attributes(field)
            args["images"] = "&emsp;".join(["<img src='{}' /><input type='checkbox' name='{}-delete'>Delete</input>"
                                           .format(src, filename) for src, filename in attributes])
            template = self.data_template
        else:
            template = self.empty_template

        return HTMLString(template % args)


class MultipleImageUploadField(ImageUploadField):
    widget = MultipleImageUploadInput()

    def process(self, formdata, data=unset_value):

        self.formdata = formdata  # get the formdata to delete images
        return super(MultipleImageUploadField, self).process(formdata, data)

    def process_formdata(self, valuelist):

        self.data = list()

        for value in valuelist:
            if self._is_uploaded_file(value):
                self.data.append(value)

    def populate_obj(self, obj, name):

        field = getattr(obj, name, None)

        if field:
            filenames = ast.literal_eval(field)

            for filename in filenames[:]:
                if filename + "-delete" in self.formdata:
                    self._delete_file(filename)
                    filenames.remove(filename)
        else:
            filenames = list()

        for data in self.data:
            if self._is_uploaded_file(data):
                self.image = Image.open(data)

                filename = self.generate_name(obj, data)
                filename = self._save_file(data, filename)

                data.filename = filename
                filenames.append(filename)

        setattr(obj, name, str(filenames))


class ModelHasMultipleImages(db.Model):
    id = db.Column(db.Integer(), primary_key=1)

    # len of str representation of filename lists may exceed the len of field

    image = db.Column(db.String(128))


class ModelViewHasMultipleImages(ModelView):

    def _list_thumbnail(view, context, model, name):
        if not model.images:
            return ''

        def gen_img(filename):
            return '<img src="{}">'.format(url_for('static',
                                                   filename="images/uploads/" + thumbgen_filename(filename)))

        return Markup(" ".join([gen_img(image) for image in ast.literal_eval(model.images)]))

    column_formatters = {'images': _list_thumbnail}
    form_extra_fields = {'images': MultipleImageUploadField("Images",
                                                           base_path="static/images/uploads/",
                                                           url_relative_path="images/uploads/",
                                                           thumbnail_size=(60, 60, True))}


class DataExportView(BaseView):
    """数据导出视图 - 导出数据库表数据为 CSV 并打包为 ZIP"""
    
    @expose('/')
    def index(self):
        """显示数据导出页面"""
        return self.render('admin/data_export.html')
    
    @expose('/export')
    def export(self):
        """执行数据导出"""
        try:
            # 创建内存中的 ZIP 文件
            memory_file = io.BytesIO()
            
            with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
                # 导出各个表
                self._export_table(zf, 'tb_post_public', PublicPost)
                self._export_table(zf, 'tb_post_comment', PostComment)
                self._export_table(zf, 'tb_post_like', PostLike)
                self._export_table(zf, 'tb_post_flag', PostFlag)
                self._export_table(zf, 'tb_post_factcheck', PostFactcheck)
                self._export_table(zf, 'tb_room', Room)
                self._export_table(zf, 'tb_room_member', RoomMember)
                self._export_table(zf, 'tb_user', User, exclude_fields=['password'])
            
            # 重置文件指针
            memory_file.seek(0)
            
            # 生成文件名（带时间戳）
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'chattera_data_export_{timestamp}.zip'
            
            # Flask 1.x 使用 attachment_filename，Flask 2.x 使用 download_name
            return send_file(
                memory_file,
                mimetype='application/zip',
                as_attachment=True,
                attachment_filename=filename
            )
            
        except Exception as e:
            flash(f'数据导出失败: {str(e)}', 'error')
            return redirect(url_for('.index'))
    
    def _export_table(self, zipfile_obj, table_name, model_class, exclude_fields=None):
        """
        导出单个表到 CSV
        
        Args:
            zipfile_obj: ZipFile 对象
            table_name: 表名
            model_class: SQLAlchemy 模型类
            exclude_fields: 要排除的字段列表（如 password）
        """
        exclude_fields = exclude_fields or []
        
        # 查询所有数据
        records = model_class.query.all()
        
        if not records:
            # 如果表为空，创建一个空的 CSV 文件
            csv_content = f"# {table_name} - No data\n"
            zipfile_obj.writestr(f'{table_name}.csv', csv_content)
            return
        
        # 获取所有列名（排除指定字段）
        columns = [col.name for col in model_class.__table__.columns 
                   if col.name not in exclude_fields]
        
        # 创建 CSV 内容
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=columns)
        writer.writeheader()
        
        # 写入数据
        for record in records:
            row_data = {}
            for col in columns:
                value = getattr(record, col, None)
                # 处理特殊类型
                if value is None:
                    row_data[col] = ''
                elif isinstance(value, datetime):
                    row_data[col] = value.strftime('%Y-%m-%d %H:%M:%S')
                else:
                    row_data[col] = str(value)
            writer.writerow(row_data)
        
        # 将 CSV 内容添加到 ZIP
        csv_content = output.getvalue()
        zipfile_obj.writestr(f'{table_name}.csv', csv_content.encode('utf-8-sig'))  # 使用 BOM 以支持 Excel
        output.close()
