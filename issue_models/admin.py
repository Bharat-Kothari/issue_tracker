from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.


# from .models import new_project,projects_member,stories
# admin.site.register(new_project)
# admin.site.register(projects_member)
# admin.site.register(stories)



class otheruser(UserAdmin):
    fieldsets = (
        (None, {'fields': ('emailaddr', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name', 'dob','photo',)}),

    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('emailaddr', 'password1', 'password2'),
        }),
    )

    list_display = ('emailaddr', 'first_name', 'last_name',)
    list_filter = ('is_staff', 'is_superuser', 'is_active', )
    search_fields = ('emailaddr', 'first_name', 'last_name',)
    ordering = ('emailaddr',)




from .models import MyUser
admin.site.register(MyUser,otheruser)


import  models
admin.site.register(models.new_project)
admin.site.register(models.stories)

