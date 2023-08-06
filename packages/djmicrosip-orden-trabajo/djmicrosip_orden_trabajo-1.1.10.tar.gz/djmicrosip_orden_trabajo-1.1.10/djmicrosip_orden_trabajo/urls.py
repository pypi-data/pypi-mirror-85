# from django.conf.urls import patterns, url
from django.urls import path,include
from .views import *

urlpatterns = (
	path('', index),
	path('info_cliente/', info_cliente),
    path('pedido/<str:folio>/', add_pedido),
    
    path('lista_pedidos/', lista_pedidos),
    path('get_pedido/', get_pedido),
    path('get_venta/', get_venta),
    
    path('inf_articulo/', inf_articulo),
    path('vendedor_asignar/', vendedor_asignar),
    path('get_detalles/', get_detalles),
    path('change_progress/', change_progress),
    path('fin_progress/', fin_progress),
    path('return_progress/', return_progress),
    path('get_tiempos/', get_tiempos),
    path('actualiza_base_datos/', actualiza_base_datos),
    path('preferencias/', preferencias),
    path('nota_pedido/<int:id_doc>/', nota_pedido),
    path('firma/<int:id_crm>/', firma),
    path('enviar_correo/', enviar_correo),
    path('lista_vendedores/', lista_vendedores),
    path('configuracion_usuarios_onesignal/<int:id_vendedor>/', configuracion_usuarios_onesignal),
    path('search_id/', search_id),
    path('send_notifications_preprogramadas/', send_notifications_preprogramadas),
    path('usuario_cliente/', usuario_cliente),
    path('pedido_solictud/', pedido_solictud),
    path('lista_solicitudes/', lista_solicitudes),
)

  