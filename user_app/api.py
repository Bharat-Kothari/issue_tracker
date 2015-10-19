from tastypie.authorization import Authorization
from tastypie.constants import ALL_WITH_RELATIONS, ALL
from tastypie.resources import ModelResource
from models import MyUser


class UserResource(ModelResource):
    class Meta:
        queryset = MyUser.objects.all()
        resource_name = 'myuser'
        authorization = Authorization()
        filtering = {
            'first_name': ALL,
            }