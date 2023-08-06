from django.db import models
#Python
from datetime import datetime
#Own
from multiselectfield import MultiSelectField
from .storage import OverwriteStorage
from django_microsip_base.libs.models_base.models import VentasDocumento,VendedorBase,Cliente

class Pedidos_Crm(models.Model):
    id = models.AutoField(primary_key=True, db_column='CRM_ID')
    folio= models.CharField(max_length=9,db_column='FOLIO',null=True)
    fecha_registro = models.DateTimeField(db_column='FECHA_HORA_REGISTRO')
    fecha_inicio = models.DateTimeField(null=True, db_column='FECHA_HORA_INICIO')
    PROGRESS_CHOICES = (
        (u'0', u'Recibido'),
        (u'25', u'Inicio'), 
        (u'50', u'Finalizado'), 
        (u'75', u'Aviso cliente'), 
        (u'100', u'Entregado')
        )
    progreso = models.CharField(max_length=3, default='0', choices=PROGRESS_CHOICES, db_column='PROGRESO')
    fecha_meta = models.DateTimeField(null=True, db_column='FECHA_META')
    fecha_mod = models.DateTimeField(null=True, db_column='FECHA_MODIFICACION')
    fecha_aviso = models.DateTimeField(null=True, db_column='FECHA_AVISO')
    fecha_fin = models.DateTimeField(null=True, db_column='FECHA_FIN')
    fecha_entrega = models.DateTimeField(null=True, db_column='FECHA_ENTREGA')
    nota = models.TextField(null=True, blank=True, db_column='NOTA')
    bdatos = models.CharField(max_length=250, db_column='BASE_DATOS')
    conexion = models.CharField(max_length=10, db_column='CONEXION')
    HARDWARE_CHOICES = (
        (u'CPU', u'CPU'),
        (u'LAPTOP', u'LAPTOP'),
        (u'CABLE', u'CABLE'),
        (u'MONITOR', u'MONITOR'),
        (u'IMPRESORA', u'IMPRESORA'),
        (u'CARGADOR', u'CARGADOR'),
        (u'OTROS', u'OTROS')
        )
    hardware=MultiSelectField(choices=HARDWARE_CHOICES,db_column="HARDWARE")
    descripcion_otros=models.TextField(null=True,db_column="DESC_OTROS")
    precio_aproximado=models.FloatField(default=0,null=True, blank=True,db_column="PRECIO_APROXIMADO")
    descripcion_general=models.TextField(null=True,db_column="DESC_GENERAL")
    descripcion_solicitud=models.TextField(null=True,db_column="DESC_SOLICITUD")
    firma = models.ImageField(blank=True, null=True , upload_to='pedidos_crm', db_column='SIC_FIRMA_URL', storage=OverwriteStorage())
    TIPO_SERVICIO_CHOICES = (
        (u'PRESENCIAL', u'PRESENCIAL'),
        (u'REMOTO', u'REMOTO'),
        )
    tipo_servicio=models.CharField(null=True,max_length=50, default='PRESENCIAL', choices=TIPO_SERVICIO_CHOICES, db_column='TIPO_SERVICIO')
    llamada=models.BooleanField(default=False, db_column='LLAMADA')
    solicitud=models.BooleanField(default=False, db_column='SOLICITUD')
    TIPO_LLAMADA_CHOICES = (
        (u'PENDIENTE', u'PENDIENTE'),
        (u'ATENDIDA', u'ATENDIDA'),
        )
    tipo_llamada=models.CharField(null=True,max_length=50, default='ATENDIDA', choices=TIPO_LLAMADA_CHOICES, db_column='TIPO_LLAMADA')
    envio_correo=models.BooleanField(default=False, db_column='ENVIO_CORREO')
    preprogramado=models.BooleanField(default=False, db_column='PREPROGRAMADO')
    venta=models.ForeignKey('VentasDocumento', blank=True, null=True, db_column='VENTA',on_delete=models.CASCADE)

    class Meta:
        db_table = u'SIC_PEDIDOS_CRM'
        app_label = 'models_base' 

    def image_path(instance, filename):
        return os.path.join('some_dir', str(instance.some_identifier), 'filename.ext')
    # def __unicode__(self):
    #     return self.progreso

class Usuario_notificacion(models.Model):
    user_id = models.AutoField(primary_key=True, db_column='USER_ID')
    vendedor= models.ForeignKey('Vendedor', blank=True, null=True, db_column='VENDEDOR_ID',on_delete=models.CASCADE)
    id_onesignal=models.CharField(max_length=200,db_column='ID_ONESIGNAL',null=True)
    administrador=models.BooleanField(default=False,db_column='ADMINISTRADOR')
    usuario_microsipd=models.IntegerField( blank=True, null=True, db_column='USUARIO_MICROSIP')

    class Meta:
        db_table = u'SIC_USUARIO_NOTIFICACION'
        app_label = 'models_base'