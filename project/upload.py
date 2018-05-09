from markupsafe import Markup
from . import app
from PIL import Image
import ast
from flask import url_for
from flask_admin import form
from flask_admin.contrib.sqla import ModelView
from .utils import MultipleImageUploadField


class ProductUpload(ModelView):
    form_excluded_columns = ('likes', 'views', 'events', 'items', 'comments')

    def _list_thumbnail(view, context, model, name):
        if not model.images:
            return None

        def gen_img(filename):
            return '<img src="{}">'.format(url_for('static',
                                                   filename="images/products/" + form.thumbgen_filename(model.images)))

        return Markup("<br />".join(gen_img(model.images) for image in ast.literal_eval(model.images)))

    column_formatters = {'images': _list_thumbnail}

    form_extra_fields = {'images': MultipleImageUploadField("Images",
                                                            base_path="project/static/images/products",
                                                            url_relative_path="images/products/",
                                                            thumbnail_size=(64, 64, 1))}

class AdvertisementUpload(ModelView):

    def _list_thumbnail(view, context, model, name):
        if not model.images:
            return None

        def gen_img(filename):
            return '<img src="{}">'.format(url_for('static',
                                                   filename="images/ads/" + form.thumbgen_filename(model.images)))

        return Markup("<br />".join(gen_img(model.images) for image in ast.literal_eval(model.images)))

    column_formatters = {'images': _list_thumbnail}

    form_extra_fields = {'images': MultipleImageUploadField("Images",
                                                            base_path="project/static/images/ads",
                                                            url_relative_path="images/ads/",
                                                            thumbnail_size=(64, 64, 1))}

class CategoryUpload(ModelView):

    def _list_thumbnail(view, context, model, name):
        if not model.icon:
            return None

        def gen_img(filename):
            return '<img src="{}">'.format(url_for('static',
                                                   filename="images/category/" + form.thumbgen_filename(model.icon)))

        return Markup("<br />".join(gen_img(model.icon) for image in ast.literal_eval(model.icon)))

    column_formatters = {'icon': _list_thumbnail}

    form_extra_fields = {'icon': MultipleImageUploadField("icon",
                                                            base_path="project/static/images/icons/category",
                                                            url_relative_path="images/icons/category/",
                                                            thumbnail_size=(64, 64, 1))}
