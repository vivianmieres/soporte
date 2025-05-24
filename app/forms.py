from .models import Tipo_equipo, Cliente, Equipo, Estado, Solicitud,Telefono, Prestadora, Cargo, Usuario_cargo
from .models import Tipo_repuesto_acc, Repuesto_accesorio, Solicitud_repuesto_acc
from django import forms
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, ReadOnlyPasswordHashField
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django_select2.forms import ModelSelect2Widget
import datetime
from django.db.models import Q
from django.forms import DateInput

#Mantenimiento usuario
class CargaUsuarioForm(UserCreationForm,forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({
            'class':'form-control'
        })
        self.fields["first_name"].widget.attrs.update({
            'class':'form-control'
        })
        self.fields["last_name"].widget.attrs.update({
            'class':'form-control'
        })
        self.fields["email"].widget.attrs.update({
            'class':'form-control'
        })

    class Meta:
        model= User
        fields= ["username","first_name","last_name", "email","is_staff","is_active","is_superuser","password1","password2"]

        widgets ={
            'is_superuser': forms.CheckboxInput(attrs={'class':'checkboxInvoice'}),
            'is_staff': forms.CheckboxInput(attrs={'class':'checkboxInvoice'}),
            'is_active': forms.CheckboxInput(attrs={'class':'checkboxInvoice'})
        } 
    
    def clean_username(self):
        username = self.cleaned_data.get("username")
        
        if len(username) < 5:
            raise forms.ValidationError("El nombre de usuario debe tener al menos 5 caracteres.")
        return username   
		
    def validacion(self):
        username = self.cleaned_data.get("username")

        if username == "" or username == None:
            raise forms.ValidationError("El campo Nombre de Usuario no puede quedar vacio")
        
#Modificacion usuario
class ModifUsuarioForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({
            'class':'form-control'
        })
        self.fields["first_name"].widget.attrs.update({
            'class':'form-control'
        })
        self.fields["last_name"].widget.attrs.update({
            'class':'form-control'
        })
        self.fields["email"].widget.attrs.update({
            'class':'form-control'
        })

        self.fields.pop('password', None)

    class Meta:
        model= User
        fields= ["username","first_name","last_name", "email","is_staff","is_active","is_superuser"]

    widgets ={
            'is_superuser': forms.CheckboxInput(attrs={'class':'checkboxInvoice'}),
            'is_staff': forms.CheckboxInput(attrs={'class':'checkboxInvoice'}),
            'is_active': forms.CheckboxInput(attrs={'class':'checkboxInvoice'})
    }    



#Modificacion password usuario
class ModifPasswordForm(PasswordChangeForm): 
    class Meta:
        model= User
        
""" class usuario_mante_pass(PasswordChangeView):
    form_class = ModifPasswordForm
    success_url = reverse_lazy('Acceso')
    template_name = 'usuarioPass.html'   """      

#Widget de un cliente
class ClienteWidget(ModelSelect2Widget):
    model = Cliente
    search_fields = [
        "nombres__icontains",
        "apellidos__icontains",
    ]

    def label_from_instance(self, obj):
        return f"{obj.apellidos}, {obj.nombres}"
		
#Mantenimiento cliente
class CargaClienteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["nombres"].widget.attrs.update({
            'class':'form-control'
        })
        self.fields["apellidos"].widget.attrs.update({
            'class':'form-control'
        })
        self.fields["documento"].widget.attrs.update({
            'class':'form-control'
        })
        self.fields["nacionalidad"].widget.attrs.update({
            'class':'form-control'
        })
        self.fields["email"].widget.attrs.update({
            'class':'form-control'
        })
        self.fields["fecha_nacimiento"].widget.attrs.update({
            'class':'form-control'
        })
        self.fields["direccion"].widget.attrs.update({
            'class':'form-control'
        })
    class Meta:
        model= Cliente
        fields= ["id_cliente","nombres","apellidos","documento","nacionalidad","email","fecha_nacimiento","direccion"]

        widgets ={
            #'documento'        : forms.NumberInput(),
            'fecha_nacimiento' : forms.DateInput(attrs={'type':'date'})
        }

    def validacion(self):
        nombre = self.cleaned_data.get("nombres")
        if nombre == "" or nombre == None:
            raise forms.ValidationError("El campo Nombres no puede quedar vacio")

        apellido = self.cleaned_data.get("apellidos")
        if apellido == "" or apellido == None:
            raise forms.ValidationError("El campo Apellidos no puede quedar vacio")   

        documento = self.cleaned_data.get("documento")
        if documento == "" or documento == None:
            raise forms.ValidationError("El campo Documento no puede quedar vacio") 
        
        nacionalidad = self.cleaned_data.get("nacionalidad")
        if nacionalidad == "" or nacionalidad == None:
            raise forms.ValidationError("El campo Nacionalidad no puede quedar vacio")

#Mantenimiento telefono        
class CargaTelefonoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        id_prestadora = forms.ModelChoiceField(queryset= Prestadora.objects.all())
        self.fields["id_prestadora"].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields["prefijo"].widget.attrs.update({
            'class':'form-control'
        })
        self.fields["numero"].widget.attrs.update({
            'class':'form-control'
        })
      
    class Meta:
        model= Telefono
        fields= ["id_telefono","id_cliente","id_prestadora","prefijo","numero","principal","activo"]
        
        widgets ={
       'id_cliente': ClienteWidget(attrs={'class': 'form-control select2-custom'}), 
       'principal': forms.CheckboxInput(attrs={'class':'checkboxInvoice'}),
       'activo': forms.CheckboxInput(attrs={'class':'checkboxInvoice'})
        } 

        labels = {
            'id_cliente'    : 'Cliente',
            'id_prestadora' : 'Operadora'
        }    

    def validacion(self):
        Cliente = self.cleaned_data.get("id_cliente")
        if Cliente == None:
            raise forms.ValidationError("El campo Cliente no puede quedar vacio")  

        Prestadora = self.cleaned_data.get("id_prestadora")
        if Prestadora == None:
            raise forms.ValidationError("El campo Operadora no puede quedar vacio")   
    
        prefijo = self.cleaned_data.get("prefijo")
        if prefijo == "" or prefijo == None:
            raise forms.ValidationError("El campo Prefijo no puede quedar vacio")  
         
        numero = self.cleaned_data.get("numero")
        if numero == "" or numero == None:
            raise forms.ValidationError("El campo Numero no puede quedar vacio")   

    def clean(self):
        cleaned_data = super().clean()
        cliente = cleaned_data.get("id_cliente")
        principal = cleaned_data.get("principal")

        if principal and cliente:
            # Filtrar otros teléfonos principales para el mismo cliente
            qs = Telefono.objects.filter(id_cliente=cliente, principal=True)

            # Si estamos editando un teléfono, excluir el mismo
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise forms.ValidationError("Ya existe un teléfono principal para este cliente.")
        
#Mantenimiento prestadora        
class CargaPrestadoraForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["empresa"].widget.attrs.update({
            'class':'form-control'
        })
            
    class Meta:
        model= Prestadora
        fields= ["empresa","activo"]
        error_messages = {
            "empresa": { "unique": "Esta empresa ya se cargo anteriormente."}
        }        

    widgets ={
             'activo': forms.CheckboxInput(attrs={'class':'checkboxInvoice'})
        }    

    def validacion(self):
        empresa = self.cleaned_data.get("empresa")
        if empresa == "" or empresa == None:
            raise forms.ValidationError("El campo Empresa no puede quedar vacio")        
                   
#Mantenimiento tipo equipo        
class CargaTipoEquipoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["descripcion"].widget.attrs.update({
            'class':'form-control'
        })
        # self.fields["activo"].widget.attrs.update({
        #     'class':'form-control'
        # })
    class Meta:
        model= Tipo_equipo
        fields= ["id_tipo_equipo","descripcion","activo"]

    widgets ={
             'activo': forms.CheckboxInput(attrs={'class':'checkboxInvoice'})
         }    

    def validacion(self):
        descrip = self.cleaned_data.get("descripcion")
        if descrip == "" or descrip == None:
            raise forms.ValidationError("El campo Descripcion no puede quedar vacio")
        
#Mantenimiento equipo 
class CargaEquipoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        id_tipo_equipo = forms.ModelChoiceField(queryset= Tipo_equipo.objects.all())

        self.fields["id_tipo_equipo"].widget.attrs.update({
            'class':'form-control'
        })
        
        self.fields["descripcion"].widget.attrs.update({
            'class':'form-control'
        })
        self.fields["marca"].widget.attrs.update({
            'class':'form-control'
        })
        self.fields["modelo"].widget.attrs.update({
            'class':'form-control'
        })
        self.fields["serie"].widget.attrs.update({
            'class':'form-control'
        })
    class Meta:
        model= Equipo
        fields= ["id_equipo","id_cliente","id_tipo_equipo","descripcion","marca","modelo","serie"]
        
        widgets ={
       'id_cliente': ClienteWidget(attrs={'class': 'form-control select2-custom'})
        }  

        labels = {
            'id_cliente'    : 'Cliente',
            'id_tipo_equipo': 'Tipo de equipo'
        }    


    def validacion(self):
        Cliente = self.cleaned_data.get("id_cliente")
        if Cliente == None:
            raise forms.ValidationError("El campo Cliente no puede quedar vacio")  

        tipo_equip = self.cleaned_data.get("id_tipo_equipo")
        if tipo_equip == None:
            raise forms.ValidationError("El campo Tipo Equipo no puede quedar vacio")   
    
        caract = self.cleaned_data.get("descripcion")
        if caract == "" or caract == None:
            raise forms.ValidationError("El campo Descripción no puede quedar vacio")    
#Mantenimiento estado
class CargaEstadoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["nombre"].widget.attrs.update({
            'class':'form-control'
        })
        self.fields["descripcion"].widget.attrs.update({
            'class':'form-control'
        })
       
    class Meta:
        model= Estado
        fields= ["nombre","descripcion","activo"]

    widgets ={
             'activo': forms.CheckboxInput(attrs={'class':'checkboxInvoice'})
        }    

    def validacion(self):
        descrip = self.cleaned_data.get("nombre")
        if descrip == "" or descrip == None:
            raise forms.ValidationError("El campo Nombre no puede quedar vacio")

#widget del equipo de un cliente
class EquipoWidget(ModelSelect2Widget):
    model = Equipo
    search_fields = [
        "id_cliente__nombres__icontains",
        "id_cliente__apellidos__icontains",
        "id_tipo_equipo__descripcion",
    ]

    def label_from_instance(self, obj):
        return f"{obj.id_cliente.nombres} {obj.id_cliente.apellidos}-{obj.id_tipo_equipo.descripcion} {obj.marca} {obj.modelo}"

#Mantenimiento solicitud
class CargaSolicitudForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['id_equipo'].widget.attrs.update({
            'class': 'form-control select2-custom'
        })

        #filtrar los estados activos y ordenar por id_estado
        self.fields["id_estado"].queryset = Estado.objects.filter(activo=True).order_by('id_estado')

        #mostrar id-nombre
        self.fields["id_estado"].label_from_instance = lambda obj: f"{obj.id_estado} - {obj.nombre}"

        #Seleccionar por defecto estado "Abierto"
        estado_abierto = Estado.objects.filter(nombre__iexact="Abierto", activo=True).first()
        if estado_abierto:
            self.fields["id_estado"].initial = estado_abierto.id_estado

        #Fecha de hoy por defecto para fecha de ingreso
        self.fields["fecha_ingreso"].initial = datetime.date.today()    

        # Filtrar solo los usuarios con cargo 'Técnico' y que estén activos
        cargo_tecnico = Cargo.objects.filter(cargo__iexact="Técnico").first()
   
        if cargo_tecnico:
            self.fields["id_usuario_cargo"].queryset = Usuario_cargo.objects.filter(
            id_cargo=cargo_tecnico.id_cargo, activo=True).select_related('id')  # optimiza las consultas al traer datos del usuario

            # Mostrar nombre de usuario en el desplegable
            self.fields["id_usuario_cargo"].label_from_instance = lambda obj: f"{obj.id.username} ({obj.id.first_name} {obj.id.last_name})"
        else:
            self.fields["id_usuario_cargo"].queryset = Usuario_cargo.objects.none()

      
        #Estilos de boostrap
        self.fields["id_estado"].widget.attrs.update({
            'class': 'form-control'
        })

        self.fields["descripcion"].widget.attrs.update({
            'class':'form-control'
        })
        self.fields["fecha_ingreso"].widget.attrs.update({
            'class': 'form-control datepicker',
            'autocomplete': 'off',
            'placeholder': 'dd/mm/yyyy'
        })
        self.fields["fecha_cierre"].widget.attrs.update({
            'class': 'form-control datepicker',
            'autocomplete': 'off',
            'placeholder': 'dd/mm/yyyy'
        })
        self.fields["id_usuario_cargo"].widget.attrs.update({
            'class':'form-control'
        })

    
    class Meta:
        model= Solicitud
        fields= ["id_equipo","id_estado","descripcion","fecha_ingreso","fecha_cierre","id_usuario_cargo"]
        widgets = {
            'id_equipo': EquipoWidget,
            'fecha_ingreso': DateInput(format='%d/%m/%Y'),
            'fecha_cierre': DateInput(format='%d/%m/%Y'),
        } 
        labels = {
            'id_equipo': 'Equipo de un Cliente',
            'id_estado': 'Tipo de estado',
            'id_usuario_cargo': 'Técnico'
        }    

    def validacion(self):
        equipo = self.cleaned_data.get("id_equipo")
        if equipo == None:
            raise forms.ValidationError("El campo Equipo no puede quedar vacio")   
    
        estado = self.cleaned_data.get("id_estado")
        if estado == None:
            raise forms.ValidationError("El campo Estado no puede quedar vacio") 
        
        descripcion = self.cleaned_data.get("descripcion")
        if descripcion == None:
            raise forms.ValidationError("El campo Descripcion no puede quedar vacio") 
			
    def clean(self):
        cleaned_data = super().clean()
        estado = cleaned_data.get("id_estado")
        fecha_cierre = cleaned_data.get("fecha_cierre")
        tecnico = cleaned_data.get("id_usuario_cargo")

        # Verificamos si el estado se llama 'Cerrado'
        if estado and estado.nombre.lower() != 'cerrado' and fecha_cierre:
            raise forms.ValidationError("La fecha de cierre solo se puede completar si el estado es 'Cerrado'.")
        
        # Si está en 'Cerrado' pero no tiene fecha de cierre, podría obligarlo
        if estado and estado.nombre.lower() == 'cerrado' and not fecha_cierre:
            raise forms.ValidationError("Debe completar la fecha de cierre para un estado 'Cerrado'.")
        
        # Si estado es Cerrado y no hay fecha de cierre, asignar fecha actual
        if estado and estado.nombre.lower() == 'cerrado':
            if not fecha_cierre:
                cleaned_data["fecha_cierre"] = datetime.date.today()
        elif fecha_cierre:
            # Si estado no es Cerrado pero hay fecha de cierre, lanzar error
            raise forms.ValidationError("La fecha de cierre solo se puede completar si el estado es 'Cerrado'.")
        
        # Validar que técnico sea obligatorio si el estado es 'Diagnóstico y presupuesto' (id_estado == 2)
        if estado and estado.id_estado == 2 and not tecnico:
            self.add_error('id_usuario_cargo', "Debe asignar un técnico cuando el estado es 'Diagnóstico y presupuesto'.")

        return cleaned_data



#Mantenimiento tipo repuesto accesorio        
class CargaTipoRepuestoAccForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       
        self.fields["nombre"].widget.attrs.update({
            'class':'form-control'
        })
      
    class Meta:
        model= Tipo_repuesto_acc
        fields= ["nombre","activo"]
 
    widgets ={
             'activo': forms.CheckboxInput(attrs={'class':'checkboxInvoice'})
        }  

    def validacion(self):
        descrip = self.cleaned_data.get("nombre")
        if descrip == "" or descrip == None:
            raise forms.ValidationError("El campo Nombre no puede quedar vacio")  
#Mantenimiento repuesto accesorio        
class CargaRepuestoAccForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       
        id_tipo_repuesto_acc = forms.ModelChoiceField(queryset= Tipo_repuesto_acc.objects.all())

        self.fields["id_tipo_repuesto_acc"].widget.attrs.update({
            'class':'form-control'
        })

        self.fields["marca"].widget.attrs.update({
            'class':'form-control'
        })

        self.fields["descripcion"].widget.attrs.update({
            'class':'form-control'
        })

        self.fields["precio"].widget.attrs.update({
            'class':'form-control'
        })

        self.fields["cant"].widget.attrs.update({
            'class':'form-control'
        })
      
    class Meta:
        model= Repuesto_accesorio
        fields= ["id_repuesto_acc","id_tipo_repuesto_acc","marca","descripcion","precio","cant"]
 
        labels = {
            'id_tipo_repuesto_acc': 'Tipo de repuesto/accesorio'
        }   

    def validacion(self):
        descrip = self.cleaned_data.get("nombre")
        if descrip == "" or descrip == None:
            raise forms.ValidationError("El campo Nombre no puede quedar vacio") 
        
    def save(self, commit=True):
        instance = super().save(commit=False)

        if self.instance.pk:
            # No modificar 'cant' si es una instancia ya existente
            instance.cant = self.instance.cant

        if commit:
            instance.save()
        return instance 

#Mantenimiento Asignacion de repuesto a una solicitud                
class CargaSolicitudRepuestoAccForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #Mostrar solicitud + cliente + equipo si el presupuesto de la solicitud esta confirmada
        self.fields["id_solicitud"].queryset = Solicitud.objects.select_related(
            "id_equipo__id_cliente",
            "id_equipo__id_tipo_equipo",
            "id_equipo"
        ).filter(Q(id_estado__nombre__iexact="Presupuesto confirmado")|
                 Q(id_estado__nombre__iexact="Reparación en curso"))

        self.fields["id_solicitud"].label_from_instance = lambda obj: (
            f"#{obj.id_solicitud} - "
            f"{obj.descripcion} - "
            f"{obj.id_equipo.id_cliente.nombres} {obj.id_equipo.id_cliente.apellidos} - "
            f"{obj.id_equipo.id_tipo_equipo.descripcion} "
            f"{obj.id_equipo.marca} {obj.id_equipo.modelo}"
        ) 

        # Solo mostrar repuestos con stock > 0
        self.fields["id_repuesto_acc"].queryset = Repuesto_accesorio.objects.filter(stock__gt=0)

        # Mostrar tipo de repuesto + marca + descripción + stock disponible
        self.fields["id_repuesto_acc"].label_from_instance = lambda obj: (
        f"{obj.id_tipo_repuesto_acc.nombre} - {obj.marca or ''} {obj.descripcion} "
        f"(Stock: {obj.stock})").strip()

        
        #Fecha de hoy por defecto para fecha de asignacion
        self.fields["fecha_asignacion"].initial = datetime.date.today()    

        #Estilos de boostrap
        self.fields["id_solicitud"].widget.attrs.update({
            'class':'form-control'
        })

        self.fields["id_repuesto_acc"].widget.attrs.update({
            'class':'form-control'
        })

        self.fields["fecha_asignacion"].widget.attrs.update({
            'class':'form-control'
        })
      
    class Meta:
        model= Solicitud_repuesto_acc
        fields= ["id_solicitud_repuesto_acc","id_solicitud","id_repuesto_acc","fecha_asignacion"]
 
        labels = {
            'id_solicitud': 'Solicitud de un cliente',
            'id_repuesto_acc': 'Repuesto/accesorio'
        }   

    def validacion(self):
        fecha = self.cleaned_data.get("fecha_asignacion")
        if fecha == None:
            raise forms.ValidationError("La fecha de asignacion no puede quedar vacio")  

    def clean_id_repuesto_acc(self):
        repuesto = self.cleaned_data.get("id_repuesto_acc")
        if repuesto and repuesto.stock <= 0:
            raise forms.ValidationError("Este repuesto/accesorio no tiene stock disponible.")
        return repuesto
               

#Mantenimiento cargo        
class CargaCargoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["cargo"].widget.attrs.update({
            'class':'form-control'
        })
            
    class Meta:
        model= Cargo
        fields= ["cargo","activo"]
        error_messages = {
            "cargo": { "unique": "Este cargo ya se cargo anteriormente."}
        }        

    widgets ={
             'activo': forms.CheckboxInput(attrs={'class':'checkboxInvoice'})
        }    

    def validacion(self):
        cargo = self.cleaned_data.get("cargo")
        if cargo == "" or cargo == None:
            raise forms.ValidationError("El campo Cargo no puede quedar vacio")  
        
class CargaAsignarCargoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        id = forms.ModelChoiceField(queryset= User.objects.all())
        id_cargo = forms.ModelChoiceField(queryset= Cargo.objects.all())

        self.fields["id"].widget.attrs.update({
            'class':'form-control'
        })

        self.fields["id_cargo"].widget.attrs.update({
            'class':'form-control'
        })
            
    class Meta:
        model= Usuario_cargo
        fields= ["id_usuario_cargo","id","id_cargo","activo"]
        labels = {
            'id': 'Usuario',
            'id_cargo': 'Cargo'
        }  
        widgets ={
             'activo': forms.CheckboxInput(attrs={'class':'checkboxInvoice'})
        }  

class FiltroSolicitudForm(forms.Form):
    desde = forms.DateField(
        required=False,
        input_formats=['%d/%m/%Y'],
        widget=forms.DateInput(
            format='%d/%m/%Y',
            attrs={
                'class': 'form-control datepicker',
                'placeholder': 'dd/mm/yyyy',
                'autocomplete': 'off'
            }
        )
    )
    hasta = forms.DateField(
        required=False,
        input_formats=['%d/%m/%Y'],
        widget=forms.DateInput(
            format='%d/%m/%Y',
            attrs={
                'class': 'form-control datepicker',
                'placeholder': 'dd/mm/yyyy',
                'autocomplete': 'off'
            }
        )
    )
    cliente = forms.CharField(
        required=False,
        label="Cliente (nombre o apellido)",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    estado = forms.ModelChoiceField(
        queryset=Estado.objects.filter(activo=True),
        required=False,
        label="Tipo de estado",
        empty_label="Todos los tipos de estado",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['estado'].label_from_instance = lambda obj: f"{obj.id_estado} - {obj.nombre}"

class FiltroRepuestoAccForm(forms.Form):
    tipo = forms.ModelChoiceField(
        queryset= Tipo_repuesto_acc.objects.all(),
        required=False,
        label="Tipo de Repuesto/Accesorio",
        empty_label="Todos los tipos de respuestos/accesorios",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    marca = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

class FiltroEstadoTiempoResolucionForm(forms.Form):
    cliente = forms.CharField(
        required=False,
        label="Cliente (nombre o apellido)",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    estado = forms.ModelChoiceField(
        queryset=Estado.objects.filter(activo=True),  # Solo los estados activos
        required=False,
        label="Tipo de estado",
        empty_label="Todos los tipos de estado",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    fecha_inicio = forms.DateField(
        required=False,
        label="Desde",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    fecha_fin = forms.DateField(
        required=False,
        label="Hasta",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['estado'].label_from_instance = lambda obj: f"{obj.id_estado} - {obj.nombre}"

class FiltroRepuestoAccUsadosForm(forms.Form):
    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.all(),
        required=False,
        label="Cliente",
        empty_label="Todos los clientes",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    fecha_inicio = forms.DateField(
        required=False,
        label="Desde",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    fecha_fin = forms.DateField(
        required=False,
        label="Hasta",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )