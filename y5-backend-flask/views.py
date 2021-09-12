import ast
from PIL import Image
from flask import url_for
from flask_admin.contrib.sqla import ModelView
from markupsafe import Markup
from wtforms.widgets import html_params, HTMLString
from wtforms.utils import unset_value
from flask_admin.helpers import get_url
from flask_admin.form.upload import ImageUploadField, thumbgen_filename
from flask_admin._compat import string_types, urljoin

from extensions import db


class RoomModelView(ModelView):
    # can_create = False
    # can_edit = True
    list_columns = ['id', 'room_name', 'room_desc', 'room_type', 'people_limit', 'created_at']
    column_searchable_list = ['room_id', 'people_limit', 'created_at']
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
