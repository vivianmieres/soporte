from django.shortcuts import render, redirect
#from .usuarioForm import UsuarioFormulario
from .forms import CargaUsuarioForm, CargaClienteForm, ModifUsuarioForm, ModifPasswordForm, CargaTipoEquipoForm
from .forms import CargaTelefonoForm, CargaPrestadoraForm, CargaCargoForm, CargaAsignarCargoForm, CargaSolicitudRepuestoAccForm
from .forms import CargaEquipoForm, CargaSolicitudForm, CargaEstadoForm, CargaTipoRepuestoAccForm, CargaRepuestoAccForm
from .forms import FiltroSolicitudForm, FiltroRepuestoAccForm
from . import models
from django.contrib import messages
from django.db.models import Q, Prefetch
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from datetime import datetime
from django.db import transaction
from django.shortcuts import get_object_or_404
# Create your views here.

def Login(request):
   if request.method=='POST':
        usuario=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=usuario,password=password)
        print(usuario)
        print(password)
        if user is not None:
            print(user.get_username())
            login(request, user)
            usuario=User.objects.get(username=user.get_username())
            #if usuario.is_staff==True:
                #para redigir al admin si es administrador
              #  return redirect('admin:login')
            #elif usuario.is_active:
            if usuario.is_active:
                return redirect('Principal')
            else:
               messages.error (request, "Usuario Inactivo")
               return redirect('Acceso')

        else:
            messages.error (request, "Usuario o contraseña incorrecta")
            return redirect('Acceso')
        
   return render(request,"login.html",{})


def Principal(request):
   # context = {
   #    'titulo': "Principal"
   # } 

   return render(request, 'principal.html', {})

#MODULO USUARIO
#Consulta
def usuario_consulta(request):
   usuarios = []
   usuarios = models.AuthUser.objects.all()
   if request.method=="GET":
        solicitud_busqueda = request.GET.get("buscar")
        print(solicitud_busqueda)
        if solicitud_busqueda:
            #busca por nombre, apellido
            usuarios = (models.AuthUser.objects.filter(username__icontains = solicitud_busqueda))
   elif request.method=="POST":
      user_seleccionado= request.POST.get("user_seleccionado",False)
      print(user_seleccionado)
      if user_seleccionado != False:
         pk_user = models.AuthUser.objects.get(username=user_seleccionado)
         print(pk_user.username)
         return redirect('Usuario_mante_pk',pk=pk_user.id)
      else: 
         messages.error(request,"No se selecciono a un Usuario")
   context = {
      'titulo'      : "Consulta de Usuario",
      'usuario'     : usuarios

   } 
   return render(request,"usuarioConsulta.html",context)

#Mantenimiento
def usuario_mante(request):
   if request.method=="POST":
      if 'Cancelar' in request.POST:
         return redirect('Usuario_consulta')

      form = CargaUsuarioForm(request.POST or None) 
      if form.is_valid():    
         username1 = form.data.get("username")
         print(username1)
         #username2 = form.cleaned_data.get("username")
         form.save()
         return redirect('Usuario_consulta')
      else:
         print(form.errors)     
   else:
      form = CargaUsuarioForm(request.POST or None)  

   context = {
      'titulo': "Mantenimiento de Usuario",
      'form'  : form,
   } 
   return render(request,"baseMante.html",context)

#Modificacion
def usuario_mante_pk(request,pk): 
   #usuario= models.AuthUser.objects.get(id = pk)
   usuario= User.objects.get(id = pk)
   form = ModifUsuarioForm(request.POST or None, instance = usuario) 
   if request.method=="POST": 
      if 'Cancelar' in request.POST:
         return redirect('Usuario_consulta')
      if form.is_valid():    
         form.save()
         return redirect('Usuario_consulta')
      else:   
         print(form.errors) 
        
   context = {
      'titulo': "Mantenimiento de Usuario",
      'form'  : form
   } 
   return render(request,"baseMante.html",context)


#Modificacion password
def usuario_pass(request):
   usuario_acual = request.user
   # if usuario_acual.is_superuser:
   #    return redirect('Usuario_consulta_pass')
     
   # else: 
   return redirect('Usuario_mante_pass_login')
   

def usuario_consulta_pass(request):
   usuarios = []
   usuarios = models.AuthUser.objects.all()
   if request.method=="GET":
        solicitud_busqueda = request.GET.get("buscar")
        print(solicitud_busqueda)
        if solicitud_busqueda:
            #busca por nombre, apellido
            usuarios = (models.AuthUser.objects.filter(username__icontains = solicitud_busqueda))
   elif request.method=="POST":
      user_seleccionado= request.POST.get("user_seleccionado",False)
      print(user_seleccionado)
      if user_seleccionado != False:
         pk_user = models.AuthUser.objects.get(username=user_seleccionado)
         print(pk_user.username)
         return redirect('Usuario_mante_pass')
      else: 
         messages.error(request,"No se selecciono a un Usuario")
   context = {
      'titulo'      : "Modificar contraseña de Usuario",
      'usuario'     : usuarios

   } 
   return render(request,"usuarioConsulta.html",context)   


def usuario_mante_pass(request, pk):
   usuario= models.AuthUser.objects.get(id = pk)
   if request.method == 'POST':
      if 'Cancelar' in request.POST:
         return redirect('Usuario_consulta_pass')
      form = PasswordChangeForm(usuario, request.POST)
      if form.is_valid():
         user = form.save()
         update_session_auth_hash(request, user)  # Mantiene la sesión activa
         messages.success(request, 'Tu contraseña ha sido cambiada con éxito.')
         return redirect('Usuario_consulta_pass')  # Redirige a la página de perfil u otra
      else:
         print(form.errors) 
   else:
      form = PasswordChangeForm(usuario, request.POST)

   context = {
      'titulo': "Modificar contraseña de Usuario",
      'form'  : form
   }

   return render(request,"baseMante.html",context)

@login_required
def usuario_mante_pass_login(request):
   if request.method == 'POST':
      if 'Cancelar' in request.POST:
         return redirect('Principal')
      print(request.user.username)
      form = PasswordChangeForm(request.user, request.POST)
      if form.is_valid():
         user = form.save()
         update_session_auth_hash(request, user)  # Mantiene la sesión activa
         messages.success(request, 'Tu contraseña ha sido cambiada con éxito.')
         return redirect('Principal')
      else:
         print(form.errors) 
   else:
      form = PasswordChangeForm(request.user)

   context = {
      'titulo': "Modificar contraseña de Usuario",
      'form'  : form
   }

   return render(request,"baseMante.html",context)

#Cargo
#Consulta Cargo
def cargo_consulta(request):
   cargo = []
   cargo = models.Cargo.objects.all().order_by('id_cargo')
   print(cargo)
   if request.method=="GET":
      busqueda = request.GET.get("buscar")
      print(busqueda)
      if busqueda:      
         cargo = (models.Cargo.objects.filter(cargo__icontains = busqueda))
      print(cargo)
   elif request.method=="POST":
      cargo_seleccionado= request.POST.get("cargo_seleccionado",False)
      print(cargo_seleccionado)
      if cargo_seleccionado != False:
         pk_cargo = models.Cargo.objects.get(id_cargo = cargo_seleccionado)
         print(pk_cargo.id_cargo)
         return redirect('Cargo_mante_pk',pk=pk_cargo.id_cargo)
      else: 
         messages.error(request,"No se selecciono ningun cargo")

   context = {
      'titulo'      : "Consulta de Cargo",
      'cargo'     : cargo,
   } 
   return render(request,"cargoConsulta.html",context)

#Mantenimiento cargo
def cargo_mante(request): 
   if request.method=="POST":
      if 'Cancelar' in request.POST:
         return redirect('Cargo_consulta')

      form = CargaCargoForm(request.POST or None)  
      if form.is_valid():    
         aux1 = form.data.get("cargo")
         print(aux1)
         form.save()
         return redirect('Cargo_consulta')
      else:
         print(form.errors)
   else:
      form = CargaCargoForm(request.POST or None) 

   context = {
      'titulo': "Mantenimiento de Cargo",
      'form'  : form
   } 
   return render(request,"baseMante.html",context)

#Modificacion cargo
def cargo_mante_pk(request,pk): 
   cargo = models.Cargo.objects.get(id_cargo = pk)
   form = CargaCargoForm(request.POST or None, instance = cargo) 
   if request.method=="POST": 
      if 'Cancelar' in request.POST:
         return redirect('Cargo_consulta')
      
      if form.is_valid():    
         form.save()
         return redirect('Cargo_consulta')
      else:
         print(form.errors)
        
   context = {
      'titulo': "Mantenimiento de Cargo",
      'form'  : form
   } 
   return render(request,"baseMante.html",context)


#Asignar cargo
#Consulta asignar cargo
def asignar_cargo_consulta(request):
   usuario_cargo = []
   usuario_cargo = models.Usuario_cargo.objects.all().order_by('id_usuario_cargo')
   print(usuario_cargo)
   if request.method=="GET":
      busqueda = request.GET.get("buscar")
      print(busqueda)
      if busqueda:      
         usuario_cargo = (models.Usuario_cargo.objects.filter(id__username__icontains = busqueda))
      print(usuario_cargo)
   elif request.method=="POST":
      usuario_cargo_seleccionado= request.POST.get("usuario_cargo_seleccionado",False)
      print(usuario_cargo_seleccionado)
      if usuario_cargo_seleccionado != False:
         pk_usuario_cargo = models.Usuario_cargo.objects.get(id_usuario_cargo = usuario_cargo_seleccionado)
         print(pk_usuario_cargo.id_usuario_cargo)
         return redirect('Asignar_cargo_mante_pk',pk=pk_usuario_cargo.id_usuario_cargo)
      else: 
         messages.error(request,"No se asignó ningún cargo al usuario")

   context = {
      'titulo'      : "Consulta de Asignación de Cargo",
      'usuario_cargo'     : usuario_cargo,
   } 
   return render(request,"asignarCargoConsulta.html",context)

#Mantenimiento asignar cargo
def asignar_cargo_mante(request): 
   if request.method=="POST":
      if 'Cancelar' in request.POST:
         return redirect('Asignar_cargo_consulta')

      form = CargaAsignarCargoForm(request.POST or None)  
      if form.is_valid():    
         #aux1 = form.data.get("cargo")
         #print(aux1)
         form.save()
         return redirect('Asignar_cargo_consulta')
      else:
         print(form.errors)
   else:
      form = CargaAsignarCargoForm(request.POST or None) 

   context = {
      'titulo': "Mantenimiento de asignación de Cargo a usuario",
      'form'  : form
   } 
   return render(request,"baseMante.html",context)

#Modificacion asignar cargo
def asignar_cargo_mante_pk(request,pk): 
   usuarioCargo = models.Usuario_cargo.objects.get(id_usuario_cargo = pk)
   form = CargaAsignarCargoForm(request.POST or None, instance = usuarioCargo) 
   if request.method=="POST": 
      if 'Cancelar' in request.POST:
         return redirect('Asignar_cargo_consulta')
      
      if form.is_valid():    
         form.save()
         return redirect('Asignar_cargo_consulta')
      else:
         print(form.errors)
        
   context = {
      'titulo': "Mantenimiento de Asignación de cargo",
      'form'  : form
   } 
   return render(request,"baseMante.html",context)

#MODULO CLIENTE
#Consulta
def cliente_consulta(request):
   clientes = []
   clientes = models.Cliente.objects.all()

   for cliente in clientes:
      cliente.telefono_principal = cliente.telefono_set.filter(activo=True, principal=True).first()
     
   if request.method=="GET":
        #tipo_busqueda = request.GET.get()
      busqueda = request.GET.get("buscar")
      print(busqueda)
        #if request.GET.nombre:
            #busca por nombre, apellido
      if busqueda:      
         clientes = (models.Cliente.objects.filter(nombres__icontains = busqueda) or
                     models.Cliente.objects.filter(apellidos__icontains = busqueda))
      #   else:
      #       #busca por documento
      #       usuarios = (models.Cliente.objects.filter( Q(nro_documento__icontains = busqueda)))
   elif request.method=="POST":
      cliente_seleccionado= request.POST.get("cliente_seleccionado",False)
      if cliente_seleccionado != False:
         pk_cliente = models.Cliente.objects.get(id_cliente = cliente_seleccionado)
         print(pk_cliente.id_cliente)
         return redirect('Cliente_mante_pk',pk=pk_cliente.id_cliente)
      else: 
         messages.error(request,"No se selecciono a un cliente")

   context = {
      'titulo'      : "Consulta de Cliente",
      'cliente'     : clientes,
      #'busqueda'    : tipo_busqueda

   } 
   return render(request,"clienteConsulta.html",context)

#Mantenimiento
def cliente_mante(request): 
   if request.method=="POST":
      if 'Cancelar' in request.POST:
         return redirect('Cliente_consulta')
      
      form = CargaClienteForm(request.POST or None) 
      if form.is_valid():    
         # aux1 = form.data.get("nombres")
         # aux2 = form.data.get("apellidos")
         # aux3 = form.data.get("documento")
         # print(aux1)
         # form_data = form.cleaned_data
         # print(form_data)
         form.save()
         return redirect('Cliente_consulta')
      else:
         print(form.errors) 
         #form= CargaClienteForm()     
         #messages.error("No se guardaron los datos")   
         # cliente = models.Cliente.objects.get(id_cliente= pk)
         # form = CargaClienteForm(request.GET)  
   else:
      form = CargaClienteForm(request.POST or None) 

   context = {
      'titulo': "Mantenimiento de Cliente",
      'form'  : form
   } 
   return render(request,"baseMante.html",context)

#Modificacion
def cliente_mante_pk(request,pk): 
   cliente= models.Cliente.objects.get(id_cliente = pk)
   form = CargaClienteForm(request.POST or None, instance = cliente) 
   if request.method=="POST": 
      if 'Cancelar' in request.POST:
         return redirect('Cliente_consulta')
      
      if form.is_valid():    
         form.save()
         return redirect('Cliente_consulta')
      else:
         print(form.errors)
         #form= CargaClienteForm(instance = cliente)     
         #messages.error("No se guardaron los datos")   

   context = {
      'titulo': "Mantenimiento de Cliente",
      'form'  : form
   } 
   return render(request,"baseMante.html",context)

#Telefono
#Consulta telefono
def telefono_consulta(request):
   telefonos = []
   telefonos = models.Telefono.objects.all().order_by('id_telefono')
   if request.method=="GET":
       
      busqueda = request.GET.get("buscar")
      print(busqueda)
        #if request.GET.nombre:
            #busca por nombre, apellido
      if busqueda:      
         telefonos = models.Telefono.objects.filter(Q(id_cliente__nombres__icontains=busqueda) |
                                                    Q(id_cliente__apellidos__icontains=busqueda) |
                                                    Q(prefijo__icontains=busqueda) |
                                                    Q(numero__icontains=busqueda)).order_by('id_telefono')
   elif request.method=="POST":
      telefono_seleccionado= request.POST.get("telefono_seleccionado",False)
      print(telefono_seleccionado)
      if telefono_seleccionado != False:
         pk_telefono = models.Telefono.objects.get(id_telefono = telefono_seleccionado)
         print(pk_telefono.id_telefono)
         return redirect('Telefono_mante_pk',pk=pk_telefono.id_telefono)
      else: 
         messages.error(request,"No se selecciono un telefono")

   context = {
      'titulo'      : "Consulta de telefono de Cliente",
      'telefono'     : telefonos,
   } 
   return render(request,"telefonoConsulta.html",context)  


#Mantenimiento telefono
def telefono_mante(request): 
   if request.method=="POST":
      if 'Cancelar' in request.POST:
         return redirect('Telefono_consulta')
      
      form = CargaTelefonoForm(request.POST or None) 
      if form.is_valid():    
         form.save()
         return redirect('Telefono_consulta')
      else:
         print(form.errors) 
   else:
      form = CargaTelefonoForm(request.POST or None) 

   context = {
      'titulo': "Mantenimiento de Telefonos de Cliente",
      'form'  : form
   } 
   return render(request,"baseMante.html",context)

#Modificacion telefono
def telefono_mante_pk(request,pk): 
   telefono = models.Telefono.objects.get(id_telefono = pk)
   form = CargaTelefonoForm(request.POST or None, instance = telefono) 
   if request.method=="POST": 
      if 'Cancelar' in request.POST:
         return redirect('Telefono_consulta')
      
      if form.is_valid():    
         form.save()
         return redirect('Telefono_consulta')
      else:
         print(form.errors)
        
   context = {
      'titulo': "Mantenimiento de Telefono de Cliente",
      'form'  : form
   } 
   return render(request,"baseMante.html",context)

#Prestadora
#Consulta prestadora
def prestadora_consulta(request):
   prestadora = []
   prestadora = models.Prestadora.objects.all().order_by('id_prestadora')
   print(prestadora)
   if request.method=="GET":
      busqueda = request.GET.get("buscar")
      print(busqueda)
      if busqueda:      
         prestadora = (models.Prestadora.objects.filter(empresa__icontains = busqueda))
      print(prestadora)
   elif request.method=="POST":
      prestadora_seleccionado= request.POST.get("prestadora_seleccionado",False)
      print(prestadora_seleccionado)
      if prestadora_seleccionado != False:
         pk_prestadora = models.Prestadora.objects.get(id_prestadora = prestadora_seleccionado)
         print(pk_prestadora.id_prestadora)
         return redirect('Prestadora_mante_pk',pk=pk_prestadora.id_prestadora)
      else: 
         messages.error(request,"No se selecciono ninguna operadora")

   context = {
      'titulo'      : "Consulta de Operadora",
      'prestadora'     : prestadora,
   } 
   return render(request,"prestadoraConsulta.html",context)


#Mantenimiento prestadora
def prestadora_mante(request): 
   if request.method=="POST":
      if 'Cancelar' in request.POST:
         return redirect('Prestadora_consulta')

      form = CargaPrestadoraForm(request.POST or None)  
      if form.is_valid():    
         aux1 = form.data.get("empresa")
         print(aux1)
         form.save()
         return redirect('Prestadora_consulta')
      else:
         print(form.errors)
   else:
      form = CargaPrestadoraForm(request.POST or None) 

   context = {
      'titulo': "Mantenimiento de Operadora",
      'form'  : form
   } 
   return render(request,"baseMante.html",context)

#Modificacion prestadora
def prestadora_mante_pk(request,pk): 
   prestadora = models.Prestadora.objects.get(id_prestadora = pk)
   form = CargaPrestadoraForm(request.POST or None, instance = prestadora) 
   if request.method=="POST": 
      if 'Cancelar' in request.POST:
         return redirect('Prestadora_consulta')
      
      if form.is_valid():    
         form.save()
         return redirect('Prestadora_consulta')
      else:
         print(form.errors)
        
   context = {
      'titulo': "Mantenimiento de Operadora",
      'form'  : form
   } 
   return render(request,"baseMante.html",context)
#MODULO EQUIPO
def equipo(request):
   return render(request,"",{}) 

#Equipo
#Consulta equipo
def equipo_consulta(request):
   equipo = []
   equipo = models.Equipo.objects.select_related('id_tipo_equipo','id_cliente').all()
   print(equipo)
   if request.method=="GET":
      busqueda = request.GET.get("buscar")
      print(busqueda)
      if busqueda:      
         equipo = models.Equipo.objects.filter(Q(id_tipo_equipo__descripcion__icontains=busqueda)|
                                               Q(marca__icontains=busqueda) | 
                                               Q(modelo__icontains=busqueda))
      print(equipo)
   elif request.method=="POST":
      equipo_seleccionado= request.POST.get("equipo_seleccionado",False)
      print(equipo_seleccionado)
      if equipo_seleccionado != False:
         pk_equipo = models.Equipo.objects.get(id_equipo = equipo_seleccionado)
         print(pk_equipo.id_equipo)
         return redirect('Equipo_mante_pk',pk=pk_equipo.id_equipo)
      else: 
         messages.error(request,"No se selecciono ningun equipo")

   context = {
      'titulo'      : "Consulta de Equipo",
      'equipo'     : equipo,
   } 
   return render(request,"equipoConsulta.html",context)

#Mantenimiento
def equipo_mante(request): 
   if request.method=="POST":
      if 'Cancelar' in request.POST:
         return redirect('Equipo_consulta')
      
      form = CargaEquipoForm(request.POST or None) 
      if form.is_valid():       
         aux1 = form.data.get("caracteristicas")
         print(aux1)
         # form_data = form.cleaned_data
         # print(form_data)
         form.save()
         return redirect('Equipo_consulta')
      else:
         print(form.errors)
         #form= CargaEquipoForm()     
         #messages.error("No se guardaron los datos") 
   else:
      form = CargaEquipoForm(request.POST or None)  

   context = {
      'titulo': "Mantenimiento de Equipo",
      'form'  : form
   } 
   return render(request,"baseMante.html",context)

#Modificacion
def equipo_mante_pk(request,pk): 
   equipo = models.Equipo.objects.get(id_equipo = pk)
   form = CargaEquipoForm(request.POST or None, instance = equipo) 
   if request.method=="POST": 
      if 'Cancelar' in request.POST:
         return redirect('Equipo_consulta')
       
      if form.is_valid():    
         form.save()
         return redirect('Equipo_consulta')
      else:
         print(form.errors)
         #form= CargaEquipoForm(instance = equipo)     
         #messages.error("No se guardaron los datos")   

   context = {
      'titulo': "Mantenimiento de Equipo",
      'form'  : form
   } 
   return render(request,"baseMante.html",context)


#Tipo equipo
#Consulta
def tipo_equipo_consulta(request):
   tipo_eq = []
   tipo_eq = models.Tipo_equipo.objects.all()
   print(tipo_eq)
   if request.method=="GET":
      busqueda = request.GET.get("buscar")
      print(busqueda)
      if busqueda:      
         tipo_eq = (models.Tipo_equipo.objects.filter(descripcion__icontains = busqueda))
      print(tipo_eq)
   elif request.method=="POST":
      tipo_eq_seleccionado= request.POST.get("tipo_eq_seleccionado",False)
      print(tipo_eq_seleccionado)
      if tipo_eq_seleccionado != False:
         pk_tipo_eq = models.Tipo_equipo.objects.get(descripcion= tipo_eq_seleccionado)
         print(pk_tipo_eq.id_tipo_equipo)
         return redirect('Tipo_equipo_mante_pk',pk=pk_tipo_eq.id_tipo_equipo)
      else: 
         messages.error(request,"No se selecciono ningun tipo de equipo")

   context = {
      'titulo'      : "Consulta de Tipo de Equipo",
      'tipo_equipo'     : tipo_eq,
   } 
   return render(request,"tipoEquipoConsulta.html",context)

#Mantenimiento
def tipo_equipo_mante(request): 
   if request.method=="POST":
      if 'Cancelar' in request.POST:
         return redirect('Tipo_equipo_consulta')

      form = CargaTipoEquipoForm(request.POST or None)  
      if form.is_valid():    
         aux1 = form.data.get("descripcion")
         print(aux1)
         # form_data = form.cleaned_data
         # print(form_data)
         form.save()
         return redirect('Tipo_equipo_consulta')
      else:
         print(form.errors)
         #form= CargaTipoEquipoForm()     
         #messages.error("No se guardaron los datos") 
   else:
      form = CargaTipoEquipoForm(request.POST or None) 

   context = {
      'titulo': "Mantenimiento de Tipo de Equipo",
      'form'  : form
   } 
   return render(request,"baseMante.html",context)

#Modificacion
def tipo_equipo_mante_pk(request,pk): 
   tipo_equipo = models.Tipo_equipo.objects.get(id_tipo_equipo = pk)
   form = CargaTipoEquipoForm(request.POST or None, instance = tipo_equipo) 
   if request.method=="POST": 
      if 'Cancelar' in request.POST:
         return redirect('Tipo_equipo_consulta')
      
      if form.is_valid():    
         form.save()
         return redirect('Tipo_equipo_consulta')
      else:
         print(form.errors)
         #form= CargaTipoEquipoForm(instance = tipo_equipo)     
         #messages.error("No se guardaron los datos")   

   context = {
      'titulo': "Mantenimiento de Tipo de Equipo",
      'form'  : form
   } 
   return render(request,"baseMante.html",context)


#MODULO SOLICITUD
def solicitud(request):
   return render(request,"",{}) 

#Solicitud
#Consulta
def solicitud_consulta(request):
   solicitud = []
   solicitud = models.Solicitud.objects.all()
   print(solicitud)
   if request.method=="GET":
      busqueda = request.GET.get("buscar")
      print(busqueda)
      if busqueda:      
         solicitud = (models.Solicitud.objects.filter(descripcion__icontains = busqueda))
      print(solicitud)
   elif request.method=="POST":
      solicitud_seleccionado= request.POST.get("solicitud_seleccionado",False)
      print(solicitud_seleccionado)
      if solicitud_seleccionado != False:
         pk_solicitud = models.Solicitud.objects.get(id_solicitud = solicitud_seleccionado)
         print(pk_solicitud.id_solicitud)
         return redirect('Solicitud_mante_pk',pk=pk_solicitud.id_solicitud)
      else: 
         messages.error(request,"No se selecciono ninguna Solicitud")

   context = {
      'titulo'      : "Consulta de Solicitud",
      'solicitud'     : solicitud,
   } 
   return render(request,"solicitudConsulta.html",context)

#Mantenimiento de solicitud
def solicitud_mante(request): 
   if request.method=="POST":
      if 'Cancelar' in request.POST:
         return redirect('Solicitud_consulta')

      form = CargaSolicitudForm(request.POST or None)
      cliente_form = CargaClienteForm(request.POST)  
      if 'GuardarCliente' in request.POST and cliente_form.is_valid():
         cliente_form.save()
         messages.success(request, "Cliente agregado correctamente.")
         return redirect('Solicitud_mante') 
      elif 'Guardar' in request.POST and form.is_valid():
            aux1 = form.data.get("descripcion")
            print(aux1)
            form.save()
            return redirect('Solicitud_consulta')
      else:
         print(form.errors, cliente_form.errors)    
   else:
      form = CargaSolicitudForm(request.POST or None) 
      cliente_form = CargaClienteForm(request.POST or None)

   context = {
      'titulo': "Mantenimiento de Solicitud",
      'form'  : form,
      'cliente_form' : cliente_form
   } 
   return render(request,"solicitudMante.html",context)

#Modificacion de solicitud
def solicitud_mante_pk(request,pk): 
   solicitud = models.Solicitud.objects.get(id_solicitud = pk)
   form = CargaSolicitudForm(request.POST or None, instance = solicitud) 
   if request.method=="POST": 
      if 'Cancelar' in request.POST:
         return redirect('Solicitud_consulta')
      
      if form.is_valid():    
         form.save()
         return redirect('Solicitud_consulta')
      else:
         print(form.errors)
         #form= CargaSolicitudForm(instance = solicitud)     
         #messages.error("No se guardaron los datos")   

   context = {
      'titulo': "Mantenimiento de Solicitud",
      'form'  : form
   } 
   return render(request,"baseMante.html",context)


#Asignacion de repuesto/accesorio en una solicitud
#Consulta de asignacion de repuesto/acc
def solicitud_repuesto_acc_consulta(request):
   solicitud_repuesto_acc = []
   solicitud_repuesto_acc = models.Solicitud_repuesto_acc.objects.select_related(
        "id_solicitud__id_equipo__id_cliente",
        "id_repuesto_acc__id_tipo_repuesto_acc"
    ).all()
   print(solicitud_repuesto_acc)
   if request.method=="GET":
      busqueda = request.GET.get("buscar")
      print(busqueda)
      if busqueda:      
         solicitud_repuesto_acc = solicitud_repuesto_acc.filter(
                Q(id_solicitud__id_equipo__id_cliente__nombres__icontains=busqueda) |
                Q(id_solicitud__id_equipo__id_cliente__apellidos__icontains=busqueda) |
                Q(id_repuesto_acc__marca__icontains=busqueda) |
                Q(id_repuesto_acc__descripcion__icontains=busqueda) |
                Q(id_repuesto_acc__id_tipo_repuesto_acc__nombre__icontains=busqueda)
         )
      print(solicitud_repuesto_acc)
   elif request.method=="POST":
      solicitud_repuesto_acc_seleccionado= request.POST.get("solicitud_repuesto_acc_seleccionado",False)
      print(solicitud_repuesto_acc_seleccionado)
      if solicitud_repuesto_acc_seleccionado != False:
         pk_solicitud_repuesto_acc = models.Solicitud_repuesto_acc.objects.get(id_solicitud_repuesto_acc = solicitud_repuesto_acc_seleccionado)
         print(pk_solicitud_repuesto_acc.id_solicitud_repuesto_acc)
         return redirect('Solicitud_repuesto_acc_mante_pk',pk=pk_solicitud_repuesto_acc.id_solicitud_repuesto_acc)
      else: 
         messages.error(request,"No se ha asignado ningun repuesto a la Solicitud")

   context = {
      'titulo'      : "Consulta de asignacion de repuesto/accesorio en una solicitud",
      'solicitud_repuesto_acc'     : solicitud_repuesto_acc,
   } 
   return render(request,"solicitudRepuestoAccConsulta.html",context)

#Mantenimiento de asignacion de repuesto/accesorio en una solicitud
def solicitud_repuesto_acc_mante(request): 
   if request.method=="POST":
      if 'Cancelar' in request.POST:
         return redirect('Solicitud_repuesto_acc_consulta')
      
      form = CargaSolicitudRepuestoAccForm(request.POST or None) 
      if form.is_valid():    
         aux1 = form.data.get("id_solicitud_repuesto_acc")
         print(aux1)
         with transaction.atomic():  # Para garantizar integridad
            solicitud_repuesto_acc = form.save(commit=False)
            repuesto = solicitud_repuesto_acc.id_repuesto_acc

            # Verificamos que haya stock disponible
            if repuesto.stock > 0:
               repuesto.stock -= 1
               repuesto.save()
               solicitud_repuesto_acc.save()
            else:
               form.add_error('id_repuesto_acc', 'No hay stock disponible de este repuesto/accesorio.')  
               context = {
                        'titulo': "Mantenimiento de asignación de repuesto/accesorio en una Solicitud",
                        'form': form
                    }
               return render(request, "baseMante.html", context) 
         return redirect('Solicitud_repuesto_acc_consulta')
      else:
         print(form.errors)
        
   else:
      form = CargaSolicitudRepuestoAccForm(request.POST or None) 

   context = {
      'titulo': "Mantenimiento de asignación de repuesto/accesorio en una Solicitud",
      'form'  : form
   }    
   return render(request,"baseMante.html",context)

#Modificacion de asignacion de respuesto/accesorio en una solicitud
def solicitud_repuesto_acc_mante_pk(request,pk): 
   solicitud_repuesto_acc = get_object_or_404(models.Solicitud_repuesto_acc, id_solicitud_repuesto_acc=pk)
   form = CargaSolicitudRepuestoAccForm(request.POST or None, instance = solicitud_repuesto_acc) 
   if request.method=="POST": 
      if 'Cancelar' in request.POST:
         return redirect('Solicitud_repuesto_acc_consulta')
      
      if form.is_valid():    
         with transaction.atomic():
            antiguo_repuesto = solicitud_repuesto_acc.id_repuesto_acc
            nueva_asignacion = form.save(commit=False)
            nuevo_repuesto = nueva_asignacion.id_repuesto_acc

            # Si cambió el repuesto
            if antiguo_repuesto != nuevo_repuesto:
              # Validamos que haya stock en el nuevo repuesto
               if nuevo_repuesto.stock > 0:
                  # Restamos del nuevo repuesto
                  nuevo_repuesto.stock -= 1
                  nuevo_repuesto.save()

                  # Sumamos al stock del repuesto anterior
                  antiguo_repuesto.stock += 1
                  antiguo_repuesto.save()

                  nueva_asignacion.save()
               else:
                  form.add_error('id_repuesto_acc', 'No hay stock disponible del nuevo repuesto/accesorio.')
                  context = {
                        'titulo': "Mantenimiento de asignación de repuesto/accesorio en una Solicitud",
                        'form': form
                  }
                  return render(request, "baseMante.html", context) 
            else:
               # Si no cambió el repuesto, solo se guarda
               nueva_asignacion.save()

         return redirect('Solicitud_repuesto_acc_consulta')
      else:
         print(form.errors)
        
   context = {
      'titulo': "Mantenimiento de asignación de repuesto/accesorio en una solicitud",
      'form'  : form
   } 
   return render(request,"baseMante.html",context)
#Estado
#Consulta de estado
def estado_consulta(request):
   estado = []
   estado = models.Estado.objects.all()
   print(estado)
   if request.method=="GET":
      busqueda = request.GET.get("buscar")
      print(busqueda)
      if busqueda:      
         estado = (models.Estado.objects.filter(nombre__icontains = busqueda))
      print(estado)
   elif request.method=="POST":
      estado_seleccionado= request.POST.get("estado_seleccionado",False)
      print(estado_seleccionado)
      if estado_seleccionado != False:
         pk_estado = models.Estado.objects.get(id_estado = estado_seleccionado)
         print(pk_estado.id_estado)
         return redirect('Estado_mante_pk',pk=pk_estado.id_estado)
      else: 
         messages.error(request,"No se selecciono tipo de estado de una solicitud")

   context = {
      'titulo'      : "Consulta de Tipo de estado",
      'estado'     : estado,
   } 
   return render(request,"estadoConsulta.html",context)

#Mantenimiento
def estado_mante(request): 
   if request.method=="POST":
      if 'Cancelar' in request.POST:
         return redirect('Estado_consulta')
      
      form = CargaEstadoForm(request.POST or None) 
      if form.is_valid():    
         aux1 = form.data.get("nombre")
         print(aux1)
         # form_data = form.cleaned_data
         # print(form_data)
         form.save()
         return redirect('Estado_consulta')
      else:
         print(form.errors)
         #form= CargaEstadoForm()     
         #messages.error("No se guardaron los datos")  
   else:
      form = CargaEstadoForm(request.POST or None) 

   context = {
      'titulo': "Mantenimiento de Tipo de estado de Solicitud",
      'form'  : form
   } 
   return render(request,"baseMante.html",context)

#Modificacion
def estado_mante_pk(request,pk): 
   estado = models.Estado.objects.get(id_estado = pk)
   form = CargaEstadoForm(request.POST or None, instance = estado) 
   if request.method=="POST": 
      if 'Cancelar' in request.POST:
         return redirect('Estado_consulta')
       
      if form.is_valid():    
         form.save()
         return redirect('Estado_consulta')
      else:
         print(form.errors)
         #form= CargaEstadoForm(instance = estado)     
         #messages.error("No se guardaron los datos")   

   context = {
      'titulo': "Mantenimiento de Tipo de estado de Solicitud",
      'form'  : form
   } 

   return render(request,"baseMante.html",context)

# MODULO REPUESTO ACCESORIO
def respuesto_acc(request):
   return render(request,"",{}) 

#Repuesto accesorio
#Consulta de repuesto accesorio
def repuesto_acc_consulta(request):
   repuesto_acc = []
   repuesto_acc = models.Repuesto_accesorio.objects.all()
   print(repuesto_acc)
   if request.method=="GET":
      busqueda = request.GET.get("buscar")
      print(busqueda)
      if busqueda:      
         repuesto_acc = models.Repuesto_accesorio.objects.filter(Q(id_tipo_repuesto_acc__nombre__icontains = busqueda)|
                                                                  Q(marca__icontains = busqueda)|
                                                                  Q(descripcion__icontains = busqueda))
      print(repuesto_acc)
   elif request.method=="POST":
      repuesto_acc_seleccionado= request.POST.get("repuesto_acc_seleccionado",False)
      print(repuesto_acc_seleccionado)
      if repuesto_acc_seleccionado != False:
         pk_repuesto_acc = models.Repuesto_accesorio.objects.get(id_repuesto_acc = repuesto_acc_seleccionado)
         print(pk_repuesto_acc.id_repuesto_acc)
         return redirect('Repuesto_acc_mante_pk',pk=pk_repuesto_acc.id_repuesto_acc)
      else: 
         messages.error(request,"No se selecciono ningun respuesto/accesorio")

   context = {
      'titulo'           : "Consulta de Respuesto/Accesorio",
      'repuesto_acc'     : repuesto_acc,
   } 
   return render(request,"repuestoAccConsulta.html",context)

#Mantenimiento repuesto accesorio
def repuesto_acc_mante(request): 
   if request.method=="POST":
      if 'Cancelar' in request.POST:
         return redirect('Repuesto_acc_consulta')
      
      form = CargaRepuestoAccForm(request.POST or None) 
      if form.is_valid():    
         aux1 = form.data.get("nombre")
         print(aux1)
         with transaction.atomic():  # Para garantizar integridad
            solicitud_repuesto_acc = form.save(commit=False)
            repuesto = solicitud_repuesto_acc.id_repuesto_acc

            # Verificamos que haya stock disponible
            if repuesto.stock > 0:
               repuesto.stock -= 1
               repuesto.save()
               solicitud_repuesto_acc.save()
            else:
               form.add_error('id_repuesto_acc', 'No hay stock disponible de este repuesto/accesorio.')  
               context = {
                        'titulo': "Mantenimiento de asignación de repuesto/accesorio en una Solicitud",
                        'form': form
                    }
               return render(request, "baseMante.html", context)
         return redirect('Repuesto_acc_consulta')
      else:
         print(form.errors) 
   else:
      form = CargaRepuestoAccForm(request.POST or None) 

   context = {
      'titulo': "Mantenimiento de Repuesto y Accesorio",
      'form'  : form
   } 
   return render(request,"baseMante.html",context)

#Modificacion repuesto accesorio
def repuesto_acc_mante_pk(request,pk): 
   repuesto_acc = models.Repuesto_accesorio.objects.get(id_repuesto_acc = pk)
   form = CargaRepuestoAccForm(request.POST or None, instance = repuesto_acc) 
   if request.method=="POST": 
      if 'Cancelar' in request.POST:
         return redirect('Repuesto_acc_consulta')
      
      if form.is_valid():    
         with transaction.atomic():
            antiguo_repuesto = solicitud_repuesto_acc.id_repuesto_acc
            nueva_asignacion = form.save(commit=False)
            nuevo_repuesto = nueva_asignacion.id_repuesto_acc

            # Si cambió el repuesto
            if antiguo_repuesto != nuevo_repuesto:
              # Validamos que haya stock en el nuevo repuesto
               if nuevo_repuesto.stock > 0:
                  # Restamos del nuevo repuesto
                  nuevo_repuesto.stock -= 1
                  nuevo_repuesto.save()

                  # Sumamos al stock del repuesto anterior
                  antiguo_repuesto.stock += 1
                  antiguo_repuesto.save()

                  nueva_asignacion.save()
               else:
                  form.add_error('id_repuesto_acc', 'No hay stock disponible del nuevo repuesto/accesorio.')
                  context = {
                        'titulo': "Mantenimiento de asignación de repuesto/accesorio en una Solicitud",
                        'form': form
                  }
                  return render(request, "baseMante.html", context) 
            else:
               # Si no cambió el repuesto, solo se guarda
               nueva_asignacion.save()

         return redirect('Repuesto_acc_consulta')
      else:
         print(form.errors)
   context = {
      'titulo': "Mantenimiento de Repuesto y Accesorio",
      'form'  : form
   } 
   return render(request,"baseMante.html",context)


#tipo repuesto acc
#Consulta de tipo repuesto acc
def tipo_repuesto_acc_consulta(request):
   tipo_repuesto_acc = []
   tipo_repuesto_acc = models.Tipo_repuesto_acc.objects.all()
   print(tipo_repuesto_acc)
   if request.method=="GET":
      busqueda = request.GET.get("buscar")
      print(busqueda)
      if busqueda:      
         tipo_repuesto_acc = (models.Tipo_repuesto_acc.objects.filter(nombre__icontains = busqueda))
      print(tipo_repuesto_acc)
   elif request.method=="POST":
      tipo_repuesto_acc_seleccionado= request.POST.get("tipo_repuesto_acc_seleccionado",False)
      print(tipo_repuesto_acc_seleccionado)
      if tipo_repuesto_acc_seleccionado != False:
         pk_tipo_repuesto_acc = models.Tipo_repuesto_acc.objects.get(id_tipo_repuesto_acc = tipo_repuesto_acc_seleccionado)
         print(pk_tipo_repuesto_acc.id_tipo_repuesto_acc)
         return redirect('Tipo_repuesto_acc_mante_pk',pk=pk_tipo_repuesto_acc.id_tipo_repuesto_acc)
      else: 
         messages.error(request,"No se selecciono ningun tipo de repuesto/accesorio")

   context = {
      'titulo'                : "Consulta de Tipo de Repuesto/Accesorio",
      'tipo_repuesto_acc'     : tipo_repuesto_acc,
   } 
   return render(request,"tipoRepuestoAccConsulta.html",context)

#Mantenimiento de tipo repuesto acc
def tipo_repuesto_acc_mante(request): 
   if request.method=="POST":
      if 'Cancelar' in request.POST:
         return redirect('Tipo_repuesto_acc_consulta')
      
      form = CargaTipoRepuestoAccForm(request.POST or None) 
      if form.is_valid():    
         aux1 = form.data.get("nombre")
         print(aux1)
         # form_data = form.cleaned_data
         # print(form_data)
         form.save()
         return redirect('Tipo_repuesto_acc_consulta')
      else:
         print(form.errors)
         #form= CargaTipoRepuestoAccForm()     
         #messages.error("No se guardaron los datos")   
   else:
      form = CargaTipoRepuestoAccForm(request.POST or None) 

   context = {
      'titulo': "Mantenimiento de Tipo de Repuesto y Accesorio",
      'form'  : form
   } 
   return render(request,"baseMante.html",context)

#Modificacion tipo de repuesto acc
def tipo_repuesto_acc_mante_pk(request,pk): 
   tipo_repuesto_acc = models.Tipo_repuesto_acc.objects.get(id_tipo_repuesto_acc = pk)
   form = CargaTipoRepuestoAccForm(request.POST or None, instance = tipo_repuesto_acc) 

   # Deshabilitar el campo 'cant' para que no se pueda modificar
   form.fields['cant'].disabled = True

   if request.method=="POST": 
      if 'Cancelar' in request.POST:
         return redirect('Tipo_repuesto_acc_consulta')
      
      if form.is_valid():    
         form.save()
         return redirect('Tipo_repuesto_acc_consulta')
      else:
         print(form.errors)
         #form= CargaTipoRepuestoAccForm(instance = tipo_repuesto_acc)     
         #messages.error("No se guardaron los datos")   

   context = {
      'titulo': "Mantenimiento de tipo de Repuesto y Accesorio",
      'form'  : form
   } 
   return render(request,"baseMante.html",context)

#REPORTES
#Reporte de solicitud
def solicitud_reporte(request):
   form = FiltroSolicitudForm(request.GET or None)
   solicitudes = models.Solicitud.objects.select_related(
        "id_equipo__id_cliente",
        "id_equipo__id_tipo_equipo",
        "id_estado"
   )

   if form.is_valid():
      cd = form.cleaned_data
      if cd['desde']:
         solicitudes = solicitudes.filter(fecha_ingreso__gte=cd['desde'])
      if cd['hasta']:
         solicitudes = solicitudes.filter(fecha_ingreso__lte=cd['hasta'])
      if cd['cliente']:
         solicitudes = solicitudes.filter(
            Q(id_equipo__id_cliente__nombres__icontains=cd['cliente']) |
            Q(id_equipo__id_cliente__apellidos__icontains=cd['cliente'])
         )
      if cd['estado']:
         solicitudes = solicitudes.filter(id_estado=cd['estado'])
   
   # Ordenar por ID
   solicitudes = solicitudes.order_by("id_solicitud")

   if 'generar_pdf' in request.GET:
      template = get_template("solicitudReporte.html")
      html = template.render({"solicitudes": solicitudes})
      response = HttpResponse(content_type='application/pdf')
      response['Content-Disposition'] = 'attachment; filename="reporte_solicitudes.pdf"'
      pisa.CreatePDF(html, dest=response)
      return response
      
   context = {
      'titulo': "Reporte de solicitudes en PDF",
      'form'  : form,
      'solicitudes': solicitudes
   } 

   return render(request, "solicitudFiltro.html", context)

#Inventario de repuesto/accesorio
def repuesto_acc_inventario(request):
   form = FiltroRepuestoAccForm(request.GET or None)
   repuestos = models.Repuesto_accesorio.objects.select_related("id_tipo_repuesto_acc")

   if form.is_valid():
      cd = form.cleaned_data
      if cd["tipo"]:
         repuestos = repuestos.filter(id_tipo_repuesto_acc=cd["tipo"])
      if cd["marca"]:
         repuestos = repuestos.filter(marca__icontains=cd["marca"])

   # Ordenar por ID
   repuestos = repuestos.order_by("id_repuesto_acc")
      
   if 'generar_pdf' in request.GET:
      template = get_template("repuestoAccInventario.html")
      html = template.render({
        "repuestos": repuestos,
        "fecha_actual": datetime.now().strftime("%d/%m/%Y %I:%M %p")  # ejemplo: 14/05/2025 10:45 AM
      })
      response = HttpResponse(content_type='application/pdf')
      response['Content-Disposition'] = 'attachment; filename="inventario_repuestos_acc.pdf"'
      pisa.CreatePDF(html, dest=response)
      return response
      
   context = {
      'titulo': "Inventario de Repuestos/Accesorios en PDF",
      'form'  : form,
      'repuestos': repuestos
   } 

   return render(request, "repuestoAccFiltro.html", context)



""" def usuario_mante_pass(request,pk):
   usuario= models.AuthUser.objects.get(id = pk)
   form = ModifPasswordForm(request.POST or None) 
   if request.method=="POST":
      if form.is_valid:    
         form.save()
         return redirect('Acceso')
      else:
         form= ModifPasswordForm()     
         messages.error("No se guardaron los datos")   
         
   context = {
      'titulo': "Modificacion de Contraseña",
      'form'  : form
   } 
   return render(request,"usuarioPass.html",context)    """

""" def usuario_mante_pass(ModifPasswordForm):
   form_class = ModifPasswordForm
   success_url = reverse_lazy('home')
   template_name = 'usuarioPass.html' """


""" @login_required
def usuario_mante_pass(request):
   form = ModifPasswordForm(user=request.user, data=request.POST or None)
   if form.is_valid():
     form.save()
     update_session_auth_hash(request, form.user)
     return redirect('Acceso')
   
   context = {
      'titulo': "Modificacion de Contraseña",
      'form'  : form
   } 
   return render(request, 'usuarioPass.html', context) """