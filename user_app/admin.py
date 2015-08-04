from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


# Register your models here.


from .models import MyUser


class OtherUser(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'dob', 'photo',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    list_display = ('email', 'first_name', 'last_name',)
    list_filter = ('is_staff', 'is_superuser', 'is_active', )
    search_fields = ('email', 'first_name', 'last_name',)
    ordering = ('email',)


admin.site.register(MyUser, OtherUser)
