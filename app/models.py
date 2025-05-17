# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order

#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

#Tablas creadas Django
class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    id = models.BigAutoField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    def __str__(self) -> str:
        return str(self.username)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'



#Tablas creadas
class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nombres = models.CharField()
    apellidos = models.CharField()
    documento = models.IntegerField()
    nacionalidad = models.CharField()
    email = models.CharField(blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    direccion = models.CharField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.nombres} {self.apellidos}"
    

    class Meta:
        managed = False
        db_table = 'cliente'



class Prestadora(models.Model):
    id_prestadora = models.AutoField(primary_key=True)
    empresa = models.CharField(max_length=100, unique= True)
    activo = models.BooleanField(default= True)

    def __str__(self) -> str:
         return str(self.empresa)
    

    class Meta:
        managed = False
        db_table = 'prestadora'


class Telefono(models.Model):
    id_telefono = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='id_cliente')
    id_prestadora = models.ForeignKey(Prestadora, models.DO_NOTHING, db_column='id_prestadora')
    prefijo = models.CharField(max_length=4)
    numero = models.IntegerField()
    principal = models.BooleanField()
    activo = models.BooleanField(default= True)

    def __str__(self) -> str:
        return '('+  str(self.prefijo) +') ' +  str(self.numero)
    

    class Meta:
        managed = False
        db_table = 'telefono'

class Tipo_equipo(models.Model):
    id_tipo_equipo = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=100)
    activo = models.BooleanField(default= True)

    def __str__(self) -> str:
         return str(self.descripcion)
    

    class Meta:
        managed = False
        db_table = 'tipo_equipo'

class Equipo(models.Model):
    id_equipo = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='id_cliente') 
    id_tipo_equipo = models.ForeignKey(Tipo_equipo, models.DO_NOTHING, db_column='id_tipo_equipo') 
    marca = models.CharField(max_length= 50)
    modelo = models.CharField(max_length= 50)
    serie = models.CharField(max_length= 50)
    descripcion = models.CharField(max_length=100)
    
    def __str__(self) -> str:
         return str(self.id_equipo)
    

    class Meta:
        managed = False
        db_table = 'equipo'

class Estado(models.Model):
    id_estado = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=150)
    activo = models.BooleanField(default= True) 

    def __str__(self) -> str:
         return str(self.nombre)
    

    class Meta:
        managed = False
        db_table = 'estado'


class Tipo_repuesto_acc(models.Model):
    id_tipo_repuesto_acc = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    activo = models.BooleanField(default= True)

    def __str__(self) -> str:
         return str(self.nombre)
    

    class Meta:
        managed = False
        db_table = 'tipo_repuesto_acc'

class Repuesto_accesorio(models.Model):
    id_repuesto_acc = models.AutoField(primary_key=True)
    id_tipo_repuesto_acc = models.ForeignKey(Tipo_repuesto_acc, models.DO_NOTHING, db_column='id_tipo_repuesto_acc')
    marca = models.CharField(max_length= 50, null=True)
    descripcion = models.CharField(max_length= 100)
    precio = models.IntegerField()
    cant = models.IntegerField()
    stock = models.IntegerField()
    fecha_registro = models.DateField(auto_now_add=True)
   
    
    def __str__(self) -> str:
        return str(self.descripcion)
    

    class Meta:
        managed = False
        db_table = 'repuesto_accesorio'

class Cargo(models.Model):
    id_cargo = models.AutoField(primary_key=True)
    cargo = models.CharField(max_length=100)
    activo = models.BooleanField(default= True)

    def __str__(self) -> str:
         return str(self.cargo)
    

    class Meta:
        managed = False
        db_table = 'cargo'

class Usuario_cargo(models.Model):
    id_usuario_cargo = models.AutoField(primary_key=True)
    id = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='id') 
    id_cargo = models.ForeignKey(Cargo, models.DO_NOTHING, db_column='id_cargo')
    activo = models.BooleanField(default=True)

    class Meta:
        managed = False
        db_table = 'usuario_cargo'



class Solicitud(models.Model):
    id_solicitud = models.AutoField(primary_key=True)
    id_equipo = models.ForeignKey(Equipo, models.DO_NOTHING, db_column='id_equipo') 
    id_estado = models.ForeignKey(Estado, models.DO_NOTHING, db_column='id_estado') 
    descripcion = models.CharField(max_length=150)
    fecha_ingreso = models.DateField()
    fecha_cierre = models.DateField(null= True, blank=True)
    id_usuario_cargo = models.ForeignKey(Usuario_cargo, models.DO_NOTHING, db_column='id_usuario_cargo', null= True)

    def __str__(self) -> str:
         return str(self.id_solicitud)
    

    class Meta:
        managed = True
        db_table = 'solicitud'

class Solicitud_repuesto_acc(models.Model):
    id_solicitud_repuesto_acc = models.AutoField(primary_key=True)
    id_solicitud = models.ForeignKey(Solicitud, models.DO_NOTHING, db_column='id_solicitud')
    id_repuesto_acc = models.ForeignKey(Repuesto_accesorio, models.DO_NOTHING, db_column='id_repuesto_acc') 
    fecha_asignacion =  models.DateField()

    def __str__(self) -> str:
         return str(self.id_solicitud_repuesto_acc)
    

    class Meta:
        managed = False
        db_table = 'solicitud_repuesto_acc'

class Solicitud_estado_historico(models.Model):
    id_solicitud_estado_historico = models.AutoField(primary_key=True)
    id_solicitud = models.ForeignKey(Solicitud, models.DO_NOTHING, db_column='id_solicitud')
    id_estado = models.ForeignKey(Estado, models.DO_NOTHING, db_column='id_estado')
    desde = models.DateField()
    hasta = models.DateField()