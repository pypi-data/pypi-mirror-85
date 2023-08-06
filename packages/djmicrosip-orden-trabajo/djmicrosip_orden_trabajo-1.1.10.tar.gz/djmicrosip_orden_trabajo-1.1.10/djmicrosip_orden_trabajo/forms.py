# Django
from django import forms 
from datetime import date
from django.forms.models import inlineformset_factory
import autocomplete_light
from django_select2 import forms as s2forms
from .models import *
from django_microsip_base.libs.models_base.models import VentasDocumentoDetalle, VentasDocumento, Articulo, Cliente, Almacen, ClienteDireccion, CondicionPago, Vendedor,Registry
from django.conf import settings

class ClienteWidget(s2forms.ModelSelect2Widget):
	search_fields = [
		"nombre__icontains",
		"contacto1__icontains",
	]

class PedidoAddForm(forms.ModelForm):
	#cliente = forms.ModelChoiceField(queryset=Cliente.objects.all().order_by('nombre'), widget=forms.Select(attrs={'class': 'form-control'}),  required=True)
	cliente_direccion = forms.ModelChoiceField(queryset=ClienteDireccion.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}), required=False)
	DESCUENTO_TIPO = (
		(u'P', u'Porcentaje'), 
		(u'I', u'Importe'),
		)
	descuento_tipo = forms.ChoiceField(choices=DESCUENTO_TIPO,widget=forms.Select(attrs={'class': 'form-control'}), required=False)
	
	def __init__(self, *args, **kwargs):
		super(PedidoAddForm, self).__init__(*args, **kwargs)
		self.fields['tipo'].widget.attrs['class'] = 'form-control'
		self.fields['fecha'].widget.attrs['class'] = 'form-control'
		self.fields['cliente_clave'].widget.attrs['class'] = 'form-control'
		self.fields['direccion_consignatario'].widget.attrs['class'] = 'form-control'
		self.fields['almacen'].widget.attrs['class'] = 'form-control'
		self.fields['moneda'].widget.attrs['class'] = 'form-control'
		self.fields['condicion_pago'].widget.attrs['class'] = 'form-control'
		self.fields['condicion_pago'].required=False
		self.fields['vendedor'].widget.attrs['class'] = 'form-control'
		self.fields['uso_cfdi'].widget.attrs['class'] = 'form-control'
		self.fields['descuento_porcentaje'].widget.attrs['class'] = 'form-control text-right'
		self.fields['descuento_importe'].widget.attrs['class'] = 'form-control text-right'
		self.fields['modalidad_facturacion'].widget.attrs['class'] = 'form-control'
		self.fields['sistema_origen'].widget.attrs['class'] = 'form-control'
		self.fields['metodo_pago_sat'].widget.attrs['class'] = 'form-control'
		self.fields['importe_neto'].widget.attrs['class'] = 'form-control text-right'
		self.fields['tipo'].required=False
		self.fields['tipo_cambio'].widget.attrs['class'] = 'form-control'
		self.fields['tipo_cambio'].required=False
		self.fields['direccion_consignatario'].required=False
		self.fields['fecha'].required=False
		self.fields['modalidad_facturacion'].required=False
		self.fields['sistema_origen'].required=False
		self.fields['metodo_pago_sat'].required=False
		self.fields['uso_cfdi'].required=False
		self.fields['vendedor'].required=False
		self.fields['descuento_importe'].required=False
		self.fields['descuento_porcentaje'].required=False
		self.fields['cliente'].required=True
		self.fields['descripcion'].widget.attrs['class'] = 'form-control'
		self.fields['descripcion'].required=False
		self.fields['creacion_usuario'].widget.attrs['class'] = 'form-control'
		self.fields['creacion_usuario'].required=False
		self.fields['cliente'].widget.attrs['class'] = 'form-control' 

		if int(settings.MICROSIP_VERSION) >= 2020:
			self.fields['sucursal_id'].widget.attrs['class'] = 'form-control'
			self.fields['sucursal_id'].required=False		


	class Meta:
		model = VentasDocumento
		if int(settings.MICROSIP_VERSION) >= 2020:
			fields = ('cliente','cliente_direccion','descuento_tipo','tipo','fecha','cliente_clave',
				'direccion_consignatario','almacen','moneda','condicion_pago','vendedor','uso_cfdi',
				'descuento_porcentaje','descuento_importe','modalidad_facturacion','sistema_origen',
				'metodo_pago_sat','importe_neto','tipo_cambio','descripcion','creacion_usuario','sucursal_id')
		else:
			fields = ('cliente','cliente_direccion','descuento_tipo','tipo','fecha','cliente_clave',
				'direccion_consignatario','almacen','moneda','condicion_pago','vendedor','uso_cfdi',
				'descuento_porcentaje','descuento_importe','modalidad_facturacion','sistema_origen',
				'metodo_pago_sat','importe_neto','tipo_cambio','descripcion','creacion_usuario')
		widgets = {
			"cliente": ClienteWidget,
		}

class UsuarioOneSignalForm(forms.ModelForm):
	
	def __init__(self, *args, **kwargs):
		super(UsuarioOneSignalForm, self).__init__(*args, **kwargs)
		
		self.fields['id_onesignal'].widget.attrs['class'] = 'form-control'
	
	class Meta:
		model = Usuario_notificacion
		fields = ('id_onesignal',)


class VentasDetalleDocumentoForm(forms.ModelForm):
	articulo = forms.ModelChoiceField(queryset=Articulo.objects.all().order_by('nombre'), widget=forms.Select(attrs={'class': 'form-control'}), required=True)

	def __init__(self, *args, **kwargs):
		super(VentasDetalleDocumentoForm, self).__init__(*args, **kwargs)
		self.fields['unidades'].widget.attrs['class'] = 'form-control text-right'
		self.fields['precio_unitario'].widget.attrs['class'] = 'form-control text-right'
		self.fields['descuento_porcentaje'].widget.attrs['class'] = 'form-control text-right'
		self.fields['precio_total_neto'].widget.attrs['class'] = 'form-control text-right'
		self.fields['notas'].widget.attrs['class'] = 'form-control'
		self.fields['notas'].widget.attrs['rows'] = 2
		self.fields['articulo_clave'].widget.attrs['class'] = 'form-control'

	class Meta:
		model = VentasDocumentoDetalle
		fields = ('articulo','unidades','precio_unitario','descuento_porcentaje','precio_total_neto','notas','articulo_clave')

class VendedorForm(forms.Form):
	vendedor = forms.ModelChoiceField(queryset=Vendedor.objects.all().order_by('nombre'), widget=forms.Select(attrs={'class': 'form-control'}), required=False)

class PedidoCrmForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(PedidoCrmForm, self).__init__(*args, **kwargs)
		self.fields['hardware'].required=False
		self.fields['descripcion_otros'].required=False
		self.fields['precio_aproximado'].required=False
		self.fields['fecha_registro'].required=False
		self.fields['precio_aproximado'].widget.attrs['class'] = 'form-control text-right'
		self.fields['descripcion_general'].required=False
		self.fields['descripcion_general'].widget.attrs['class'] = 'form-control'
		self.fields['fecha_registro'].widget.attrs['class'] = 'form-control'
		self.fields['descripcion_otros'].widget.attrs['class'] = 'form-control'
		self.fields['tipo_servicio'].widget.attrs['class'] = 'form-control'
		self.fields['tipo_llamada'].widget.attrs['class'] = 'form-control'
		self.fields['descripcion_otros'].widget.attrs['rows'] = 3
		self.fields['preprogramado'].required=False		

	class Meta:
		model = Pedidos_Crm
		fields = ('hardware','descripcion_otros','precio_aproximado','descripcion_general',
				'tipo_servicio','llamada','tipo_llamada','fecha_registro','preprogramado')

class PreferenciasManageForm(forms.Form):
	articulo = forms.ModelChoiceField(queryset=Articulo.objects.all().order_by('nombre'), widget=forms.Select(attrs={'class': 'form-control'}))
	logo = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
	imagen_extra = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
	url_pdf_destino=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control'}),)
	email=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control'}),)
	password=forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'class': 'form-control'}),)
	servidor_correo = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control'}),)
	puerto=forms.CharField(max_length=20,widget=forms.TextInput(attrs={'class': 'form-control'}),)

	app_id=forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'class': 'form-control'}),required=False)
	app_api_key=forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'class': 'form-control'}),required=False)
	url_servidor=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control'}),required=False)

	
	def save(self, *args, **kwargs):
		articulo = Registry.objects.get( nombre = 'SIC_Pedidos_Crm_Articulo_predeterminado')
		articulo.valor = self.cleaned_data['articulo'].id
		articulo.save()
		
		logo = Registry.objects.get( nombre = 'SIC_Pedidos_Crm_Logo')
		logo.valor = self.cleaned_data['logo']
		logo.save()
		
		imagen_extra = Registry.objects.get( nombre = 'SIC_Pedidos_Crm_Imagen_extra')
		imagen_extra.valor = self.cleaned_data['imagen_extra']
		imagen_extra.save()
		
		url_pdf_destino = Registry.objects.get( nombre = 'SIC_Pedidos_Crm_Url_Pdf_Destino')
		url_pdf_destino.valor = self.cleaned_data['url_pdf_destino']
		url_pdf_destino.save()

		email = Registry.objects.get( nombre = 'SIC_Pedidos_Crm_Email')
		email.valor = self.cleaned_data['email']
		email.save()

		password = Registry.objects.get( nombre = 'SIC_Pedidos_Crm_Password')
		password.valor = self.cleaned_data['password']
		password.save()

		servidor_correo = Registry.objects.get( nombre = 'SIC_Pedidos_Crm_Servidro_Correo')
		servidor_correo.valor = self.cleaned_data['servidor_correo']
		servidor_correo.save()

		puerto = Registry.objects.get( nombre = 'SIC_Pedidos_Crm_Puerto')
		puerto.valor = self.cleaned_data['puerto']
		puerto.save()

		app_id = Registry.objects.get( nombre = 'SIC_Pedidos_Crm_App_id')
		app_id.valor = self.cleaned_data['app_id']
		app_id.save()

		app_api_key = Registry.objects.get( nombre = 'SIC_Pedidos_Crm_App_api_key')
		app_api_key.valor = self.cleaned_data['app_api_key']
		app_api_key.save()

		url_servidor = Registry.objects.get( nombre = 'SIC_Pedidos_Crm_Url_servidor')
		url_servidor.valor = self.cleaned_data['url_servidor']
		url_servidor.save()



class FirmaForm(forms.ModelForm):
	data_image=forms.CharField(widget=forms.HiddenInput(), required=False)
	def __init__(self, *args, **kwargs):
		super(FirmaForm, self).__init__(*args, **kwargs)

		self.fields['firma'].widget.attrs['class'] = 'form-control'
		self.fields['firma'].required=False

	class Meta:
		model = Pedidos_Crm
		fields = ('firma','data_image')

class FindFrom(forms.Form):
	llamada=forms.BooleanField(required=False)
	inicio=forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control'}),required=False,initial=date.today)
	fin=forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control'}),required=False,initial=date.today)
	busqueda=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control','place-holder':'Ingrese criterio de busqueda'}), required=False)
	FILTRO = (
		(u'', u'-------------'),
		(u'EP', u'En Proceso'),
		(u'PDA', u'Pendiente de Asignar'), 
		(u'F', u'Finalizado'),
		)
	filtro = forms.ChoiceField(choices=FILTRO,widget=forms.Select(attrs={'class': 'form-control'}), required=False)
	TIPO_DOCUMENTO = (
		(u'', u'-------------'),
		(u'F', u'Facturado'),
		(u'R', u'Remisionado'),
		)
	tipo_documento = forms.ChoiceField(choices=TIPO_DOCUMENTO,widget=forms.Select(attrs={'class': 'form-control'}), required=False)