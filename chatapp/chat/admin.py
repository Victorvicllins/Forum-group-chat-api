from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from chat.models import Farm, Topic, Forum
from .forms import UserAdminCreationForm, UserAdminChangeForm
# Register your models here.

admin.site.site_header = "BJ Farms Administration"
User = get_user_model()

class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = ('email', 'first_name', 'last_name', 'active',)
    list_filter = ('active', 'staff', 'admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        ('personal info', {'fields': ('first_name', 'last_name',)}),
        ('permissions', {'fields': ('admin', 'staff', 'active')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2')
        }),
    )
    search_fields =  ('email', 'first_name',)
    ordering = ('first_name', 'last_name',)
    filter_horizontal = ()

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Farm)
admin.site.register(Forum)
admin.site.register(Topic)
