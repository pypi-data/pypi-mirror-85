import re
from django.contrib.auth.mixins import PermissionRequiredMixin
from utilities.views import BulkDeleteView, BulkImportView, ObjectEditView, ObjectListView
from rest_framework.viewsets import ModelViewSet
from pydoc import locate
import inflection


class CRUDViewGenerator:
    """
        Generator for view classes
        Simple metaclass usage in order to create basic CRUD views.
        Automatically changes names cases, styles etc.

    """

    name = ""
    package = "netbox_aws_accounts"

    def __init__(self, name):
        self.name = name

    def list(self):
        return type(
            self.name + "ListView",
            (PermissionRequiredMixin, ObjectListView),
            {
                "permission_required": self.package + ".view_" + self.name.lower(),
                "queryset": locate(self.package + ".models." + self.name).objects.all(),
                "filterset": locate(self.package + ".filters." + self.name + "Filter"),
                "filterset_form": locate(self.package + ".forms." + self.name + "FilterForm"),
                "table": locate(self.package + ".tables." + self.name + "Table"),
                "template_name": "netbox_aws_accounts/common_list.html",
                "extra_context": lambda
                    self,
                    name=inflection.pluralize(inflection.titleize(self.name)),
                    add_button_link=f"plugins:{ self.package }:{ inflection.tableize(self.name)}_add",
                    delete_button_link=f"plugins:{ self.package }:{ inflection.tableize(self.name) }_delete" : {
                        "title_text" : name,
                        "add_button_link": add_button_link,
                        "delete_button_link": delete_button_link,
                    }
            }
        )

    def create(self):
        return type(
            self.name + "CreateView",
            (PermissionRequiredMixin, ObjectEditView),
            {
                "permission_required": self.package + ".add_" + self.name.lower(),
                "model": locate(self.package + ".models." + self.name),
                "queryset": locate(self.package + ".models." + self.name).objects.all(),
                "model_form": locate(self.package + ".forms." + self.name + "Form"),
                "template_name": "netbox_aws_accounts/common_edit.html",
                "table": locate(self.package + ".tables." + self.name + "Table"),
                "default_return_url": "plugins:netbox_aws_accounts:" + inflection.tableize(self.name) + "_list",
            }
        )

    def bulk_delete(self):
        return type(
            self.name + "BulkDeleteView",
            (PermissionRequiredMixin, BulkDeleteView),
            {
                "permission_required": self.package + ".delete_" + self.name.lower(),
                "queryset": locate(self.package + ".models." + self.name).objects.all(),
                "filterset": locate(self.package + ".filters." + self.name + "Filter"),
                "table": locate(self.package + ".tables." + self.name + "Table"),
                "default_return_url": "plugins:netbox_aws_accounts:" + inflection.tableize( self.name ) + "s_list"
            }
        )

    def edit(self):
        return type(
            self.name + "EditView",
            (self.create(),),
            {
                "permission_required": self.package + ".change_" + self.name.lower()
            }
        )

    def view_set(self):
        return type(
            self.name + "ViewSet",
            (ModelViewSet,),
            {
                "queryset": locate(self.package + ".models." + self.name).objects.all(),
                "serializer_class": locate(self.package + ".api.serializers." + self.name + "Serializer"),
                "filterset_class": locate(self.package + ".filters." + self.name + "Filter"),
            }
        )

