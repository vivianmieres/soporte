# signals.py
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Solicitud
from app.utils.whatsapp import send_whatsapp_message
from app.utils.email_sms import send_sms_via_email
from app.models import Parametro

@receiver(pre_save, sender=Solicitud)
def guardar_estado_anterior(sender, instance, **kwargs):
    if instance.pk:
        try:
            instance._estado_anterior = Solicitud.objects.get(pk=instance.pk).id_estado
        except Solicitud.DoesNotExist:
            instance._estado_anterior = None

@receiver(post_save, sender=Solicitud)
def notificar_solicitud(sender, instance, created, **kwargs):
    cliente = instance.id_equipo.id_cliente
    telefono = cliente.telefono_set.filter(principal=True, activo=True).first()
    if not telefono:
        return
    numero_completo = f"{telefono.prefijo}{telefono.numero}"

    if created:
        mensaje = f"Hola {cliente.nombres}, tu solicitud #{instance.id_solicitud} ha sido registrada."
        #send_whatsapp_message(numero_completo, mensaje)
    else:
        estado_anterior = getattr(instance, "_estado_anterior", None)
        if estado_anterior != instance.id_estado:
            mensaje = f"La solicitud #{instance.id_solicitud} ha cambiado de estado a: {instance.id_estado}."
           # send_whatsapp_message(numero_completo, mensaje)

        if instance.id_estado.nombre.lower() == "cerrado":
            encuesta_url = "" #f"https://mi-sitio.com/encuesta?sid={instance.id_solicitud}"
            mensaje = (
                f"Tu solicitud #{instance.id_solicitud} ha sido cerrada.\n"
                f"Agradecemos tu opinión, por favor responde esta breve encuesta:\n{encuesta_url}"
            )
            #send_whatsapp_message(numero_completo, mensaje)

# Lógica condicional según parámetros
    parametros = Parametro.objects.first()
    if mensaje:
        if parametros.notificacion_whatsapp:
            send_whatsapp_message(numero_completo, mensaje)
        if parametros.notificacion_sms:
            if telefono.id_prestadora and telefono.id_prestadora.servidor:
                send_sms_via_email(numero_completo, telefono.id_prestadora.servidor, mensaje)
