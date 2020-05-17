from django.urls import path,include
from .views import *
from rest_framework import routers

router=routers.DefaultRouter()
router.register('app',sentimentviews)

urlpatterns=[
    path('api/',include(router.urls)),
    path('status/',sentimentclassifier)
]