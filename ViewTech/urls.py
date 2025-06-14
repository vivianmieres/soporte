"""
URL configuration for ViewTech project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.Login, name= 'Acceso'),
    path('principal/',views.Principal, name= 'Principal'),
    #modulo usuario
    path('usuario_mante/', views.usuario_mante, name= 'Usuario_mante'),
    path('usuario_mante_pk/<str:pk>', views.usuario_mante_pk, name= 'Usuario_mante_pk'),
    path('usuario_consulta/', views.usuario_consulta, name= 'Usuario_consulta'),
    #modulo usuario - cambio contrasenha
    path('password/', views.usuario_pass, name= 'Usuario_pass'),
    path('password_consulta/', views.usuario_consulta_pass, name= 'Usuario_consulta_pass'),
    path('password_mante/<str:pk>', views.usuario_mante_pass, name= 'Usuario_mante_pass'),
    path('password_mante_login/', views.usuario_mante_pass_login, name= 'Usuario_mante_pass_login'),
    #modulo usuario - cargo
    path('cargo_mante/', views.cargo_mante, name= 'Cargo_mante'),
    path('cargo_mante_pk/<str:pk>', views.cargo_mante_pk, name= 'Cargo_mante_pk'),
    path('cargo_consulta/', views.cargo_consulta, name= 'Cargo_consulta'),
    #modulo usuario - asignacion de cargo
    path('asignar_cargo_mante/', views.asignar_cargo_mante, name= 'Asignar_cargo_mante'),
    path('asignar_cargo_mante_pk/<str:pk>', views.asignar_cargo_mante_pk, name= 'Asignar_cargo_mante_pk'),
    path('asignar_cargo_consulta/', views.asignar_cargo_consulta, name= 'Asignar_cargo_consulta'),
    #modulo cliente
    path('cliente_mante/', views.cliente_mante, name= 'Cliente_mante'),
    path('cliente_mante_pk/<str:pk>', views.cliente_mante_pk, name= 'Cliente_mante_pk'),
    path('cliente_consulta/', views.cliente_consulta, name= 'Cliente_consulta'),
    #telefono cliente
    path('telefono_mante/', views.telefono_mante, name= 'Telefono_mante'),
    path('telefono_mante_pk/<str:pk>', views.telefono_mante_pk, name= 'Telefono_mante_pk'),
    path('telefono_consulta/', views.telefono_consulta, name= 'Telefono_consulta'),
    #prestadora telefono cliente
    path('prestadora_mante/', views.prestadora_mante, name= 'Prestadora_mante'),
    path('prestadora_mante_pk/<str:pk>', views.prestadora_mante_pk, name= 'Prestadora_mante_pk'),
    path('prestadora_consulta/', views.prestadora_consulta, name= 'Prestadora_consulta'),
   #modulo equipo
   path('equipo/',views.equipo, name='Equipo'),
   path('equipo/equipo_consulta/', views.equipo_consulta, name= 'Equipo_consulta'),
   path('equipo/equipo_mante/', views.equipo_mante, name= 'Equipo_mante'),
   path('equipo/equipo_mante_pk/<str:pk>', views.equipo_mante_pk, name= 'Equipo_mante_pk'),
   path('equipo/tipo_equipo_consulta/', views.tipo_equipo_consulta, name= 'Tipo_equipo_consulta'),
   path('equipo/tipo_equipo_mante/', views.tipo_equipo_mante, name= 'Tipo_equipo_mante'),
   path('equipo/tipo_equipo_mante_pk/<str:pk>', views.tipo_equipo_mante_pk, name= 'Tipo_equipo_mante_pk'),
   #modulo solicitud
   path('solicitud/',views.solicitud, name='Solicitud'),         
   path('solicitud/solicitud_consulta/', views.solicitud_consulta, name= 'Solicitud_consulta'),
   path('solicitud/solicitud_mante/', views.solicitud_mante, name= 'Solicitud_mante'),
   path('solicitud/solicitud_mante_pk/<str:pk>', views.solicitud_mante_pk, name= 'Solicitud_mante_pk'),   
   path('solicitud/solicitud_repuesto_acc_consulta/', views.solicitud_repuesto_acc_consulta, name= 'Solicitud_repuesto_acc_consulta'),
   path('solicitud/solicitud_repuesto_acc_mante/', views.solicitud_repuesto_acc_mante, name= 'Solicitud_repuesto_acc_mante'),
   path('solicitud/solicitud_repuesto_acc_mante_pk/<str:pk>', views.solicitud_repuesto_acc_mante_pk, name= 'Solicitud_repuesto_acc_mante_pk'),     
   path('solicitud/estado_consulta/', views.estado_consulta, name= 'Estado_consulta'),
   path('solicitud/estado_mante/', views.estado_mante, name= 'Estado_mante'),
   path('solicitud/estado_mante_pk/<str:pk>', views.estado_mante_pk, name= 'Estado_mante_pk'),     
   #modulo repuesto/accesorio
   path('repuesto_acc/',views.respuesto_acc, name='Repuesto_acc'),
   path('equipo/repuesto_acc_consulta/', views.repuesto_acc_consulta, name= 'Repuesto_acc_consulta'),
   path('equipo/repuesto_acc_mante/', views.repuesto_acc_mante, name= 'Repuesto_acc_mante'),
   path('equipo/repuesto_acc_mante_pk/<str:pk>', views.repuesto_acc_mante_pk, name= 'Repuesto_acc_mante_pk'),
   path('repuesto_acc/tipo_repuesto_acc_consulta/', views.tipo_repuesto_acc_consulta, name= 'Tipo_repuesto_acc_consulta'),
   path('repuesto_acc/tipo_repuesto_acc_mante/', views.tipo_repuesto_acc_mante, name= 'Tipo_repuesto_acc_mante'),
   path('repuesto_acc/tipo_repuesto_acc_mante_pk/<str:pk>', views.tipo_repuesto_acc_mante_pk, name= 'Tipo_repuesto_acc_mante_pk'),
   path("select2/", include("django_select2.urls")),
   #modulo reportes
   path("reporte/solicitud_reporte/", views.solicitud_reporte, name="Solicitud_reporte"),
   path("reporte/estado_tiempo_res_reporte/", views.estado_tiempo_resolucion_reporte, name="Estado_tiempo_res_reporte"),
   path("reporte/repuestos_acc_usados_reporte/", views.repuestos_acc_usados_reporte, name="Repuestos_acc_usados_reporte"), 
   path("reporte/repuesto_acc_inventario/", views.repuesto_acc_inventario, name="Repuesto_acc_inventario"),
   path("reporte/rendimiento_tecnicos_estadistica/", views.rendimiento_tecnicos_estadistica, name="Rendimiento_tecnico_estadistica"),                                                          
   #dashboard
   path('dashboard/solicitud', views.dashboard_solicitudes, name='Dashboard_solicitudes'),
   path('dashboard/encuesta', views.dashboard_encuesta, name='Dashboard_encuesta'),
   #encuesta de satisfaccion al cliente 
   #path("encuesta_satifaccion_cliente/encuesta/<int:id_solicitud>/", views.encuesta_satisfaccion, name="Encuesta_satisfaccion_cliente"),
   path("encuesta_satifaccion_cliente/encuesta/", views.encuesta_satisfaccion, name="Encuesta_satisfaccion_cliente"),
   path("encuesta_satifaccion_cliente/gracias", views.encuesta_gracias, name="Encuesta_gracias"), 
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)