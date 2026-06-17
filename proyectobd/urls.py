from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_reservaciones, name='lista_reservaciones'),
    path('nueva/', views.crear_reservacion, name='crear_reservacion'),
    path('reservacion/<int:reservacion_id>/', views.detalle_reservacion, name='detalle_reservacion'),
    path('reservacion/<int:reservacion_id>/confirmar/', views.confirmar_reservacion, name='confirmar_reservacion'),
    path('reservacion/<int:reservacion_id>/cancelar/', views.cancelar_reservacion, name='cancelar_reservacion'),
    path('reservacion/<int:reservacion_id>/finalizar/', views.finalizar_reservacion, name='finalizar_reservacion'),
    path('reservacion/<int:reservacion_id>/editar/', views.editar_reservacion, name='editar_reservacion'),
]