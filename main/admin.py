from django.contrib import admin
from django.contrib.auth.models import User

from .models import Post


class UserAdmin(admin.ModelAdmin):
    def group(self, user):
        groups = []
        for group in user.groups.all():
            groups.append(group.name)
        return ' '.join(groups)

    group.short_description = 'Groups'

    list_display = ('username', 'email', 'first_name', 'last_name', 'group', 'is_staff')

admin.site.unregister(User)

admin.site.register(Post)
admin.site.register(User, UserAdmin)

