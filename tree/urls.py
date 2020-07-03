from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='tree-index'),
    path('<str:memberName>', views.displayMember, name='tree-member'),
]