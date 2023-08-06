function none_cero(folio) {
    
    var indice_inicio=0
    var indice_fin=0
    var x=0
    while(indice_inicio == 0)
    {
        if (folio[x] == "0") {indice_inicio=x}
        x=x+1;

    }
    
    x=indice_inicio;
    while(indice_fin == 0)
    {
        if (folio[x] != "0") {indice_fin=x}
        x=x+1
    }
    
    remplazar=folio.substr(indice_inicio,indice_fin-1)
    folio_nuevo=folio.replace(remplazar, "")

    return folio_nuevo
}

function Pedido(ventas,ligas) {
	debugger;
  var html='<div class="row fila header"> <div class="col-lg-1 col-md-1 col-xs-4 col-sm-1"> <label>Folio</label> </div> <div class="col-lg-1 col-md-1 col-xs-4 col-sm-1"> <label>Fecha</label> </div> <div class="col-lg-3 col-md-3 col-xs-4 col-sm-3"> <label>Detalles</label> </div> <div class="col-lg-3 col-md-3 col-xs-3 col-sm-3"> <label>Cliente</label> </div> <div class="col-lg-3 col-md-3 col-xs-3 col-sm-3"> <label>Vendedor</label> </div> <div class="col-lg-1"> <label><span>R</span><span style="margin-left: 12px;">F</span>  </label> </div> </div> </div>'
  $("#listas_detalle").append(html);
  for (var i = 0; i < ventas.length; i++) {
    var fol=ventas[i][1];
    Detalle_(ventas[i][1]).then((pedido) => {
      var si_llamada='';
      var remisionado='';
      var facturado='';
      var envio_correo='';
      	 
      var div = document.createElement("div");
      var folio=none_cero(pedido["venta_folio"]);
      if( pedido["llamada"])
      {
      	if(pedido["tipo_llamada"]== "PENDIENTE")
      		{
      			si_llamada='<a style="color: red;" class="glyphicon glyphicon-phone-alt"></a>';
      		}
      	else
      		{
      			si_llamada='<a style="color: green;" class="glyphicon glyphicon-phone-alt"></a>';
      		}

      }
      if(pedido["venta_estado"]=='S')
      	{remisionado='checked';}
      if(pedido["venta_estado"]=='F')
      	{facturado='checked';}
      if(ligas != null)
      {
      	if(ligas.includes(pedido["venta_id"]))
      		{facturado='checked';}

      }
      if(pedido["enviar_correo"])
      {
        envio_correo='<a style="color: green;" title="Enviar correo" href="#" class="glyphicon glyphicon-send send_correo" id="'+pedido["id"]+'"></a>'
      }
      else
      {
         envio_correo='<a style="color: red;" title="Enviar correo" href="#" class="glyphicon glyphicon-send send_correo" id="'+pedido["id"]+'"></a> '
      }
      div.setAttribute('class', 'row fila '+pedido["id"]+'');
      div.innerHTML=
        '<div  class="steps"> <div class="col-lg-1 col-md-1 col-xs-4 col-sm-1"> <label class="lbl">Folio</label>'+si_llamada+'<span id="'+pedido["venta_id"]+'" class="glyphicon glyphicon-triangle-right more hidden-print" aria-hidden="true"></span> <a class="hidden-print" href="/pedidos/pedido/'+pedido["id"]+'/">'+folio+' </a> </div> <div class="col-lg-1 col-md-1 col-xs-4 col-sm-1"> <label class="lbl">Fecha</label> '+pedido["fecha_registro"]+' </div> <div class="col-lg-3 col-md-3 col-xs-4 col-sm-3"> <label class="lbl">Detalles</label> <a id="'+pedido["id"]+'" class="hidden-print det_progreso" href="#" data-toggle="modal" data-target="#myModal'+pedido["id"]+'">Mas</a> <div class="modal fade '+pedido["id"]+'" id="myModal'+pedido["id"]+'" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> <div class="modal-dialog"> <div class="modal-content"> <div class="modal-header"> <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button> <h4 class="modal-title" id="myModalLabel">Detalles</h4> </div> <div class="modal-body"> <div class="row"> <div class="col-lg-12 col-md-12 col-xs-12 col-sm-12"> <label class="">Descripcion</label> '+pedido["venta_descripcion"]+' </div> <div class="col-lg-6 col-md-6 col-xs-6 col-sm-6"> <br> <label class="">Nota</label> <div style="display: flex;"> <a href="/pedidos/nota_pedido/'+pedido["venta_id"]+'/" target="_blank" class="glyphicon glyphicon-print"></a>&nbsp; <a href="/pedidos/firma/'+pedido["id"]+'/" target="_blank" class="glyphicon glyphicon-edit">Firma</a> &nbsp;&nbsp;'+envio_correo+'</div> </div> <div class="col-lg-12 col-md-12 col-xs-12 col-sm-12"> <br> <label class="">Progreso</label> <div class="vendedor_asignado hidden" id="ven'+pedido["id"]+'"> <a id="'+pedido["id"]+'" style="position: relative; float: right;" class="hidden-print det_progreso" href="#" data-toggle="modal" data-target="#myModal">Detalles</a> <br> <div id='+pedido["id"]+' class="progress prog'+pedido["id"]+'" data-value="'+pedido["progreso"]+'"> <span id='+pedido["id"]+' class="progress-item" data-width="'+pedido["progreso"]+'%" >'+pedido["progreso"]+'% </span> </div> <div id="change_state'+pedido["id"]+'" class="hidden" style="display: flex; justify-content: center; align-items: center; margin-bottom: 5px;"> <a id="'+pedido["id"]+'" class="btn return_state"></a> <a id="'+pedido["id"]+'" class="btn change_state"></a> <a id="'+pedido["id"]+'" class="btn fin_state hidden"></a> </div> </div> <div class="vendedor_sinasignar hidden" id="vensin'+pedido["id"]+'"> No se asigno vendedor aun </div> </div> </div> </div> <div class="modal-footer"> <button type="button" class="btn btn-default" data-dismiss="modal">Cerrar</button> <!-- <button type="button" class="btn btn-primary">OK</button> --> </div> </div> </div> </div> </div> </div> <div class="steps"> <div class="col-lg-3 col-md-3 col-xs-7 col-sm-3"> <label class="lbl">Cliente</label> '+pedido["venta_cli_nombre"]+'</div> <div class="col-lg-3 col-md-3 col-xs-5 col-sm-3 ss" id="'+pedido["id"]+'"> <label class="lbl">Vendedor</label> <span class="hidden" name="venta_ven" id="'+pedido["id"]+'">'+pedido["vendedor_id"]+'</span> <div class="vendedor_asignado hidden" id="ven'+pedido["id"]+'"> <a  id="'+pedido["id"]+'" class="guardar btn'+pedido["id"]+' glyphicon glyphicon-ok-sign hidden"></a> <a  id="'+pedido["id"]+'" class="cancelar btncancel'+pedido["id"]+' glyphicon glyphicon-remove-sign hidden"></a> <a  id="'+pedido["id"]+'" class="hidden-print asignar asign'+pedido["id"]+' glyphicon glyphicon-pencil"></a> <span id="'+pedido["id"]+'" class="vendedor_asign'+pedido["id"]+'"> '+pedido["venta_vendedor"]+' </span> </div> <div class="vendedor_sinasignar hidden" id="vensin'+pedido["id"]+'"> <a  id="'+pedido["id"]+'" class="guardar btn'+pedido["id"]+' glyphicon glyphicon-ok-sign hidden"></a> <a  id="'+pedido["id"]+'" class="cancelar btncancel'+pedido["id"]+' glyphicon glyphicon-remove-sign hidden"></a> <a  id="'+pedido["id"]+'" class="asignar asign'+pedido["id"]+'">Asignar</a> </div> '+pedido["form"]+' </div> </div> <div class="steps"> <div class="col-lg-1"> <label class="lbl"><span>R</span><span style="margin-left: 12px;">F</span>  </label> <input type="checkbox" id="r'+pedido["venta_id"]+'" name="remisionado" '+remisionado+' onclick="this.checked=!this.checked;"> <input type="checkbox" id="f'+pedido["venta_id"]+'" name="facturado"'+facturado+' onclick="this.checked=!this.checked;"> </div> </div> <div class="detalles det'+pedido["venta_id"]+' hidden fila"> <div class="row"> <div class="col-lg-4 col-md-4 col-xs-4 col-sm-4"><strong>Unidades</strong></div> <div class="col-lg-4 col-md-4 col-xs-4 col-sm-4"><strong>Articulo</strong></div> <div class="col-lg-4 col-md-4 col-xs-4 col-sm-4"><strong>Nota</strong></div> </div> <div class="row" id="contenido" data-value="Quiubo"> </div> </div>';   
      $("#listas_detalle").append(div);

		var id_crm=pedido["id"];
		var $this=$(".prog"+id_crm+" span.progress-item");
		console.log(pedido["progreso"])
		
		$($this).css("width",pedido["progreso"]+"%");
		
		if(pedido["progreso"]=="25")
		{$($this).css("background-color","#dc3545");
		$(".fila."+id_crm).css("background","#ff00004d");}
		else if(pedido["progreso"]=="50")
		{$($this).css("background-color","#ff9007");
		$(".fila."+id_crm).css("background","#ffa5004d");}
		else if(pedido["progreso"]=="75")
		{$($this).css("background-color","#ffc107");
		$(".fila."+id_crm).css("background","#ffff004d");}
		else if(pedido["progreso"]=="100")
		{$($this).css("background-color","#28a745");
		$(".fila."+id_crm).css("background","#0080004d");
		}
		else
		{$(".fila."+id_crm).css("background","#ffffff");}		
		//in_progres(pedido["progreso"],this,pedido["id"]);     	

      	var vendedor=pedido["venta_vendedor"];
		console.log(vendedor);
		var id=pedido["id"];

		if(vendedor == null)
		{
			$('#ven'+id+'.vendedor_asignado').addClass("hidden");
			$('#vensin'+id+'.vendedor_sinasignar').removeClass("hidden");
		}
		else
		{
			$('#ven'+id+'.vendedor_asignado').removeClass("hidden");
			$('#vensin'+id+'.vendedor_sinasignar').addClass("hidden");
		}
  });
	if(i==ventas.length)
	{
      	//alert(i);    
      	$("#left").removeClass('hidden');
  		$("#right").removeClass('hidden');
       
	}
}
  $("#guardar").removeClass('hidden');
}
function Detalle_(folio) {
 return fetch(`/pedidos/get_pedido/?folio=${folio}`, {
   method: 'GET',
   credentials: 'same-origin'
 })
 .then((response) => {
   if(response.ok) {
     return response.json();
   } else {
     throw new Error('Server response wasn\'t OK');
   }
 })
 .then((json) => {
   const pedido=json;
   return pedido;
 });
}
function Venta(page) {
	debugger;
  $("#left").addClass('hidden');
  $("#right").addClass('hidden');
  $("#guardar").addClass('hidden');
  
  $("#listas_detalle").empty();
  var busqueda=$("#id_busqueda").val();
  var llamada= $("#id_llamada").prop('checked');
  if (llamada){llamada=1;}else{llamada=0;}
  var tipo_documento= $("#id_tipo_documento").val();
  var filtro= $("#id_filtro").val();
  var inicio= $("#id_inicio").val();
  var fin = $("#id_fin").val();
 
 fetch(`/pedidos/get_venta/?busqueda=${busqueda}&llamada=${llamada.toString()}&tipo_documento=${tipo_documento}&filtro=${filtro}&inicio=${inicio}&fin=${fin}&page=${page}`, {
   method: 'GET',
   credentials: 'same-origin'
 })
 .then((response) => {
   if(response.ok) {
     return response.json();
   } else {
     throw new Error('Server response wasn\'t OK');
   }
 })
 .then((json) => {
   const response=json;
   	Pedido(response.ventas,response.ligas);
  	if(response.numero_pagina==1)
  		{var left='';}
  	else
  		{var left='<a class="glyphicon glyphicon-triangle-left" id="left"></a>';}
  	if(response.numero_pagina==response.total_paginas)
  		{var right='';}
  	else
  		{var right='<a id="right" class="glyphicon glyphicon-triangle-right"></a>';}
  	$(".step-links").empty(); 
  	$(".step-links").append(left+'<span class="current">Pagina <strong id="numero_paginas">'+response.numero_pagina +'</strong> de '+response.total_paginas+' </span>'+right);
 });
}
function Guardar(page) {
	debugger;
  $("#left").addClass('hidden');
  $("#right").addClass('hidden');
  
  $("#listas_detalle").empty();
  var busqueda=$("#id_busqueda").text();
  var llamada= $("#id_llamada").prop('checked');
  var tipo_documento= $("#id_tipo_documento").val();
  var filtro= $("#id_filtro").val();
  var inicio= $("#id_inicio").val();
  var fin = $("#id_fin").val();


  var url = '/pedidos/get_venta/';
  var data = {
            'page':page,
            'busqueda':busqueda,
            'llamada':llamada,
            'tipo_documento':tipo_documento,
            'filtro':filtro,
            'inicio':inicio,
            'fin':fin, 
            };
  fetch(url, {
    method: 'POST', // or 'PUT'
    body: JSON.stringify(data), // data can be `string` or {object}!
    headers:{
      'Content-Type': 'application/json'
    }
  }).then(res => res.json())
  .catch(error => console.error('Error:', error))
  .then(response => {
  	Pedido(response.ventas,response.ligas);
  	if(response.numero_pagina==1)
  		{var left='';}
  	else
  		{var left='<a class="glyphicon glyphicon-triangle-left" id="left"></a>';}
  	if(response.numero_pagina==response.total_paginas)
  		{var right='';}
  	else
  		{var right='<a id="right" class="glyphicon glyphicon-triangle-right"></a>';}
  	$(".step-links").empty(); 
  	$(".step-links").append(left+'<span class="current">Pagina <strong id="numero_paginas">'+response.numero_pagina +'</strong> de '+response.total_paginas+' </span>'+right);
  });

	
}

$( "#guardar" ).click(function(){
  //$(this).addClass('hidden');
 

});


function in_progres(width,$this,id_crm) {
	
		$($this).css("width",width);
		if(width=="25%")
		{$($this).css("background-color","#dc3545");
		$(".fila."+id_crm).css("background","#ff00004d");}
		else if(width=="50%")
		{$($this).css("background-color","#ff9007");
		$(".fila."+id_crm).css("background","#ffa5004d");}
		else if(width=="75%")
		{$($this).css("background-color","#ffc107");
		$(".fila."+id_crm).css("background","#ffff004d");}
		else if(width=="100%")
		{$($this).css("background-color","#28a745");
		$(".fila."+id_crm).css("background","#0080004d");
		}
		else
		{$(".fila."+id_crm).css("background","#ffffff");}
}

function Cargar() {
	debugger;
	$( ".progress-item" ).each(function() {
		var width=$(this).attr("data-width");
		var id_crm=$(this).attr("id");
		
		in_progres(width,this,id_crm);


	});
	$( "[name*='vendedor']" ).each(function() {
		$(this).addClass("hidden");
		var number=$(this).parent().attr("id");
		$(this).addClass("pedido"+number);
	});
  $( "[class*='folio_ven']" ).each(function() {
    var folio=$(this).text();
    var envio_correo='';
    var si_llamada='';
    $(this).text(none_cero(folio));
/*    Detalle_(folio).then((pedido) => {
      if(pedido["enviar_correo"])
      {
        envio_correo='<a style="color: green;" title="Enviar correo" href="#" class="glyphicon glyphicon-send send_correo" id="'+pedido["id"]+'"></a>'
      }
      else
      {
         envio_correo='<a style="color: red;" title="Enviar correo" href="#" class="glyphicon glyphicon-send send_correo" id="'+pedido["id"]+'"></a> '
      }
      if( pedido["llamada"])
      {
        if(pedido["tipo_llamada"]== "PENDIENTE")
          {
            si_llamada='<a style="color: red;" class="glyphicon glyphicon-phone-alt"></a>';
          }
        else
          {
            si_llamada='<a style="color: green;" class="glyphicon glyphicon-phone-alt"></a>';
          }

      }      
       console.log(pedido)
       var venta_id=pedido["venta_id"];
       var div='<div class="row"> <div class="col-lg-12 col-md-12 col-xs-12 col-sm-12"> <label class="">Descripcion</label>'+pedido["venta_descripcion"] +' </div> <div class="col-lg-6 col-md-6 col-xs-6 col-sm-6"> <br> <label class="">Nota</label> <div style="display: flex;"> <a href="/pedidos/nota_pedido/'+pedido["venta_id"] +'/" target="_blank" class="glyphicon glyphicon-print"></a>&nbsp; <a href="/pedidos/firma/'+pedido["id"] +'/" target="_blank" class="glyphicon glyphicon-edit">Firma</a> '+ enviar_correo+'"></a> </div> </div> <div class="col-lg-12 col-md-12 col-xs-12 col-sm-12"> <br> <label class="">Progreso</label> <div class="vendedor_asignado hidden" id="ven'+pedido["id"] +'"> <a id="'+pedido["venta_folio"] +'" style="position: relative; float: right;" class="hidden-print det_progreso" href="#" data-toggle="modal" data-target="#myModal">Detalles</a> <br> <div id='+pedido["id"] +' class="progress prog'+pedido["id"] +'" data-value="'+pedido["progreso"] +'"> <span id='+pedido["id"] +' class="progress-item" data-width="'+pedido["progreso"] +'%" >'+pedido["progreso"] +'% </span> </div> <div id="change_state'+pedido["id"] +'" class="hidden" style="display: flex; justify-content: center; align-items: center; margin-bottom: 5px;"> <a id="'+pedido["id"] +'" class="btn return_state"></a> <a id="'+pedido["id"] +'" class="btn change_state"></a> <a id="'+pedido["id"] +'" class="btn fin_state hidden"></a> </div> </div> <div class="vendedor_sinasignar hidden" id="vensin'+pedido["id"] +'"> No se asigno vendedor aun </div> </div> </div>'
      $("#"+venta_id+".modal-body").append(div);
      var id_crm=pedido["id"];
      var $this=$(".prog"+id_crm+" span.progress-item");
      console.log(pedido["progreso"])
      
      $($this).css("width",pedido["progreso"]+"%");
      
      if(pedido["progreso"]=="25")
      {$($this).css("background-color","#dc3545");
      $(".fila."+id_crm).css("background","#ff00004d");}
      else if(pedido["progreso"]=="50")
      {$($this).css("background-color","#ff9007");
      $(".fila."+id_crm).css("background","#ffa5004d");}
      else if(pedido["progreso"]=="75")
      {$($this).css("background-color","#ffc107");
      $(".fila."+id_crm).css("background","#ffff004d");}
      else if(pedido["progreso"]=="100")
      {$($this).css("background-color","#28a745");
      $(".fila."+id_crm).css("background","#0080004d");
      }
      else
      {$(".fila."+id_crm).css("background","#ffffff");}   
      });*/
    //console.log(folio);
  });

	$( "[name*='venta_ven']" ).each(function() {

		var vendedor=$(this).text();
		
		var id=$(this).attr("id");

		if(vendedor == 'None')
		{
			$('#ven'+id+'.vendedor_asignado').addClass("hidden");
			$('#vensin'+id+'.vendedor_sinasignar').removeClass("hidden");
		}
		else
		{
			$('#ven'+id+'.vendedor_asignado').removeClass("hidden");
			$('#vensin'+id+'.vendedor_sinasignar').addClass("hidden");
		}
	});	
}
$(document).ready(function(){
	$("#menu").hide();
    $('#id_inicio').datetimepicker({
        format:'d/m/Y',
        inline:false
    });
    $('#id_fin').datetimepicker({
        format:'d/m/Y',
        inline:false
    });
    $('#id_inicio').attr("autocomplete","off");
	$('#id_fin').attr("autocomplete","off");
	//Venta(1);

	Cargar();

});
/*$('#id_llamada').change(function() {
	$('.form').submit();
});*/
$( document ).on("click", ".send_correo", function() {
	$(".banner_carga").removeClass("hidden");
	$(".all_").addClass("hidden");
	var id_crm=$(this).attr("id");

		$.ajax({
		url: '/pedidos/enviar_correo/',
		type: 'get',
		data: {
		'id': id_crm,
		},
		success: function (data) {
			alert(data.mensaje)
			$(".banner_carga").addClass("hidden");
			$(".all_").removeClass("hidden");

			}
		});
});
$( document ).on("click", "#left", function() {
	var page = parseInt($("#numero_paginas").text())-1;
	Venta(page);
});
$( document ).on("click", "#right", function() {
	var page = parseInt($("#numero_paginas").text())+1;
	Venta(page);
});
$( document ).on("click", ".asignar", function() {

  var number=$(this).attr("id");
  $(this).addClass("hidden");
  
  $(".pedido"+number).removeClass("hidden");
  $(".btncancel"+number).removeClass("hidden");
  $(".vendedor_asign").addClass("hidden");

 
});
$( document ).on("click", ".cancelar", function() {

  var number=$(this).attr("id");
  $(this).addClass("hidden");
  $(".pedido"+number).addClass("hidden");
  $(".asign"+number).removeClass("hidden");
  $(".btn"+number).addClass("hidden");
  $(".vendedor_asign"+number).removeClass("hidden");
 
});
$( document ).on("click", ".guardar", function() {
	var id_crm=$(this).attr("id");
	var id_cliente=$(".pedido"+id_crm).val();

	
	
 	if(id_crm && id_vendedor)
	{
		$.ajax({
		url: '/pedidos/vendedor_asignar/',
		type: 'get',
		data: {
			'id_vendedor': id_cliente,
			'id_crm':id_crm,
		},
		success: function (data) {
				if(data.mensaje!="")
				{
					$('.cancelar').trigger("click");
					$('span.vendedor_asign'+id_crm).text(data.mensaje);
					$('#ven'+id_crm+'.vendedor_asignado').removeClass("hidden");
					$('#vensin'+id_crm+'.vendedor_sinasignar').addClass("hidden");
				}
				else
				{alert(data.mensaje)}				
			}
		});
	}
 
});
function progreso_(id_crm,progreso)
{	$(".fin_state").addClass("hidden");
		
		if(progreso=="0")
	{
		$("#change_state"+id_crm+" .return_state").addClass("hidden");
		$("#change_state"+id_crm).removeClass("hidden");
		$("#change_state"+id_crm+" .change_state").css("background-color","#dc3545");
		$("#change_state"+id_crm+" .change_state").html('Inicio <span class="glyphicon glyphicon-step-forward" aria-hidden="true"></span>');
		$(".fin_state").removeClass("hidden");
		$("#change_state"+id_crm+" .fin_state").css("background-color","#28a745");
		$("#change_state"+id_crm+" .fin_state").html('Entregado <span class="glyphicon glyphicon-step-forward" aria-hidden="true"></span>');
	}	
	else if(progreso=="25")
	{
		$("#change_state"+id_crm).removeClass("hidden");
		$("#change_state"+id_crm+" .return_state").removeClass("hidden");
		$("#change_state"+id_crm+" .change_state").css("background-color","#ff9007");
		$("#change_state"+id_crm+" .change_state").html('Finalizado <span class="glyphicon glyphicon-step-forward" aria-hidden="true"></span>');
		$("#change_state"+id_crm+" .return_state").css("background-color","#ccc");
		$("#change_state"+id_crm+" .return_state").html('<span class="glyphicon glyphicon-step-backward" aria-hidden="true"> Recibido');
	}
	else if(progreso=="50")
	{
		$("#change_state"+id_crm).removeClass("hidden");
		$("#change_state"+id_crm+" .return_state").removeClass("hidden");
		$("#change_state"+id_crm+" .change_state").css("background-color","#ffc107");
		$("#change_state"+id_crm+" .change_state").html('Aviso a cliente <span class="glyphicon glyphicon-step-forward" aria-hidden="true"></span>');
		$("#change_state"+id_crm+" .return_state").css("background-color","#dc3545");
		$("#change_state"+id_crm+" .return_state").html('<span class="glyphicon glyphicon-step-backward" aria-hidden="true"> Inicio');
	}
	else if(progreso=="75")
	{
		$("#change_state"+id_crm).removeClass("hidden");
		$("#change_state"+id_crm+" .return_state").removeClass("hidden");
		$("#change_state"+id_crm+" .change_state").css("background-color","#28a745");
		$("#change_state"+id_crm+" .change_state").html('Entregado <span class="glyphicon glyphicon-step-forward" aria-hidden="true"></span>');
		$("#change_state"+id_crm+" .return_state").css("background-color","#ff9007");
		$("#change_state"+id_crm+" .return_state").html('<span class="glyphicon glyphicon-step-backward" aria-hidden="true"> Finalizado');
	}
	else{
		$("#change_state"+id_crm).removeClass("hidden");
		$("#change_state"+id_crm+" .return_state").removeClass("hidden");
		$(".fin_state").addClass("hidden");
		$("#change_state"+id_crm+" .return_state").css("background-color","#ffc107");
		$("#change_state"+id_crm+" .return_state").html('<span class="glyphicon glyphicon-step-backward" aria-hidden="true"> Aviso a cliente');
	}
}
$(document ).on("touchstart",".progress",function(){
	var id_crm=$(this).attr("id");
	var progreso=$(this).attr("data-value");

	progreso_(id_crm,progreso);
});

$(document).on("dblclick",".progress",function() {
	var id_crm=$(this).attr("id");
	var progreso=$(this).attr("data-value");

	progreso_(id_crm,progreso);


	//alert(id_crm)

});
$( document ).on("click", ".fin_state", function() {
	var id_crm=$(this).attr("id");
	 if(id_crm)
	{
		$.ajax({
		url: '/pedidos/fin_progress/',
		type: 'get',
		data: {
			'id_crm':id_crm,
		},
		success: function (data) {
			if(data != "")
			{
				in_progres(data+"%","span#"+id_crm+".progress-item",id_crm);
				$("span#"+id_crm+".progress-item").text(data+"%");
				progreso_(id_crm,data);
			}
			else
			{alert(data.mensaje)}	
		}
		});
	}
});
$( document ).on("click", ".change_state", function() {
	var id_crm=$(this).attr("id");
	 if(id_crm)
	{
		$.ajax({
		url: '/pedidos/change_progress/',
		type: 'get',
		data: {
			'id_crm':id_crm,
		},
		success: function (data) {
			if(data != "")
			{
				in_progres(data+"%","span#"+id_crm+".progress-item",id_crm);
				$("span#"+id_crm+".progress-item").text(data+"%");
				progreso_(id_crm,data);
			}
			else
			{alert(data.mensaje)}	
		}
		});
	}
});
$( document).on("click",  ".return_state", function() {
	var id_crm=$(this).attr("id");
	 if(id_crm)
	{
		$.ajax({
		url: '/pedidos/return_progress/',
		type: 'get',
		data: {
			'id_crm':id_crm,
		},
		success: function (data) {
			if(data != "")
			{
				in_progres(data+"%","span#"+id_crm+".progress-item",id_crm);
				$("span#"+id_crm+".progress-item").text(data+"%");
				
				progreso_(id_crm,data);
			}
			else
			{alert(data.mensaje)}	
		}
		});
	}
});
$(document).on("change","[name*='vendedor']",function(){
	var valor=$(this).val();
	var number=$(this).parent().attr("id");
	if(valor != '')
	{	
		$(".btn"+number).removeClass("hidden");
	}
	else
	{$(".btn"+number).addClass("hidden");}
});
$(document ).on("click",".more", function() {
	debugger;
	var id_doc=$(this).attr("id");
	if($(this).hasClass("glyphicon-triangle-right"))
	{
		$(this).removeClass("glyphicon-triangle-right");
		$(this).addClass("glyphicon-triangle-bottom");
		$(".det"+id_doc).removeClass("hidden");
		$('.det'+id_doc+' #contenido').empty();


		$.ajax({
		url: '/pedidos/get_detalles/',
		type: 'get',
		data: {
			'id_doc': id_doc,
		},
		success: function (data) {
				
				for (var i = 0; i <= data.length-1; i++) {
					var html='<div class="col-lg-12 col-md-12 col-xs-12 col-sm-12"><div class="col-lg-4 col-md-4 col-xs-4 col-sm-4">'+data[i].unidades+'</div><div class="col-lg-4 col-md-4 col-xs-4 col-sm-4">'+data[i].articulo +'</div><div class="col-lg-4 col-md-4 col-xs-4 col-sm-4">'+data[i].notas+'</div></div>'
					$('.det'+id_doc+' #contenido').append(html);
				}
			}
		});
	}
	else
	{
		$(this).addClass("glyphicon-triangle-right");
		$(this).removeClass("glyphicon-triangle-bottom");
		$(".det"+id_doc).addClass("hidden");
	}
});
$( document ).on("click", ".det_progreso", function() {
	var id_crm=$(this).attr("id");
	$("#tiempo_espera").html('');
	$("#tiempo_fin").html('');
	$("#tiempo_aviso").html('');
	$("#tiempo_entrega").html('');
	if (id_crm)
	{
		$.ajax({
		url: '/pedidos/get_tiempos/',
		type: 'get',
		data: {
			'id_crm': id_crm,
		},
		success: function (data) {

					if(data)
					{	
						if(data.tiempo_espera)
						{$("#tiempo_espera").html(data.tiempo_espera);}
						if(data.tiempo_fin)
						{$("#tiempo_fin").html(data.tiempo_fin);}
						if(data.tiempo_aviso)
						{$("#tiempo_aviso").html(data.tiempo_aviso);}
						if(data.tiempo_entrega)	
						{$("#tiempo_entrega").html(data.tiempo_entrega);}
					}
			}
		});
	}

});