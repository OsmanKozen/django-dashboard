from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.addservice, name='addservice'),    
    path('show/', views.showservice, name='showservice'),  
    path('<str:team>/update/<int:id>', views.updateservice, name='updateservice'),    
    path('<str:team>/delete/<int:id>', views.deleteservice, name='deleteservice'),
    path('export_excel', views.export_excel, name='export-excel'),    
]
