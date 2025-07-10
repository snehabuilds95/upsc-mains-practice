



from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_view, name='upload'),
    path('practice/<int:id>/', views.practice_view, name='practice'),
]
