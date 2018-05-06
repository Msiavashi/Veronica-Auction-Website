# encoding=utf8
import sys

from markupsafe import Markup
from wtforms.widgets import HTMLString

reload(sys)
sys.setdefaultencoding('utf-8')
from database import db
from project import app
from PIL import Image
from wtforms.widgets import html_params, HTMLString
from project.model import *
import os
import os.path as op
import ast
from flask import url_for, redirect, render_template, request, abort
from flask_admin import Admin, form
from flask_admin.contrib.sqla import ModelView
from flask_admin._compat import string_types, urljoin
from wtforms.utils import unset_value
from flask_admin.helpers import get_url
from flask_admin.form.upload import ImageUploadField
# git pto

# Flask views
@app.route('/')
def index():
    return render_template('index.html')


class MultipleImageUploadInput(object):
    empty_template = "<input %(file)s multiple>"

    # display multiple images in edit view of flask-admin
    data_template = ("<div class='image-thumbnail'>"
                     "   %(images)s"
                     "</div>"
                     "<input %(file)s multiple>")

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

    def get_attributes(self, field):

        for item in ast.literal_eval(field.data):

            filename = item

            if field.thumbnail_size:
                filename = field.thumbnail_size(filename)

            if field.url_relative_path:
                filename = urljoin(field.url_relative_path, filename)

            yield get_url(field.endpoint, filename=filename), item


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


# Create admin
admin = Admin(
    app,
    " بید بازی ",
    base_template='admin.html',
    template_mode='bootstrap3',
)
# Create directory for file fields to use
file_path = op.join(op.dirname(__file__), 'files')
try:
    os.mkdir(file_path)
except OSError:
    pass


class ProductMultipleFileUpload(ModelView):
    form_excluded_columns = ('likes', 'views', 'events', 'items', 'comments')

    def _list_thumbnail(view, context, model, name):
        if not model.images:
            return ''

        def gen_img(filename):
            return '<img src="{}">'.format(url_for('static',
                                                   filename="images/custom/" + form.thumbgen_filename(image)))

        return Markup("<br />".join([gen_img(image) for image in ast.literal_eval(model.image)]))

    column_formatters = {'images': _list_thumbnail}

    form_extra_fields = {'images': MultipleImageUploadField("Images",
                                                            base_path="app/static/images/custom",
                                                            url_relative_path="images/custom/",
                                                            thumbnail_size=(400, 300, 1))}


# Product Administrative View
# class ProductView(ModelView):
#     form_excluded_columns = ('likes', 'views', 'events', 'items', 'comments')
#
#     # Override form field to use Flask-Admin FileUploadField
#     form_overrides = {
#         'images': form.MultipleFileUploadField
#     }
#
#     # Pass additional parameters to 'path' to FileUploadField constructor
#     form_args = {
#         'images': {
#             'label': 'Image File',
#             'base_path': file_path,
#             'allow_overwrite': False
#         }
#     }


admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Category, db.session))
admin.add_view(ProductMultipleFileUpload(Product, db.session))
admin.add_view(ModelView(Auction, db.session))
admin.add_view(ModelView(Address, db.session))
admin.add_view(ModelView(Gift, db.session))
admin.add_view(ModelView(Insurance, db.session))
admin.add_view(ModelView(Inventory, db.session))
admin.add_view(ModelView(Manufacture, db.session))
admin.add_view(ModelView(Offer, db.session))
admin.add_view(ModelView(Item, db.session))
