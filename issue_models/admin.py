from django.contrib import admin

# Register your models here.
from .models import MyUser
admin.site.register(MyUser)

# from .models import new_project,projects_member,stories
# admin.site.register(new_project)
# admin.site.register(projects_member)
# admin.site.register(stories)
