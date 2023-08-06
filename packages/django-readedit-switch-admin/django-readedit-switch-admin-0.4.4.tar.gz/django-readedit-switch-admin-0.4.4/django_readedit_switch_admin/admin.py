from django.contrib.admin.options import BaseModelAdmin
from django.contrib.admin.options import InlineModelAdmin
from django.contrib.admin.options import csrf_protect_m
from django.contrib.admin.options import TO_FIELD_VAR
from django.contrib.admin.options import unquote
from django.urls import reverse

class DjangoReadEditSwitchAdmin(BaseModelAdmin):
    # Work together with templatetag readedit_switch_submit_row

    def is_edit_view(self, request, obj=None):
        if not obj:
            return False
        app_label = obj._meta.app_label
        model_name = obj._meta.model_name
        edit_view_url = reverse("admin:{}_{}_change".format(app_label, model_name), args=[obj.pk])
        if edit_view_url == request.path:
            return True
        else:
            return False

    def get_changing_object(self, request, object_id):
        if not object_id:
            return None
        else:
            to_field = request.POST.get(TO_FIELD_VAR, request.GET.get(TO_FIELD_VAR))
            obj = self.get_object(request, unquote(object_id), to_field)
            return obj

    @csrf_protect_m
    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        obj = self.get_changing_object(request, object_id)
        extra_context = extra_context or {}
        extra_context["with_django_readedit_switch_admin"] = True
        extra_context["has_change_permission_real"] = self.has_change_permission_real(request, obj)
        return super().changeform_view(request, object_id, form_url, extra_context)

    def has_change_permission(self, request, obj=None):
        result = super().has_change_permission(request, obj)
        if not self.is_edit_view(request, obj):
            return result
        if hasattr(request, "django_readedit_switch_admin_ignore_edit_flag"):
            return result
        else:
            if not request.GET.get("_edit_flag"):
                return False
            else:
                return result # Not True, result may be False

    def has_change_permission_real(self, request, obj=None):
        setattr(request, "django_readedit_switch_admin_ignore_edit_flag", True)
        try:
            return self.has_change_permission(request, obj)
        finally:
            delattr(request, "django_readedit_switch_admin_ignore_edit_flag")

    def has_add_permission(self, request):
        result = super().has_add_permission(request)
        if hasattr(request, "django_readedit_switch_admin_ignore_edit_flag"):
            return result
        else:
            if not request.GET.get("_edit_flag") and isinstance(self, InlineModelAdmin) and not request.path.endswith("/add/"):
                return False
            else:
                return result

    def has_add_permission_real(self, request):
        setattr(request, "django_readedit_switch_admin_ignore_edit_flag", True)
        try:
            return self.has_add_permission(request)
        finally:
            delattr(request, "django_readedit_switch_admin_ignore_edit_flag")

    def has_delete_permission(self, request, obj=None):
        result = super().has_delete_permission(request, obj)
        if hasattr(request, "django_readedit_switch_admin_ignore_edit_flag"):
            return result
        else:
            if not request.GET.get("_edit_flag") and isinstance(self, InlineModelAdmin):
                return False
            else:
                return result

    def has_delete_permission_real(self, request, obj=None):
        setattr(request, "django_readedit_switch_admin_ignore_edit_flag", True)
        try:
            return self.has_delete_permission(request, obj)
        finally:
            delattr(request, "django_readedit_switch_admin_ignore_edit_flag")

    class Media:
        css = {
            "all": [
                "admin/css/django-readedit-switch-admin.css",
            ]
        }
        js = [
            "admin/js/vendor/jquery/jquery.js",
            "admin/js/django-readedit-switch-admin.js",
            "admin/js/jquery.init.js",
        ]
