from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.getList),
    path('<int:id>/', views.show),
    path('<int:product_id>/question-list/', views.get_questions_list),
    path('<int:product_id>/question/', views.create_question),
]