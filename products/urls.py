from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('addcomment/<int:id>', views.addcomment, name='addcomment'),
    path('blog/<int:id>', views.BlogDetailView, name='blogdetail'),
    
]
