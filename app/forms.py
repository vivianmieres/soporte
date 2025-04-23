from .models import Tipo_equipo, Cliente, Equipo, Estado, Solicitud,Telefono, Prestadora
from django import forms
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, ReadOnlyPasswordHashField
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
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
        id_cliente = forms.ModelChoiceField(queryset= Cliente.objects.all())
        id_prestadora = forms.ModelChoiceField(queryset= Prestadora.objects.all())
        
        self.fields["prefijo"].widget.attrs.update({
            'class':'form-control'
        })
        self.fields["numero"].widget.attrs.update({
            'class':'form-control'
        })
      
    class Meta:
        model= Telefono
        fields= ["id_telefono","id_cliente","id_prestadora","prefijo","numero","principal","activo"]
        labels = {
            'id_cliente'    : 'Cliente',
            'id_prestadora' : 'Prestadora'
        }    

    widgets ={
       'principal': forms.CheckboxInput(attrs={'class':'checkboxInvoice'}),
       'activo': forms.CheckboxInput(attrs={'class':'checkboxInvoice'})
    }  

    def validacion(self):
        Cliente = self.cleaned_data.get("id_cliente")
        if Cliente == None:
            raise forms.ValidationError("El campo Cliente no puede quedar vacio")  

        Prestadora = self.cleaned_data.get("id_prestadora")
        if Prestadora == None:
            raise forms.ValidationError("El campo Prestadora no puede quedar vacio")   
    
        prefijo = self.cleaned_data.get("prefijo")
        if prefijo == "" or prefijo == None:
            raise forms.ValidationError("El campo Prefijo no puede quedar vacio")  
         
        numero = self.cleaned_data.get("numero")
        if numero == "" or numero == None:
            raise forms.ValidationError("El campo Numero no puede quedar vacio")     
        
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
        id_cliente = forms.ModelChoiceField(queryset= Cliente.objects.all())
        id_tipo_equipo = forms.ModelChoiceField(queryset= Tipo_equipo.objects.all())
        
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

#Mantenimiento solicitud
class CargaSolicitudForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        id_equipo = forms.ModelChoiceField(queryset= Equipo.objects.all())
        id_estado = forms.ModelChoiceField(queryset= Estado.objects.all())


        self.fields["descripcion"].widget.attrs.update({
            'class':'form-control'
        })
        self.fields["fecha_ingreso"].widget.attrs.update({
            'class':'form-control'
        })
        self.fields["fecha_cierre"].widget.attrs.update({
            'class':'form-control'
        })
      
    class Meta:
        model= Solicitud
        fields= ["id_equipo","id_estado","descripcion","fecha_ingreso","fecha_cierre"]
        labels = {
            'id_equipo': 'Equipo',
            'id_estado': 'Estado'
        }    


    def validacion(self):
        equipo = self.cleaned_data.get("id_equipo")
        if equipo == None:
            raise forms.ValidationError("El campo Equipo no puede quedar vacio")   
    
        estado = self.cleaned_data.get("id_estado")
        if estado == None:
            raise forms.ValidationError("El campo Estado no puede quedar vacio") 
        
        descripicion = self.cleaned_data.get("descripcion")
        if estado == None:
            raise forms.ValidationError("El campo Descripcion no puede quedar vacio") 

#Mantenimiento tipo repuesto accesorio        
class CargaTipoRepuestoAccForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       
        self.fields["nombre"].widget.attrs.update({
            'class':'form-control'
        })
      
    class Meta:
        model= Estado
        fields= ["nombre","activo"]
 
    widgets ={
             'activo': forms.CheckboxInput(attrs={'class':'checkboxInvoice'})
        }  

    def validacion(self):
        descrip = self.cleaned_data.get("nombre")
        if descrip == "" or descrip == None:
            raise forms.ValidationError("El campo Nombre no puede quedar vacio")  
        