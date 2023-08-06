#encoding:utf-8
from .forms import *
from .models import *
# from django.db.models import get_app, get_models
from django.apps import apps
#from django.db.models import get_app, get_models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from common.paginator import DumbPaginator

from django_microsip_base.libs.models_base.models import Articulo,ArticuloPrecio,ArticuloClave, Moneda, PrecioEmpresa,Registry,ClienteDireccion, Cliente, CondicionPago, Vendedor, VentasDocumento, VentasDocumentoDetalle, Almacen,ClienteClave,VentasDocumentoLiga
from django.contrib.auth.models import User
from datetime import datetime
from django.forms.models import inlineformset_factory
from django.forms import formset_factory
# Django
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.list import ListView
from django.db import router, connections,connection
from django.core import management
from microsip_api.comun.sic_db import first_or_none
from .storage import send_mail_orden
# Python
import time
import json
import os
import pdb
import re, io
# import cStringIO as StringIO
from io import StringIO
from django.conf import settings
from django.template import Context
from django.template.loader import get_template
from datetime import date,datetime,timedelta
from django.db.models import Q
from xhtml2pdf import pisa
from base64 import decodestring
from django.core.files import File
import onesignal as onesignal_sdk
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.utils.functional import cached_property
 
# from apscheduler.schedulers.background import BackgroundScheduler
# app_id = 'abe73585-28d8-4b4d-9fa7-ffcd40fd980f'
# app_api_key = 'Zjc3ZDZmMDctYTk0OC00ZWU1LTkwNmEtNjVlYzJiZWNkZTc3'

@login_required(login_url='/login/')
def index(request):
	form=VendedorForm(request.POST or None)  
	page = request.GET.get('page')
	llamada = request.GET.get('llamada')
	if llamada =='on' or llamada == 'True':
		llamada=True
	else:
		llamada=False

	busqueda = request.GET.get('busqueda')
	filtro = request.GET.get('filtro')
	tipo_documento = request.GET.get('tipo_documento')
	ini_fecha = request.GET.get('inicio')
	fin_fecha = request.GET.get('fin')
	ligas=None
	ventas_pages=None
	# print(ini_fecha,fin_fecha)
	if ini_fecha and fin_fecha:
		inicio = ini_fecha
		fin = fin_fecha
		inicio=datetime.strptime(inicio, '%d/%m/%Y')
		fin=datetime.strptime(fin, '%d/%m/%Y')
		inicio=datetime(inicio.year,inicio.month,inicio.day,0,0)
		fin=datetime(fin.year,fin.month,fin.day,23,59)
		print(inicio,fin)
		pedidos_all=Pedidos_Crm.objects.filter(fecha_registro__gte=inicio,fecha_registro__lte=fin)
	else:
		hoy=datetime.today()
		inicio=datetime(hoy.year,hoy.month,hoy.day,0,0)
		fin=datetime(hoy.year,hoy.month,hoy.day,23,59)
		pedidos_all=Pedidos_Crm.objects.filter(fecha_registro__gte=inicio,fecha_registro__lte=fin)
		pedidos=pedidos_all.values_list("folio").order_by("fecha_registro")
	if llamada:
		pedidos_all=pedidos_all.filter(llamada=llamada)
	if filtro == "EP":
		pedidos_all=pedidos_all.filter(progreso__in=['0','25','50','75'])
	elif filtro == "F":
		pedidos_all=pedidos_all.filter(progreso__in=['100'])		
	pedidos=pedidos_all.values_list("folio").order_by("fecha_registro")
	if tipo_documento == "F":
		ventas_surtidas =VentasDocumento.objects.filter(folio__in=pedidos,estado="S")
		ventas_ligas=VentasDocumentoLiga.objects.filter(factura__in=ventas_surtidas,devolucion__estado="F").values_list("factura__id")
		ligas=[ven[0] for ven in ventas_ligas]
		if ventas_ligas:
			pedidos_all=pedidos_all.filter(Q(venta__estado="F") | Q(venta__id__in=ventas_ligas)).exclude(venta__estado__in=["C"])
		else:
			pedidos_all=pedidos_all.filter(venta__estado="F").exclude(venta__estado__in=["C"])
	elif tipo_documento== "R":
		ventas_surtidas =VentasDocumento.objects.filter(folio__in=pedidos,estado="S")
		ventas_ligas=VentasDocumentoLiga.objects.filter(factura__in=ventas_surtidas,devolucion__estado="F").values_list("factura__id")
		ligas=[ven[0] for ven in ventas_ligas]
		if ventas_ligas:
			pedidos_all=pedidos_all.filter(venta__estado="S").exclude(venta__estado__in=["C"]).exclude(venta__id__in=ventas_ligas)
		else:
			pedidos_all=pedidos_all.filter(venta__estado="S").exclude(venta__estado__in=["C"])
	else:
		pedidos_all=pedidos_all.exclude(venta__estado__in=["C","S","F"])
	
	if busqueda:
		if len(busqueda) >= 8:
			pedidos_all=pedidos_all.filter( Q(venta__cliente__nombre__icontains=busqueda)|
									Q(venta__cliente__contacto1__icontains=busqueda)| 
									Q(venta__vendedor__nombre__icontains=busqueda))
		else:
			pedidos_all=pedidos_all.filter( Q(venta__cliente__nombre__icontains=busqueda)|
									Q(venta__cliente__contacto1__icontains=busqueda)| 
									Q(venta__vendedor__nombre__icontains=busqueda)|
									Q(venta__folio__icontains=busqueda))
	if filtro == "PDA":
		pedidos_all=pedidos_all.filter(venta__vendedor=None)


	if pedidos_all.count() >0:
		if(pedidos_all.count()<=20):
			ventas_pages=pedidos_all
			numero_pagina=1
			total_paginas=1
			has_previous=None
			has_next=None
			print("ffinn")
		else:
			print("fffinnn")
			paginator = Paginator(pedidos_all, 20)
			try:
				print("try")
				ventas_pages = paginator.page(page)
			except PageNotAnInteger:
				ventas_pages = paginator.page(1)
			except EmptyPage:
				ventas_pages = paginator.page(paginator.num_pages)
	form_initial={
		"llamada":llamada,
		"inicio":inicio,
		"fin":fin,
		"busqueda":busqueda,
		"filtro":filtro,
		"tipo_documento":tipo_documento,
	}
	print(page,llamada,busqueda,filtro,tipo_documento,ini_fecha,fin_fecha)
	form_busqueda=FindFrom(form_initial)
	
	print("pag fin")
	context={
	 	'form':form,
		'ventas':ventas_pages,
		'form_busqueda':form_busqueda,
		'ligas':ligas,
		'llamada':llamada,
		'busqueda':busqueda,
		'filtro':filtro,
		'tipo_documento':tipo_documento,
		'inicio':inicio,
		'fin':fin,
	 }

	
	return render(request, 'djmicrosip_orden_trabajo/index.html',context)

#@csrf_exempt
def get_pedido(request):
	folio = request.GET.get('folio')
	form=VendedorForm(request.POST or None)
	# print(form)
	pedido=None
	data_=None
	venta_vendedor=None
	vendedor_id=None
	# if request.method=='POST':
	# 	data=json.loads(request.body)
	# 	print(data)
	if folio:
		# folio = data['folio']
		pedido=Pedidos_Crm.objects.filter(folio=folio).first()
		venta=VentasDocumento.objects.filter(folio=folio).first()
		if venta.vendedor:
			venta_vendedor=venta.vendedor.nombre
			vendedor_id=venta.vendedor.id
		if pedido:
			form=str(form).replace('<tr><th><label for="id_vendedor">Vendedor:</label></th><td>','')
			form=form.replace('form-control','hidden form-control pedido'+str(pedido.id))

			data_={
				'id':pedido.id,
				'fecha_registro':pedido.fecha_registro.strftime("%d/%m/%Y"),
				'progreso':pedido.progreso,
				'llamada':pedido.llamada,
				'tipo_llamada':pedido.tipo_llamada,
				'envio_correo':pedido.envio_correo,
				'venta_folio':venta.folio,
				'venta_id':venta.id,
				'venta_descripcion':venta.descripcion,
				'venta_estado':venta.estado,
				'venta_cli_nombre':venta.cliente.nombre,
				'venta_vendedor':venta_vendedor,
				'vendedor_id':vendedor_id,
				'form':form,
			}
		# print(data_)
		#pedido=list(pedido.values_list('id','fecha_registro','progreso','llamada','envio_correo'))

	return HttpResponse(json.dumps(data_), content_type='application/json')

@login_required(login_url='/login/')
def lista_pedidos(request):
	form_busqueda=FindFrom(request.POST or None)

	context={ 
		'form_busqueda':form_busqueda,
	}
	return render(request, 'djmicrosip_orden_trabajo/lista_pedidos.html',context)

# @cached_property
def get_venta(request):
	ventas=None
	ligas=None
	ventas_pages=None
	page=None
	if request.method=='GET':
		# data=json.loads(request.body)
		# print(data)
		if ventas==None:
			# page = data['page']
			# llamada = data['llamada']
			# busqueda = data['busqueda']
			# filtro = data['filtro']
			# tipo_documento = data['tipo_documento']
			# ini_fecha=data['inicio']
			# fin_fecha=data['fin']
			page = request.GET.get('page')
			llamada = request.GET.get('llamada')
			busqueda = request.GET.get('busqueda')
			filtro = request.GET.get('filtro')
			tipo_documento = request.GET.get('tipo_documento')
			ini_fecha = request.GET.get('inicio')
			fin_fecha = request.GET.get('fin')
			#print(page,llamada,busqueda,filtro,tipo_documento,ini_fecha,fin_fecha)
			# print(ini_fecha,fin_fecha)
			if llamada=='1':
				llamada=True
			else:
				llamada=False
	
			if ini_fecha and fin_fecha:
				inicio = ini_fecha
				fin = fin_fecha
				inicio=datetime.strptime(inicio, '%d/%m/%Y')
				fin=datetime.strptime(fin, '%d/%m/%Y')
				inicio=datetime(inicio.year,inicio.month,inicio.day,0,0)
				fin=datetime(fin.year,fin.month,fin.day,23,59)
				print(inicio,fin)
				pedidos_all=Pedidos_Crm.objects.filter(fecha_registro__gte=inicio,fecha_registro__lte=fin)
			else:
				hoy=datetime.today()
				inicio=datetime(hoy.year,hoy.month,hoy.day,0,0)
				fin=datetime(hoy.year,hoy.month,hoy.day,23,59)
				pedidos_all=Pedidos_Crm.objects.filter(fecha_registro__gte=inicio,fecha_registro__lte=fin)
				pedidos=pedidos_all.values_list("folio").order_by("fecha_registro")
				ventas=VentasDocumento.objects.filter(folio__in=pedidos).exclude(estado__in=["C","S","F"]).only('id','folio')
				#ventas=VentasDocumento.objects.filter(folio__in=pedidos,estado="S").exclude(estado__in=["C"])
			if llamada:
				pedidos_all=pedidos_all.filter(llamada=llamada)
			if filtro == "EP":
				pedidos_all=pedidos_all.filter(progreso__in=['0','25','50','75'])
			elif filtro == "F":
				pedidos_all=pedidos_all.filter(progreso__in=['100'])		
			pedidos=pedidos_all.values_list("folio").order_by("fecha_registro")
			# print(pedidos)
			if tipo_documento == "F":
				ventas_surtidas =VentasDocumento.objects.filter(folio__in=pedidos,estado="S")
				ventas_ligas=VentasDocumentoLiga.objects.filter(factura__in=ventas_surtidas,devolucion__estado="F").values_list("factura__id")
				ligas=[ven[0] for ven in ventas_ligas]
				if ventas_ligas:
					ventas=VentasDocumento.objects.filter(Q(estado="F",folio__in=pedidos) | Q(id__in=ventas_ligas)).exclude(estado__in=["C"]).only('id','folio').order_by('-folio')
				else:
					ventas=VentasDocumento.objects.filter(estado="F",folio__in=pedidos).exclude(estado__in=["C"]).only('id','folio').order_by('-folio')
			elif tipo_documento== "R":
				ventas_surtidas =VentasDocumento.objects.filter(folio__in=pedidos,estado="S")
				ventas_ligas=VentasDocumentoLiga.objects.filter(factura__in=ventas_surtidas,devolucion__estado="F").values_list("factura__id")
				ligas=[ven[0] for ven in ventas_ligas]
				if ventas_ligas:
					ventas=VentasDocumento.objects.filter(folio__in=pedidos,estado="S").exclude(estado__in=["C"]).exclude(id__in=ventas_ligas).only('id','folio').order_by('-folio')
				else:
					ventas=VentasDocumento.objects.filter(folio__in=pedidos,estado="S").exclude(estado__in=["C"]).only('id','folio').order_by('-folio')
			else:
				
				ventas=VentasDocumento.objects.filter(folio__in=pedidos).exclude(estado__in=["C","S","F"]).only('id','folio').order_by('-folio')
			
			if busqueda:
				if len(busqueda) >= 8:
					ventas=ventas.filter( Q(cliente__nombre__icontains=busqueda)|
											Q(cliente__contacto1__icontains=busqueda)| 
											Q(vendedor__nombre__icontains=busqueda))
				else:
					ventas=ventas.filter( Q(cliente__nombre__icontains=busqueda)|
											Q(cliente__contacto1__icontains=busqueda)| 
											Q(vendedor__nombre__icontains=busqueda)|
											Q(folio__icontains=busqueda))
			if filtro == "PDA":
				ventas=ventas.filter(vendedor=None)

	# else:
	# 	hoy=datetime.today()
	# 	inicio=datetime(hoy.year,hoy.month,hoy.day,0,0)
	# 	fin=datetime(hoy.year,hoy.month,hoy.day,23,59)
	# 	pedidos_all=Pedidos_Crm.objects.filter(fecha_registro__gte=inicio,fecha_registro__lte=fin)
	# 	pedidos=pedidos_all.values_list("folio").order_by("fecha_registro")
	# 	ventas=VentasDocumento.objects.filter(folio__in=pedidos).exclude(estado__in=["C","S","F"]).only('id','folio')
		
	#ventas=serializers.serialize('json', ventas, fields=('id','folio'))	
	ventas=ventas.values_list('id','folio')
	#print(len(ventas))
	print("pag ini")

	if(len(ventas)<=20):
		ventas_pages=ventas
		numero_pagina=1
		total_paginas=1
		has_previous=None
		has_next=None
	else:
		paginator = Paginator(ventas, 20) 
		try:
			ventas_pages = paginator.page(page)
		except PageNotAnInteger:
			ventas_pages = paginator.page(1)
		except EmptyPage:
			ventas_pages = paginator.page(paginator.num_pages)
		
		numero_pagina=ventas_pages.number
		total_paginas=ventas_pages.paginator.num_pages
		has_previous=ventas_pages.has_previous
		has_next=ventas_pages.has_next
	print("pag fin")
	#ventas_pages=list(ventas_pages)
	data={
		'ventas':list(ventas_pages),
		'ligas':ligas,
		'numero_pagina':str(numero_pagina),
		'total_paginas':str(total_paginas),
		'has_previous':str(has_previous),
		'has_next':str(has_next),
	}
	  
	return HttpResponse(json.dumps(data), content_type='application/json')

def none_cero(folio):
	indice_inicio=0
	indice_fin=0
	onesignal_client=None
	x=0
	while indice_inicio == 0:
		if folio[x] == "0":
				indice_inicio=x
		x=x+1
	x=indice_inicio
	while indice_fin == 0:
		if folio[x] != "0":
				indice_fin=x
		x=x+1
	remplazar=folio[indice_inicio:indice_fin]
	folio_nuevo=folio.replace(remplazar, "")

	return folio_nuevo

@login_required(login_url='/login/')
def add_pedido(request,folio,template_name='djmicrosip_orden_trabajo/add_pedido.html'):
	id_articulo=Registry.objects.get(nombre='SIC_Pedidos_Crm_Articulo_predeterminado').get_value()
	articulo=Articulo.objects.get(id=id_articulo)
	clave_articulo=ArticuloClave.objects.filter(articulo__id=id_articulo)
	onesignal_client = None
	servidor=''
	if int(settings.MICROSIP_VERSION) >= 2020:
		using = router.db_for_write(Articulo)
		c = connections[using].cursor()
		query = "select sucursal_id from sucursales where nombre='Matriz'"
		c.execute(query)
		sucursal_id = c.fetchall()[0][0]
		print(sucursal_id)
	#lo asignamos como el valor inicial para el fromset
	if clave_articulo:
		clave_articulo=clave_articulo[0].clave
	else:
		clave_articulo=None

	form_initial = [{
				'articulo':articulo,
				'unidades':1,
				'precio_unitario':0,
				'descuento_porcentaje':0,
				'precio_total_neto':0,
				'notas':'',
				'articulo_clave':clave_articulo,
			},]
	#si el pedido tiene id buscamos el pedido para la instancia de venta
	if folio != '0':
		pedido=Pedidos_Crm.objects.get(folio=folio)

	else:
		pedido=None

	if pedido:
		venta=VentasDocumento.objects.get(folio=pedido.folio)
		venta_fecha=VentasDocumento.objects.filter(folio=pedido.folio)[0]
		form=PedidoAddForm(request.POST or None,instance=venta)
		DetalleFormSet = inlineformset_factory(VentasDocumento, VentasDocumentoDetalle,VentasDetalleDocumentoForm,extra=1)
		formset = DetalleFormSet(request.POST or None,instance=venta)
		form_crm=PedidoCrmForm(request.POST or None,instance=pedido)
		print("-0-0-0-",venta)
	else:
		venta=None
		form=PedidoAddForm(request.POST or None)
		DetalleFormSet = inlineformset_factory(VentasDocumento, VentasDocumentoDetalle,VentasDetalleDocumentoForm, extra=len(form_initial)+1)
		formset = DetalleFormSet(request.POST or None,initial=form_initial)
		form_crm=PedidoCrmForm(request.POST or None)
		print("-----",formset)

	usuario=request.user
	bdatos = request.session["selected_database"]
	conexion = request.session["conexion_activa"]
	if request.method=='POST':
		if form.is_valid():
			#datos que asignar al formulario que tienen un valor predeterminado
			form.instance.estado='P'
			form.instance.sistema_origen='VE'
			form.instance.modalidad_facturacion=None
			form.instance.metodo_pago_sat=None
			form.instance.modalidad_facturacion=None
			form.instance.metodo_pago_sat=None
			form.instance.uso_cfdi=None
			form.instance.sucursal_id=sucursal_id
			if not venta:
				form.instance.fecha=date.today()
				form.instance.creacion_usuario=usuario.username
			else:
				form.instance.fecha=venta_fecha.fecha
				form.instance.vendedor=venta_fecha.vendedor
				form.instance.creacion_usuario=venta_fecha.creacion_usuario
			if formset.is_valid():
				
				if form_crm.is_valid():
					#si existe descripcion de hadware se reemplaza por la nueva
					descripcion_venta=form.instance.descripcion
					remplazo=form_crm.instance.descripcion_general
					if remplazo:
						sin_hadware=descripcion_venta.replace(remplazo,'')
					else:
						if form.instance.descripcion:
							sin_hadware=form.instance.descripcion
						else:
							sin_hadware=""
					objetos=form_crm.instance.hardware
					hardware=""
					
					if objetos:
						hardware=" se recibio "
						for objeto in objetos:
							if objeto == "OTROS":
								hardware=hardware+form_crm.instance.descripcion_otros.upper()+", "
							else:
								hardware=hardware+objeto+", "

					form.instance.descripcion=sin_hadware+hardware
					hard=form_crm.cleaned_data['hardware']					
					precio_aproximado=form_crm.cleaned_data['precio_aproximado']
					tipo_servicio=form_crm.cleaned_data['tipo_servicio']
					tipo_llamada=form_crm.cleaned_data['tipo_llamada']
					llamada=form_crm.cleaned_data['llamada']
					preprogramado=form_crm.cleaned_data['preprogramado']
					if form_crm.cleaned_data['fecha_registro']:
						fecha_registro=form_crm.cleaned_data['fecha_registro']
					else:
						fecha_registro=datetime.now()

					#datos que asignar al formulario que tienen un valor predeterminado
					if llamada:
						form.instance.tipo='P'
					else:
						form.instance.tipo='R'
					if preprogramado:
						date_=date(fecha_registro.year,fecha_registro.month,fecha_registro.day)
						form.instance.fecha=date_

					#si el formulario tiene la informacion correcta se guarda DOCTOS_VE
					object_save=form.save()
					#si el formulario es valido guardamos el objeto que es DOCTOS_VE en la instancia de DOCTOS_VE_DET
					print(object_save)
					if not venta:
						formset.instance=object_save
						# for f in formset:
						# 	f.instance.documento=object_save
						# 	f.save()

					#se guardan todos los detalles de la venta4
					formset.save()					
					player_ids=[]
					#Creamos el crm para controlar la asignacion de pedidos mandando la instancia					
					if pedido:
						form_crm.save()
						return redirect("/pedidos/pedido/"+str(form_crm.instance.id)+"/")

					else:
						# if ("Ñ").encode('UTF-8') in form.instance.cliente.nombre:
						nombre_cliente=form.instance.cliente.nombre
						content = {"en": "Orden de trabajo de "+str(nombre_cliente)+", click para mas detalles", 
									"es": "Orden de trabajo de "+str(nombre_cliente)+", click para mas detalles"}
							
						headings = {"en": "Hay unan nueva orden de trabajo", 
									"es": "Hay unan nueva orden de trabajo"}
						usuarios=Usuario_notificacion.objects.all().values_list('id_onesignal')
						for usuario in usuarios:
							player_ids.append(str(usuario[0]))
						pedido_crm=Pedidos_Crm.objects.get_or_create(folio=object_save.folio,bdatos=bdatos,conexion=conexion,
						hardware=hard,descripcion_general=hardware,precio_aproximado=precio_aproximado,tipo_servicio=tipo_servicio,
						tipo_llamada=tipo_llamada,llamada=llamada,fecha_registro=fecha_registro,preprogramado=preprogramado,venta=form.instance)

						print(Registry.objects.get(nombre = 'SIC_Pedidos_Crm_App_id' ).get_value())
						print(Registry.objects.get(nombre = 'SIC_Pedidos_Crm_App_api_key' ).get_value())
						app_id = Registry.objects.get(nombre = 'SIC_Pedidos_Crm_App_id' ).get_value()
						app_api_key = Registry.objects.get(nombre = 'SIC_Pedidos_Crm_App_api_key' ).get_value()
						if  app_id and app_api_key:
							servidor=Registry.objects.get(nombre = 'SIC_Pedidos_Crm_Url_servidor' ).get_value()
							# Cargar OneSignal SDK			
							onesignal_client = onesignal_sdk.Client(app_auth_key=app_api_key,app_id=app_id)
							url = "http://"+str(servidor)+"/pedidos/pedido/"+str(pedido_crm[0].venta.folio)+"/"
						else:
							app_id=''
							app_api_key=''
							onesignal_client=None
							url=''	
						if onesignal_client:
							push = send_push_notification (content=content,headings=headings,url=url, player_ids=player_ids,onesignal_client=onesignal_client)
							print(push.status_code)
							print(push.json())
						

			
						return redirect("/pedidos/pedido/"+str(pedido_crm[0].venta.folio)+"/")
					
						# return redirect("/pedidos/nota_pedido/"+str(object_save.id)+"/")


	context={
		'form':form,
		'formset':formset,
		'form_crm':form_crm,
		'articulo_id':id_articulo,
	}
	return render(request, template_name, context)

@login_required(login_url='/login/')
def info_cliente(request):
	#regresa informacion necesaria de un cliente en especifico
	id_cliente=request.GET['id']
	if id_cliente:
		direcciones_cliente = ClienteDireccion.objects.filter(cliente_id=id_cliente)
		cliente_clave = ClienteClave.objects.filter(cliente__id=id_cliente)
		cliente=Cliente.objects.filter(id=id_cliente)[0]
		moneda=cliente.moneda
		condicion_de_pago=cliente.condicion_de_pago
		#print(moneda.id,condicion_de_pago.id)
		print(direcciones_cliente)
	if cliente_clave:
		clave_cliente=cliente_clave[0].clave
	else:
		clave_cliente=""
	lista_direccion={}
	direccion={}

	for direccion_cliente in direcciones_cliente:
		direccion['id'] = direccion_cliente.pk
		direccion['calle'] = direccion_cliente.calle
		direccion['es_ppal'] = direccion_cliente.es_ppal
		lista_direccion[direccion_cliente.pk] = direccion
	data={
		'lista_direccion':lista_direccion,
		'clave':clave_cliente,
		'moneda':moneda.id,
		'condicion_de_pago':condicion_de_pago.id,
		}
	return HttpResponse(json.dumps(data), content_type='application/json')

@login_required(login_url='/login/')
def vendedor_asignar(request):
	#Aqui se asigna el vendedor al pedido
	id_vendedor=request.GET['id_vendedor']
	id_crm=request.GET['id_crm']
	player_ids=[]
	servidor=''
	pedido=Pedidos_Crm.objects.get(folio=id_crm)
	venta=VentasDocumento.objects.get(folio=id_crm)
	if venta:
		vendedor=Vendedor.objects.get(id=id_vendedor)
		venta.vendedor=vendedor
		venta.save()
		mensaje=vendedor.nombre
		data={
			'mensaje':mensaje,
		}
		nombre_cliente=venta.cliente.nombre
		content = {"en": "Has recibido una asignacion para "+nombre_cliente+", click para mas detalles", 
					"es": "Has recibido una asignacion para "+nombre_cliente+", click para mas detalles"}
		headings = {"en": "Asignacion de orden de trabajo", 
					"es": "Asignacion de orden de trabajo"}
		usuarios=Usuario_notificacion.objects.filter(vendedor=vendedor).values_list('id_onesignal')

		for usuario in usuarios:
			player_ids.append(str(usuario[0]))

		app_id = Registry.objects.get(nombre = 'SIC_Pedidos_Crm_App_id' ).get_value()
		app_api_key = Registry.objects.get(nombre = 'SIC_Pedidos_Crm_App_api_key' ).get_value()
		if  app_id and app_api_key:
			servidor=Registry.objects.get(nombre = 'SIC_Pedidos_Crm_Url_servidor' ).get_value()
			# Cargar OneSignal SDK			
			onesignal_client = onesignal_sdk.Client(app_auth_key=app_api_key,app_id=app_id)
			url = "http://"+str(servidor)+"/pedidos/pedido/"+str(id_crm)+"/"
		else:
			app_id=''
			app_api_key=''
			onesignal_client=None
			url=''	

		if onesignal_client:
			push = send_push_notification (content=content,headings=headings,url=url, player_ids=player_ids,onesignal_client=onesignal_client)
			print(push.status_code)
			print(push.json())
		return HttpResponse(json.dumps(data), content_type='application/json')
	else:
		mensaje=""
		data={
			'mensaje':mensaje,
		}
		return HttpResponse(json.dumps(data), content_type='application/json')


@login_required(login_url='/login/')
def get_detalles(request):
	#Envia los detalles por pedido
	id_doc=request.GET['id_doc']
	detalles_venta=VentasDocumentoDetalle.objects.filter(documento__id=id_doc)
	lista_detalle=[]
	#Recorremos la lista de detalles y agrgamos cada detalle a un diccionario para poder serializar la consulta
	for detalle in detalles_venta:
		detalles={}
		detalles['articulo']=detalle.articulo.nombre
		detalles['unidades']=str(detalle.unidades)
		detalles['notas']=detalle.notas
		lista_detalle.append(detalles)

	return HttpResponse(json.dumps(lista_detalle), content_type='application/json')

@login_required(login_url='/login/')
def get_tiempos(request):
	#Tiempos por crm
	#print(request.user)
	folio=request.GET['id_crm']
	print("ff",folio)
	venta=VentasDocumento.objects.filter(folio=folio).first()
	pedido=Pedidos_Crm.objects.filter(venta=venta).first()

	data={}
	if pedido.fecha_inicio:
		#---Tiempo Espera---
		tiempo_espera=pedido.fecha_inicio - pedido.fecha_registro
		#print(tiempo_espera.total_seconds()/3600, "horas")
		data["tiempo_espera"]=formato_tiempo(tiempo_espera)
	if pedido.fecha_fin:
		#---Tiempo Fin---
		tiempo_fin=pedido.fecha_fin - pedido.fecha_inicio
		data["tiempo_fin"]=formato_tiempo(tiempo_fin)
	if pedido.fecha_aviso:
		#---Tiempo Aviso---
		tiempo_aviso=pedido.fecha_aviso - pedido.fecha_fin
		data["tiempo_aviso"]=formato_tiempo(tiempo_aviso)
	if pedido.fecha_entrega:
		#---Tiempo Entrega---
		tiempo_entrega=pedido.fecha_entrega - pedido.fecha_aviso
		data["tiempo_entrega"]=formato_tiempo(tiempo_entrega)

	return HttpResponse(json.dumps(data), content_type='application/json')

def formato_tiempo(time):
	print(time)
	seconds=time.total_seconds()
	dias=seconds/86400
	horas=seconds/3600
	tiempo="{0:.2f} hora(s)".format(horas)
	if horas<1:
		minutos=seconds/60
		tiempo="{0:.2f} minuto(s)".format(minutos)
	elif horas>24:

		tiempo="{0:.2f} dia(s)".format(dias)

	return tiempo

@login_required(login_url='/login/')
def fin_progress(request):
	id_crm=request.GET['id_crm']
	pedido=Pedidos_Crm.objects.filter(id=id_crm)[0]
	if pedido:
		pedido.fecha_inicio=pedido.fecha_registro
		pedido.fecha_fin=pedido.fecha_registro
		pedido.fecha_aviso=pedido.fecha_registro
		print(pedido.fecha_aviso)
		pedido.progreso='100'
		pedido.fecha_entrega=datetime.now()
	
	pedido.save()
	return HttpResponse(json.dumps(pedido.progreso), content_type='application/json')

@login_required(login_url='/login/')
def change_progress(request):
	#cambia el estado dependiendo en cual se encuentre
	id_crm=request.GET['id_crm']
	pedido=Pedidos_Crm.objects.filter(id=id_crm)[0]
	
	if pedido.progreso == '0':
		pedido.progreso='25'
		pedido.fecha_inicio=datetime.now()
	elif pedido.progreso == '25':
		pedido.progreso='50'
		pedido.fecha_fin=datetime.now()
	elif pedido.progreso =='50':
		pedido.progreso='75'
		pedido.fecha_aviso=datetime.now()
	elif pedido.progreso =='75':
		pedido.progreso='100'
		pedido.fecha_entrega=datetime.now()

	pedido.save()
	return HttpResponse(json.dumps(pedido.progreso), content_type='application/json')

@login_required(login_url='/login/')
def return_progress(request):
	#regresar el estado dependiendo en cual se encuentre
	id_crm=request.GET['id_crm']
	pedido=Pedidos_Crm.objects.filter(id=id_crm)[0]

	if pedido.progreso == '25':
		pedido.progreso='0'
		pedido.fecha_inicio=None
	elif pedido.progreso =='50':
		pedido.progreso='25'
		pedido.fecha_fin=None
	elif pedido.progreso =='75':
		pedido.progreso='50'
		pedido.fecha_aviso=None
	elif pedido.progreso =='100':
		pedido.progreso='75'
		pedido.fecha_entrega=None


	pedido.save()
	return HttpResponse(json.dumps(pedido.progreso), content_type='application/json')

@login_required(login_url='/login/')
def inf_articulo(request):
	#regresa informacion del articulo que entra en detalles
	id_articulo=request.GET['id']
	id_cliente=request.GET['id_cliente']
	id_almacen=request.GET['id_almacen']
	data_articulo=GetArticulo(id_articulo,id_cliente,id_almacen)
	id_articulo_reg=Registry.objects.get(nombre='SIC_Pedidos_Crm_Articulo_predeterminado').get_value()
	#print('-----',id_articulo)
	precio_articulo=0
	if id_articulo:
		articulo=ArticuloPrecio.objects.filter(articulo__id=id_articulo)
		clave_articulo=ArticuloClave.objects.filter(articulo__id=id_articulo)
		#print(clave_articulo)
		if articulo:
			if id_articulo == id_articulo_reg:
				precio_articulo = 0
			else: 
				precio_articulo = articulo[0].precio
		else:
			precio_articulo = 0
		if clave_articulo:
			clave=clave_articulo[0].clave
		else:
			clave=''
	data={
			'precio_articulo':str(precio_articulo),
			'clave':clave,
			'existencia':data_articulo["existencia"],
			'descuento':data_articulo["descuento"],
		}
	return HttpResponse(json.dumps(data), content_type='application/json')

def GetArticulo(articulo_id, cliente_id,id_almacen):
	#Manda llamar las existencias y descuentos desde un procedimiento
	try:
		
		using = router.db_for_write(Articulo)
		c = connections[using].cursor()
		c.execute("EXECUTE PROCEDURE CALC_EXIS_ARTALM %s,%s,CURRENT_DATE;" %(articulo_id,id_almacen) )
		print("EXECUTE PROCEDURE CALC_EXIS_ARTALM %s,%s,CURRENT_DATE;" %(articulo_id,id_almacen))
		existencia=c.fetchall()[0][0]
		c.execute("SELECT * FROM GET_POLS_DSCTO_ARTCLI (%s,%s,CURRENT_DATE) where descuento>0;"%(articulo_id,cliente_id))
		print("SELECT * FROM GET_POLS_DSCTO_ARTCLI (%s,%s,CURRENT_DATE) where descuento>0;"%(articulo_id,cliente_id))
		descuento=c.fetchall()[0][1]
		data={
			"existencia":str(existencia),
			"descuento":str(descuento),
		}
		c.close()
	except Exception as e:
		print(e)
		data={
			"existencia":str(0),
			"descuento":str(0),
		}
	return (data)

def actualiza_base_datos(request):
	using = router.db_for_write(Pedidos_Crm)
	fields_exist=[]
	bandera=False
	data={}
	#app = apps.get_app('djmicrosip_orden_trabajo')

	

	try:
		c = connections[using].cursor()
		# c.execute("CREATE GENERATOR SIC_PEDIDOS_CRM_SQ")
		# c.execute("CREATE TABLE SIC_PEDIDOS_CRM ("+
		# 		    "CRM_ID               INTEGER NOT NULL,"+
		# 		    "FECHA_HORA_REGISTRO  TIMESTAMP NOT NULL,"+
		# 		    "FECHA_HORA_INICIO    TIMESTAMP,"+
		# 		    "PROGRESO             VARCHAR(3) NOT NULL,"+
		# 		    "FECHA_META           TIMESTAMP,"+
		# 		    "FECHA_MODIFICACION   TIMESTAMP,"+
		# 		    "FECHA_AVISO          TIMESTAMP,"+
		# 		    "FECHA_FIN            TIMESTAMP,"+
		# 		    "FECHA_ENTREGA        TIMESTAMP,"+
		# 		    "NOTA                 BLOB SUB_TYPE 1 SEGMENT SIZE 80,"+
		# 		    "BASE_DATOS           VARCHAR(250) NOT NULL,"+
		# 		    "CONEXION             VARCHAR(10) NOT NULL,"+
		# 		    "HARDWARE             VARCHAR(49) NOT NULL,"+
		# 		    "DESC_OTROS           BLOB SUB_TYPE 1 SEGMENT SIZE 80,"+
		# 		    "PRECIO_APROXIMADO    DOUBLE PRECISION,"+
		# 		    "DESC_GENERAL         BLOB SUB_TYPE 1 SEGMENT SIZE 80,"+
		# 		    "SIC_FIRMA_URL        VARCHAR(100),"+
		# 		    "TIPO_SERVICIO        VARCHAR(50),"+
		# 		    "LLAMADA              SMALLINT NOT NULL,"+
		# 		    "TIPO_LLAMADA         VARCHAR(50),"+
		# 		    "FOLIO                VARCHAR(9),"+
		# 		    "ENVIO_CORREO         SMALLINT,"+
		# 		    "PREPROGRAMADO        SMALLINT,"+
		# 		    "VENTA                INTEGER,"+
		# 		    "SOLICITUD            SMALLINT"+
		# 			")")
						

		for field in Pedidos_Crm._meta.fields:
			fields_exist.append(field.get_attname_column()[1])
			data[field.get_attname_column()[1]]={"campo":field.db_type(connections[using]),"null":field.null,"default":field.default}
		col_names = []
		# management.call_command('migrate', database=using, interactive=False)
		
		c.execute("SELECT * FROM SIC_PEDIDOS_CRM")

		for desc in enumerate(c.description):
			col_names.append(desc[1][0])
		
		diferencia=list(set(fields_exist)- set(col_names))
		dif_contraria=list(set(col_names)- set(fields_exist))
		campos_add=""
		print(diferencia)
		if diferencia:
			for campo in diferencia:
				print(campo)
				if data[campo]["null"]:
					campos_add=campos_add+" ADD "+campo+" "+data[campo]["campo"]+","
				else:
					if data[campo]["campo"] == "smallint":
						campos_add=campos_add+" ADD "+campo+" "+data[campo]["campo"]+","
					else:
						campos_add=campos_add+" ADD "+campo+" "+data[campo]["campo"]+" NOT NULL,"

			temp = len(campos_add)
			campos_add=campos_add[:temp - 1]
			print(campos_add)
			if campos_add:
				consulta="ALTER TABLE SIC_PEDIDOS_CRM "+campos_add+";"
				c.execute(consulta)
				connections[using].commit()		


		if dif_contraria:
			print(dif_contraria)
			for campo in dif_contraria:
				print(campo)
				if campo=="DOCTOS_VE_ID":
					c.execute("DROP INDEX SIC_PEDIDOS_CRM_9D1423F5")
					c.execute("ALTER TABLE SIC_PEDIDOS_CRM DROP CONSTRAINT DOCTOS_VE_ID_REFS_DOCTO_VE_3CD6")
				consulta_="ALTER TABLE SIC_PEDIDOS_CRM DROP "+campo+";"
				print(consulta_)
				c.execute(consulta_)
				connections[using].commit()	
		# print("table")		
		# c.execute("CREATE GENERATOR SIC_CLIENTE_USUARIO_SQ")
		# c.execute("CREATE TABLE SIC_CLIENTE_USUARIO ("+
		# 		    "CLIENTE_USUARIO_ID  INTEGER NOT NULL,"+
		# 		    "CLIENTE_ID          INTEGER,"+
		# 		    "USUARIO_ID          INTEGER"+
		# 			")")
		# print("GENERATOR")		
		
		# print("Index and foreing")
		# c.execute("ALTER TABLE SIC_CLIENTE_USUARIO ADD PRIMARY KEY (CLIENTE_USUARIO_ID)")
		# c.execute("ALTER TABLE SIC_CLIENTE_USUARIO ADD CONSTRAINT CLIENTE_ID_REFS_CLIENTE_ID_D1E1 FOREIGN KEY (CLIENTE_ID) REFERENCES CLIENTES (CLIENTE_ID) ON DELETE CASCADE")
		# # c.execute("CREATE INDEX SIC_CLIENTE_USUARIO_1D8B2AF5 ON SIC_CLIENTE_USUARIO (CLIENTE_ID)")
		
		# c.execute("CREATE OR ALTER TRIGGER SIC_CLIENTE_USUARIO_PK FOR SIC_CLIENTE_USUARIO "+
		# 			"ACTIVE BEFORE INSERT POSITION 0 "+
		# 			"AS "+
		# 			"BEGIN "+
		# 			"   IF(new.CLIENTE_USUARIO_ID IS NULL) THEN "+
		# 			"      new.CLIENTE_USUARIO_ID = NEXT VALUE FOR SIC_CLIENTE_USUARIO_SQ; "+
		# 			"END")

		c.execute("CREATE OR ALTER trigger sic_update_orden_de_trabajo for doctos_ve "+
					"active before update position 0 "+
					"AS "+
					"DECLARE VARIABLE EXISTE INTEGER; "+
					"begin "+
					"Select Count(*) from sic_pedidos_crm where folio=NEW.folio into EXISTE; "+
					"IF (EXISTE > 0) THEN "+
					      "update sic_pedidos_crm set venta=NEW.docto_ve_id where folio=new.folio; "+
					"end")
		c.execute("CREATE OR ALTER procedure SIC_RELA_ORDTRAB_DOCTOS_VE "+
					"as "+
					"declare variable DOCTO_VE_ID integer; "+
					"declare variable FOLIO varchar(9); "+
					"declare variable LCCONTINUAR char(1); "+
					"declare VENTA cursor for ( "+
					"    select VE.DOCTO_VE_ID, PE.FOLIO "+
					"    from DOCTOS_VE VE "+
					"    inner join SIC_PEDIDOS_CRM PE on PE.FOLIO = VE.FOLIO); "+
					"BEGIN "+
					"OPEN venta; "+
					"lccontinuar='S'; "+
					"WHILE (lccontinuar = 'S')  DO "+
					"   BEGIN "+
					"    FETCH venta INTO :docto_ve_id,:folio; "+
					"    IF (ROW_COUNT=1) THEN begin "+
					"       update sic_pedidos_crm set venta= :DOCTO_VE_ID where folio= :FOLIO; "+
					"    end else "+
					"        lcContinuar = 'N'; "+
					"   END "+
					"CLOSE venta; "+
					"END")


		c.close()
	except Exception as e:
		c.close()
		print(e)
	
	padre = first_or_none(Registry.objects.filter(nombre='PreferenciasEmpresa'))
	if not Registry.objects.filter( nombre = 'SIC_Pedidos_Crm_Articulo_predeterminado' ).exists():
			Registry.objects.create(
				nombre = 'SIC_Pedidos_Crm_Articulo_predeterminado',
				tipo = 'V',
				padre = padre,
				valor= '',
			)
	if not Registry.objects.filter( nombre = 'SIC_Pedidos_Crm_Logo' ).exists():
			Registry.objects.create(
				nombre = 'SIC_Pedidos_Crm_Logo',
				tipo = 'V',
				padre = padre,
				valor= '',
			)
	if not Registry.objects.filter( nombre = 'SIC_Pedidos_Crm_Imagen_extra' ).exists():
			Registry.objects.create(
				nombre = 'SIC_Pedidos_Crm_Imagen_extra',
				tipo = 'V',
				padre = padre,
				valor= '',
			)
	if not Registry.objects.filter( nombre = 'SIC_Pedidos_Crm_Url_Pdf_Destino' ).exists():
			Registry.objects.create(
				nombre = 'SIC_Pedidos_Crm_Url_Pdf_Destino',
				tipo = 'V',
				padre = padre,
				valor= '',
			)
	if not Registry.objects.filter( nombre = 'SIC_Pedidos_Crm_Email' ).exists():
			Registry.objects.create(
				nombre = 'SIC_Pedidos_Crm_Email',
				tipo = 'V',
				padre = padre,
				valor= '',
			)
	if not Registry.objects.filter( nombre = 'SIC_Pedidos_Crm_Password' ).exists():
			Registry.objects.create(
				nombre = 'SIC_Pedidos_Crm_Password',
				tipo = 'V',
				padre = padre,
				valor= '',
			)
	if not Registry.objects.filter( nombre = 'SIC_Pedidos_Crm_Servidro_Correo' ).exists():
			Registry.objects.create(
				nombre = 'SIC_Pedidos_Crm_Servidro_Correo',
				tipo = 'V',
				padre = padre,
				valor= '',
			)
	if not Registry.objects.filter( nombre = 'SIC_Pedidos_Crm_Puerto' ).exists():
			Registry.objects.create(
				nombre = 'SIC_Pedidos_Crm_Puerto',
				tipo = 'V',
				padre = padre,
				valor= '',
			)
	if not Registry.objects.filter( nombre = 'SIC_Pedidos_Crm_App_id' ).exists():
			Registry.objects.create(
				nombre = 'SIC_Pedidos_Crm_App_id',
				tipo = 'V',
				padre = padre,
				valor= '',
			)
	if not Registry.objects.filter( nombre = 'SIC_Pedidos_Crm_App_api_key' ).exists():
			Registry.objects.create(
				nombre = 'SIC_Pedidos_Crm_App_api_key',
				tipo = 'V',
				padre = padre,
				valor= '',
			)
	if not Registry.objects.filter( nombre = 'SIC_Pedidos_Crm_Url_servidor' ).exists():
			Registry.objects.create(
				nombre = 'SIC_Pedidos_Crm_Url_servidor',
				tipo = 'V',
				padre = padre,
				valor= '',
			)


	return redirect("/pedidos/preferencias/")

def preferencias(request):
	id_articulo=Registry.objects.get(nombre='SIC_Pedidos_Crm_Articulo_predeterminado').get_value()
	logo = Registry.objects.get( nombre = 'SIC_Pedidos_Crm_Logo').get_value()
	imagen_extra = Registry.objects.get( nombre = 'SIC_Pedidos_Crm_Imagen_extra').get_value()
	url_pdf_destino = Registry.objects.get( nombre = 'SIC_Pedidos_Crm_Url_Pdf_Destino').get_value()
	email= Registry.objects.get( nombre = 'SIC_Pedidos_Crm_Email').get_value()
	password= Registry.objects.get( nombre = 'SIC_Pedidos_Crm_Password').get_value()
	servidor_correo= Registry.objects.get( nombre = 'SIC_Pedidos_Crm_Servidro_Correo').get_value()
	puerto= Registry.objects.get( nombre = 'SIC_Pedidos_Crm_Puerto').get_value()
	app_id= Registry.objects.get( nombre = 'SIC_Pedidos_Crm_App_id').get_value()
	app_api_key= Registry.objects.get( nombre = 'SIC_Pedidos_Crm_App_api_key').get_value()
	url_servidor= Registry.objects.get( nombre = 'SIC_Pedidos_Crm_Url_servidor').get_value()
	articulo=Articulo.objects.filter(id=id_articulo)
	form_initial=None
	if articulo:
		form_initial = {
			'articulo':articulo[0],
			'logo':logo,
			'imagen_extra':imagen_extra,
			'url_pdf_destino':url_pdf_destino,
			'email':email,
			'password':password,
			'servidor_correo':servidor_correo,
			'puerto':puerto,
			'app_id':app_id,
			'app_api_key':app_api_key,
			'url_servidor':url_servidor,
		}

	form = PreferenciasManageForm(request.POST or None,initial=form_initial)
	if form.is_valid():
		form.save()

	context = {
		'form': form,
	}
	return render(request, 'djmicrosip_orden_trabajo/preferencias.html', context)

def create_pdf(id_doc):
	venta=first_or_none(VentasDocumento.objects.filter(id=id_doc))
	logo = Registry.objects.get( nombre = 'SIC_Pedidos_Crm_Logo').get_value()
	imagen_extra = Registry.objects.get( nombre = 'SIC_Pedidos_Crm_Imagen_extra').get_value()
	pedido=first_or_none(Pedidos_Crm.objects.filter(folio=venta.folio))
	folio=venta.folio
	venta.folio=none_cero(folio)
	#Sacamos los datos pertinentes de la empresa desde la tabla Registry
	datos_empresa = Registry.objects.get(nombre='DatosEmpresa')
	datos_empresa = Registry.objects.filter(padre=datos_empresa)
	nombre=datos_empresa.get(nombre='Nombre').get_value()
	calle=datos_empresa.get(nombre='NombreCalle').get_value()
	num_ext=datos_empresa.get(nombre='NumExterior').get_value()
	colonia=datos_empresa.get(nombre='Colonia').get_value()
	telefono1=datos_empresa.get(nombre='Telefono1').get_value()
	telefono2=datos_empresa.get(nombre='Telefono2').get_value()
	rfc=datos_empresa.get(nombre='Rfc').get_value()
	curp=datos_empresa.get(nombre='CurpEmpresa').get_value()
	if not telefono2:
		telefono2=""
	email=datos_empresa.get(nombre='Email').get_value()
	poblacion=datos_empresa.get(nombre='Poblacion').get_value()
	#Generamos un diccionario con la informacion de la empresa
	empresa={
		"nombre":nombre,
		"calle":calle,
		"num_ext":num_ext,
		"colonia":colonia,
		"telefono1":telefono1,
		"telefono2":telefono2,
		"email":email,
		"poblacion":poblacion,
		"rfc":rfc,
		"curp":curp,
	}
	if venta:
		venta_detalles=VentasDocumentoDetalle.objects.filter(documento__id=id_doc)
	else:
		venta_detalles=None
	context={
		"venta":venta,
		"venta_detalles":venta_detalles,
		"empresa":empresa,
		"pedido":pedido,
		"MEDIA_URL":settings.MEDIA_ROOT,
		"logo":logo,
		"imagen_extra":imagen_extra,
	}
	nombre=venta.folio+".pdf"
	# template = get_template('djmicrosip_orden_trabajo/nota_pedido.html')
	# html  = template.render(Context(context))
	# result = StringIO.StringIO()
	
	# file = open(os.path.join(settings.MEDIA_ROOT, 'test.pdf'), "w+b")
	# pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)
	# if not pdf.err: 
	# 	return HttpResponse(result.getvalue(), content_type='application/pdf')
	# return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))
	
	template_path = 'djmicrosip_orden_trabajo/nota_pedido.html'
	# encontrar la plantilla y renderizarla.
	template = get_template(template_path)
	html = template.render(context)
	destination = Registry.objects.get( nombre = 'SIC_Pedidos_Crm_Url_Pdf_Destino').get_value()
	file = open(destination+"\\" + nombre, "w+b")
	# response['Content-Disposition'] = 'attachment; filename='+file+''
	# crear pdf
	pisaStatus = pisa.CreatePDF(StringIO(html), dest=file, encoding='UTF-8')

	file.seek(0)
	pdf = file.read()
	file.close()
	# if pisaStatus.err:
	#    return HttpResponse('Hubo error al crear PDF <pre>' + html + '</pre>')
	# return HttpResponse(content_type='application/pdf')


	#return render(request, 'djmicrosip_orden_trabajo/nota_pedido.html', context)

	return pdf

def nota_pedido(request,id_doc):
	pdf=create_pdf(id_doc)

	return HttpResponse(pdf,content_type='application/pdf')

def firma(request,id_crm):
	#Se recibe el nuemro de pedido crm para guardar la firma en el pedido especifico
	pedido=Pedidos_Crm.objects.get(id=id_crm)
	#print(pedido)
	form=FirmaForm(request.POST, request.FILES,instance=pedido)
	if request.method == 'POST':		
		if form.is_valid():
			if request.POST.get("data_image"):
				#Si hay datos en el canvas se crea una imagen y se guarda en el servidor
				data_url_pattern = re.compile('data:image/(png|jpeg);base64,(.*)$')
				signature_url = request.POST.get("data_image")
				signature_data = data_url_pattern.match(signature_url).group(2)
				signature_data = bytes(signature_data, encoding='utf8')
				signature_data = decodestring(signature_data)
				img_io = io.BytesIO(signature_data)
				url=str(pedido.firma).replace("pedidos_crm/","")
				if pedido.firma:
					pedido.firma.save(url, File(img_io))
				else:
					form.instance.firma.save("firma"+none_cero(pedido.folio)+".png", File(img_io))
				#return redirect("/pedidos/")

	context={
		'form':form,
		'pedido':pedido,
	}
	return render(request, 'djmicrosip_orden_trabajo/firma.html', context)

def enviar_correo(request):
	id_crm=request.GET['id']
	pedido=Pedidos_Crm.objects.get(id=id_crm)
	venta=VentasDocumento.objects.get(folio=pedido.folio)
	cliente=ClienteDireccion.objects.get(cliente=venta.cliente)
	destinatarios=(cliente.email).split(';')
	email= Registry.objects.get( nombre = 'SIC_Pedidos_Crm_Email').get_value()
	password= Registry.objects.get( nombre = 'SIC_Pedidos_Crm_Password').get_value()
	servidor_correo= Registry.objects.get( nombre = 'SIC_Pedidos_Crm_Servidro_Correo').get_value()
	puerto= Registry.objects.get( nombre = 'SIC_Pedidos_Crm_Puerto').get_value()
	#superkarelyrubio@hotmail.com
	nombre=none_cero(venta.folio)+".pdf"
	pdf=create_pdf(venta.id)
	destination = Registry.objects.get( nombre = 'SIC_Pedidos_Crm_Url_Pdf_Destino').get_value()
	file=destination+"\\" + nombre
	data={}
	bandera=send_mail_orden(servidor_correo,puerto,email,password,destinatarios,"Nota de servicio","<p>Servicios de Ingenieria</p>",file,nombre)
	if bandera:
		pedido.envio_correo=1
		print(pedido.envio_correo)
		pedido.save()
		data["mensaje"]="Correo Enviado"
		print(data)
	else:
		data["mensaje"]="Hubo un error al enviar el correo"
		print(data)

	return HttpResponse(json.dumps(data), content_type='application/json')

def lista_vendedores(request):
	vendedores=Vendedor.objects.all()
	context={
		'vendedores':vendedores,
	}
	return render(request, 'djmicrosip_orden_trabajo/lista_vendedores.html', context)


def configuracion_usuarios_onesignal(request,id_vendedor):
	vendedor=Vendedor.objects.get(id=id_vendedor)
	UsuarioFormSet = inlineformset_factory( Vendedor,Usuario_notificacion,form=UsuarioOneSignalForm ,extra=1)
	usuarios=Usuario_notificacion.objects.all().values_list('id_onesignal')
	print(usuarios)
	print(vendedor)
	if vendedor:
		formset = UsuarioFormSet(request.POST or None,instance=vendedor)
	else:
		formset = UsuarioFormSet(request.POST or None)
	if request.method=='POST':
		if formset.is_valid():
			formset.save()
			
	context={
		'vendedor':vendedor,
		'formset':formset,
	}
	return render(request, 'djmicrosip_orden_trabajo/configuracion.html', context)

def search_id(request):
	id_onesignal=request.GET['id']
	print(id_onesignal)
	usuario=Usuario_notificacion.objects.filter(id_onesignal=id_onesignal)
	if usuario:
		mensaje="El id de este dispositivo ya esta siendo usado por otro usuario"
	else:
		mensaje="Disponible"
	return HttpResponse(json.dumps(mensaje), content_type='application/json')

def send_push_notification(content,headings,url,player_ids,onesignal_client):
	print("---------------")
	print(player_ids)
	new_notification = onesignal_sdk.Notification(post_body={
		"contents": content,
		"include_player_ids":player_ids,
		"headings": headings,
		"url":url,
		})
	# new_notification.set_parameter("include_player_ids",player_ids)
	# new_notification.set_parameter("headings", headings)
	# new_notification.set_parameter("url", url)
	# send notification, it will return a response
	onesignal_response = onesignal_client.send_notification(new_notification)
	return onesignal_response

def send_notifications_preprogramadas(request):
	hoy=datetime.today()
	ahora=datetime.now()
	inicio=datetime(hoy.year,hoy.month,hoy.day,0,0)
	fin=datetime(hoy.year,hoy.month,hoy.day,23,59)
	ordenes_trabajo=Pedidos_Crm.objects.filter(preprogramado=True,fecha_registro__gte=inicio,fecha_registro__lte=fin)
	servidor=''
	for orden in ordenes_trabajo:
		time_orden=orden.fecha_registro - timedelta(hours=1)
		if ahora >= time_orden:
			if ahora < orden.fecha_registro:
				player_ids=[]
				tiempo_restante=orden.fecha_registro-ahora
				venta=VentasDocumento.objects.get(folio=orden.folio)
				nombre_cliente=(venta.cliente.nombre).encode('UTF-8')
				print("Orden de trabajo preprogramada de "+nombre_cliente+" faltan "+formato_tiempo(tiempo_restante)+" ")


				content = {"en": "Orden de trabajo preprogramada de "+nombre_cliente+" faltan "+formato_tiempo(tiempo_restante)+" ", 
							"es": "Orden de trabajo preprogramada de "+nombre_cliente+" faltan "+formato_tiempo(tiempo_restante)+" "}
				if venta.vendedor:
					headings = {"en": "Recordatorio", 
								"es": "Recordatorio"}
					usuarios=Usuario_notificacion.objects.filter(vendedor=venta.vendedor).values_list('id_onesignal')
				else:
					headings = {"en": "Recordatorio(orden no asignada)", 
								"es": "Recordatorio(orden no asignada)"}
					usuarios=Usuario_notificacion.objects.all().values_list('id_onesignal')
				print(headings)
				for usuario in usuarios:
					player_ids.append(str(usuario[0]))
				
				app_id = Registry.objects.get(nombre = 'SIC_Pedidos_Crm_App_id' ).get_value()
				app_api_key = Registry.objects.get(nombre = 'SIC_Pedidos_Crm_App_api_key' ).get_value()
				if  app_id and app_api_key:
					servidor=Registry.objects.get(nombre = 'SIC_Pedidos_Crm_Url_servidor' ).get_value()
					# Cargar OneSignal SDK			
					onesignal_client = onesignal_sdk.Client(app_auth_key=app_api_key,app_id=app_id)
					url = "http://"+str(servidor)+"/pedidos/pedido/"+str(id_crm)+"/"
				else:
					app_id=''
					app_api_key=''
					onesignal_client=None
					url=''	
				if onesignal_client:
					push = send_push_notification (content=content,headings=headings,url=url, player_ids=player_ids,onesignal_client=onesignal_client)
					print(push.status_code)
					print(push.json())

	return HttpResponse()



def usuario_cliente(request):
	clientes=Cliente.objects.filter(estatus='A')

	page = request.GET.get('page')

	form_busqueda=FilterForm(request.POST or None)
	
	if form_busqueda.is_valid():
		busqueda=form_busqueda.cleaned_data['busqueda']
		print(busqueda)
		if busqueda:
			clientes=clientes.filter(nombre__icontains=busqueda)

	paginator = Paginator(clientes, 50) 
	try:
		clientes = paginator.page(page)
	except PageNotAnInteger:
		
		clientes = paginator.page(1)
	except EmptyPage:
		
		clientes = paginator.page(paginator.num_pages)

	for cliente in clientes:
		cliente_usuario=first_or_none(ClienteUsuario.objects.filter(cliente=cliente))
		if cliente_usuario:
			client_usuario=first_or_none(User.objects.filter(id=cliente_usuario.usuario))
			cliente.usuario=client_usuario

	clientes_usuario=User.objects.all()
	
	context = {
		"clientes_usuario":clientes_usuario,
		"clientes":clientes,
		"form_busqueda":form_busqueda,
	}
	
	return render(request, 'djmicrosip_orden_trabajo/usuarios_clientes.html', context)

def pedido_solictud(request):
	usuario=request.user
	cliente=ClienteDireccion.objects.filter(rfc_curp=usuario.username,es_ppal='S').first()
	print(cliente)
	form=PedidoAddForm(request.POST or None)
	context={}
	return render(request, 'djmicrosip_orden_trabajo/solicitud.html', context)

def lista_solicitudes(request):
	context={}
	return render(request, 'djmicrosip_orden_trabajo/lista_solicitudes.html', context)

