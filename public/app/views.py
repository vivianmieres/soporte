from django.shortcuts import render, redirect
#from .usuarioForm import UsuarioFormulario
from .forms import CargaUsuarioForm, CargaClienteForm, ModifUsuarioForm, ModifPasswordForm, CargaTipoEquipoForm
from .forms import CargaEquipoForm, CargaSolicitudForm, CargaEstadoForm
from . import models
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
# Create your views here.

def Login(request):
   if request.method=='POST':
        usuario=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=usuario,password=password)
        if user is not None:
            print(user.get_username())
            login(request, user)
            usuario=User.objects.get(username=user.get_username())
            if usuario.is_staff==True:
                #para redigir al admin si es administrador
                return redirect('admin:login')
            elif usuario.is_active:
                return redirect('Principal')
        else:
            messages.error (request, "Usuario o contraseña incorrecta")
            return redirect('login')
        
   return render(request,"login.html",{})


def Principal(request):
   context = {
      'titulo': "Principal"
   } 

   return render(request, 'principal.html', context)

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
         messages.error(request,"No se selecciono a un cliente")
   context = {
      'titulo'      : "Consulta de Usuario",
      'usuario'     : usuarios

   } 
   return render(request,"usuarioConsulta.html",context)

#Mantenimiento
def usuario_mante(request):
   form = CargaUsuarioForm(request.POST or None) 
   if request.method=="POST":
        if form.is_valid:    
            aux1 = form.data.get("username")
            print(aux1)
            print(form.data)
            form.save()
            return redirect('Usuario_consulta')
        else:
            form= CargaUsuarioForm()
            messages.error("No se guardaron los datos")        
            
   context = {
      'titulo': "Mantenimiento de Usuario",
      'form'  : form,
   } 
   return render(request,"baseMante.html",context)

#Modificacion
def usuario_mante_pk(request,pk): 
   usuario= models.AuthUser.objects.get(id = pk)
   form = ModifUsuarioForm(request.POST or None, instance = usuario) 
   if request.method=="POST": 
      if form.is_valid:    
         form.save()
         return redirect('usuario_consulta')
      else:
         form= ModifUsuarioForm(instance = usuario)     
         messages.error("No se guardaron los datos")   
   # elif request.method == "GET":
   #    redirect('Usuario_mante_pass')

   context = {
      'titulo': "Mantenimiento de Usuario",
      'form'  : form
   } 
   return render(request,"baseMante.html",context)

#Modificacion password
class usuario_mante_pass(PasswordChangeView):
    form_class = ModifPasswordForm
    success_url = '/'
    #success_url = reverse_lazy('Usuario_mante_pass')
    template_name = 'usuarioPass.html'

#MODULO CLIENTE
#Consulta
def cliente_consulta(request):
   clientes = []
   clientes = models.Cliente.objects.all()
  # tipo_busqueda = 
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
         pk_cliente = models.Cliente.objects.get(documento=cliente_seleccionado)
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
   form = CargaClienteForm(request.POST or None) 
   if request.method=="POST":
      if form.is_valid:    
         # aux1 = form.data.get("nombres")
         # aux2 = form.data.get("apellidos")
         # aux3 = form.data.get("documento")
         # print(aux1)
         # form_data = form.cleaned_data
         # print(form_data)
         form.save()
         return redirect('Cliente_consulta')
      else:
         form= CargaClienteForm()     
         messages.error("No se guardaron los datos")   
         # cliente = models.Cliente.objects.get(id_cliente= pk)
         # form = CargaClienteForm(request.GET)  

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
      if form.is_valid:    
         form.save()
         return redirect('Cliente_consulta')
      else:
         form= CargaClienteForm(instance = cliente)     
         messages.error("No se guardaron los datos")   

   context = {
      'titulo': "Mantenimiento de Cliente",
      'form'  : form
   } 
   return render(request,"baseMante.html",context)

#MODULO EQUIPO
def equipo(request):
   return render(request,"",{}) 

#Equipo
#Consulta
def equipo_consulta(request):
   equipo = []
   equipo = models.Equipo.objects.select_related('id_tipo_equipo').all()
   print(equipo)
   if request.method=="GET":
      busqueda = request.GET.get("buscar")
      print(busqueda)
      if busqueda:      
         equipo = (models.Equipo.objects.filter(caracteristicas__icontains = busqueda))
      print(equipo)
   elif request.method=="POST":
      equipo_seleccionado= request.POST.get("equipo_seleccionado",False)
      print(equipo_seleccionado)
      if equipo_seleccionado != False:
         pk_equipo = models.Equipo.objects.get(caracteristicas = equipo_seleccionado)
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
   form = CargaEquipoForm(request.POST or None) 
   if request.method=="POST":
      if form.is_valid:    
         aux1 = form.data.get("caracteristicas")
         print(aux1)
         # form_data = form.cleaned_data
         # print(form_data)
         form.save()
         return redirect('Equipo_consulta')
      else:
         form= CargaEquipoForm()     
         messages.error("No se guardaron los datos")    
   context = {
      'titulo': "Mantenimiento de Equipo",
      'form'  : form
   } 
   return render(request,"baseMante.html",context)

#Modificacion
def equipo_mante_pk(request,pk): 
   equipo = models.Equipo.objects.get(id_tipo_equipo = pk)
   form = CargaEquipoForm(request.POST or None, instance = equipo) 
   if request.method=="POST": 
      if form.is_valid:    
         form.save()
         return redirect('Equipo_consulta')
      else:
         form= CargaEquipoForm(instance = equipo)     
         messages.error("No se guardaron los datos")   

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
   form = CargaTipoEquipoForm(request.POST or None) 
   if request.method=="POST":
      if form.is_valid:    
         aux1 = form.data.get("descripcion")
         print(aux1)
         # form_data = form.cleaned_data
         # print(form_data)
         form.save()
         return redirect('Tipo_equipo_consulta')
      else:
         form= CargaTipoEquipoForm()     
         messages.error("No se guardaron los datos")    
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
      if form.is_valid:    
         form.save()
         return redirect('Tipo_equipo_consulta')
      else:
         form= CargaTipoEquipoForm(instance = tipo_equipo)     
         messages.error("No se guardaron los datos")   

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
         pk_solicitud = models.Solicitud.objects.get(descripcion= solicitud_seleccionado)
         print(pk_solicitud.id_solicitud)
         return redirect('Solicitud_mante_pk',pk=pk_solicitud.id_solicitud)
      else: 
         messages.error(request,"No se selecciono ninguna Solicitud")

   context = {
      'titulo'      : "Consulta de Solicitud",
      'solicitud'     : solicitud,
   } 
   return render(request,"SolicitudConsulta.html",context)

#Mantenimiento
def solicitud_mante(request): 
   form = CargaSolicitudForm(request.POST or None) 
   if request.method=="POST":
      if form.is_valid:    
         aux1 = form.data.get("descripcion")
         print(aux1)
         # form_data = form.cleaned_data
         # print(form_data)
         form.save()
         return redirect('Solicitud_consulta')
      else:
         form= CargaSolicitudForm()     
         messages.error("No se guardaron los datos")    
   context = {
      'titulo': "Mantenimiento de Solicitud",
      'form'  : form
   } 
   return render(request,"baseMante.html",context)

#Modificacion
def solicitud_mante_pk(request,pk): 
   solicitud = models.Solicitud.objects.get(id_solicitud = pk)
   form = CargaSolicitudForm(request.POST or None, instance = solicitud) 
   if request.method=="POST": 
      if form.is_valid:    
         form.save()
         return redirect('Solicitud_consulta')
      else:
         form= CargaSolicitudForm(instance = solicitud)     
         messages.error("No se guardaron los datos")   

   context = {
      'titulo': "Mantenimiento de Solicitud",
      'form'  : form
   } 
   return render(request,"baseMante.html",context)

#Estado
#Consulta
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
         pk_estado = models.Estado.objects.get(nombre = estado_seleccionado)
         print(pk_estado.id_estado)
         return redirect('Estado_mante_pk',pk=pk_estado.id_estado)
      else: 
         messages.error(request,"No se selecciono ninguna Solicitud")

   context = {
      'titulo'      : "Consulta de Estado",
      'estado'     : estado,
   } 
   return render(request,"EstadoConsulta.html",context)

#Mantenimiento
def estado_mante(request): 
   form = CargaEstadoForm(request.POST or None) 
   if request.method=="POST":
      if form.is_valid:    
         aux1 = form.data.get("nombre")
         print(aux1)
         # form_data = form.cleaned_data
         # print(form_data)
         form.save()
         return redirect('Estado_consulta')
      else:
         form= CargaEstadoForm()     
         messages.error("No se guardaron los datos")    
   context = {
      'titulo': "Mantenimiento de Estado de Solicitud",
      'form'  : form
   } 
   return render(request,"baseMante.html",context)

#Modificacion
def estado_mante_pk(request,pk): 
   estado = models.Estado.objects.get(id_estado = pk)
   form = CargaEstadoForm(request.POST or None, instance = estado) 
   if request.method=="POST": 
      if form.is_valid:    
         form.save()
         return redirect('Estado_consulta')
      else:
         form= CargaEstadoForm(instance = estado)     
         messages.error("No se guardaron los datos")   

   context = {
      'titulo': "Mantenimiento de Estado de Solicitud",
      'form'  : form
   } 
   return render(request,"baseMante.html",context)




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


