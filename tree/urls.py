from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='tree-index'),
    path('ngoai', views.ngoai, name='tree-ngoai'),
    path('member/<str:memberName>', views.displayMember, name='tree-member'),
]