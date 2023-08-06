import inflection
from django.urls import path
from pydoc import locate

class URLPatternGenerator():

    """Generates urls associated with given name"""

    _class_name = ""
    package = "netbox_aws_accounts"

    def __init__(self, class_name):
        self._class_name = class_name

    def _endpoint(self):
        return inflection.dasherize(inflection.tableize(self._class_name)) + "/"

    def list(self):
        view_class= inflection.camelize(self._class_name) + "ListView"
        return path(
            self._endpoint(),
            locate(f"{self.package}.views.{view_class}").as_view(),
            name=f"{inflection.tableize(self._class_name)}_list"
        )


    def add(self):
        view_class= inflection.camelize(self._class_name) + "CreateView"
        return path(
            self._endpoint() + "add/",
            locate(f"{self.package}.views.{view_class}").as_view(),
            name=f"{inflection.tableize(self._class_name)}_add"
        )

    def edit(self):
        view_class = inflection.camelize(self._class_name) + "EditView"
        return path(
            self._endpoint() + "<int:pk>/edit/",
            locate(f"{self.package}.views.{view_class}").as_view(),
            name=f"{inflection.tableize(self._class_name)}_edit"
        )

    def bulkDelete(self):
        view_class= inflection.camelize(self._class_name) + "BulkDeleteView"
        return path(
            self._endpoint() + "delete/",
            locate(f"{self.package}.views.{view_class}").as_view(),
            name=f"{inflection.tableize(self._class_name)}_delete"
        )
