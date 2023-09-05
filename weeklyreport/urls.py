from django.urls import path
from . import views

urlpatterns = [
    path('', views.show),
    path('show/', views.show),
    path('showold', views.showold),
    path('<str:team>/add', views.add),
    path('<str:team>/details', views.details),
    path('<str:team>/edit/<int:id>', views.edit),
    path('<str:team>/update/<int:id>', views.update),
    path('<str:team>/delete/<int:id>', views.destroy),
    path('<str:team>/add_service', views.add_service),
    path('<str:team>/delete_service/<int:id>', views.delete_service),
    path('<str:team>/sendmailtome', views.send_mail_to_me),
    path('<str:team>/sendmailtomanager', views.send_mail_to_manager),
    path('<str:team>/sendmailtounithead', views.send_mail_to_unithead),
    path('<str:team>/search', views.search),
]
