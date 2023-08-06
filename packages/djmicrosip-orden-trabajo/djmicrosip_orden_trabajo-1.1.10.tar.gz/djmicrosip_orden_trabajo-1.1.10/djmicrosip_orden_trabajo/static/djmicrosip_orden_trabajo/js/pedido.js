var primera_ocacion=false;
$(document).ready(function(){
	// Al inicializar el html se cargann valores predeterminados y se esconde campos que trabajaran en segundo plano

	$('#id_condicion_pago').val(242);
	$('#id_moneda').val(1);
	$('#id_almacen').val(19);
	$('#id_tipo_cambio').addClass('hidden');
	$('#id_descuento_importe').addClass('hidden');
	$('#lbl_descuento_importe').addClass('hidden');
	$('.autocomplete').addClass('form-control');
	$('#id_direccion_consignatario').addClass('hidden');
	$('#id_descripcion_otros').addClass('hidden');
	$('#lblOtros').addClass('hidden');
	$('#id_descripcion').addClass('hidden');
	$(".add-row").addClass("glyphicon glyphicon-plus-sign");
	$("#id_llamada").trigger("change");
	$("#id_preprogramado").trigger("change");
	if($('#id_cliente').val())
	{
		$("#listas_detalle").removeClass("hidden");
		$("#importes").removeClass("hidden");
		$('#descripcion_compra').val($('#id_descripcion').val());
		$("#det_extra").trigger("click");
		$("#id_hardware_6").trigger("change");
		if($('#id_condicion_pago').val() == null)
		{$('#id_condicion_pago').val(854);}
		total();
	}
	$('#id_fecha_registro').attr("autocomplete","off");
    $('#id_fecha_registro').datetimepicker({
        format:'d/m/Y H:m',
        inline:false
    });
    $("select[name*='-articulo']").trigger("change");
	});
$(document).click(function(e){
	$(".delete-row").addClass("glyphicon glyphicon-remove");
	var e = $('.delete-row').slice(-1);
	if (!primera_ocacion)
	{$(e).trigger("click"); primera_ocacion=true;}
	
});

$("#guardar").click(function(e){

	$( this ).prop( "disabled", true );
	$('.form').submit();
	});

$("#det_extra").click(function(e){
	//Si al darle click al boton ver esta activo se muestran los detalle si no desaparecen
	if($("#det_extra i").hasClass("glyphicon-eye-open"))
	{
		$("#detalles_extra").removeClass("hidden");
		$("#det_extra i").removeClass("glyphicon-eye-open");
		$("#det_extra i").addClass("glyphicon-eye-close");
	}
	else
	{
		$("#detalles_extra").addClass("hidden");
		$("#det_extra i").addClass("glyphicon-eye-open");
		$("#det_extra i").removeClass("glyphicon-eye-close");
	}
	
});
$( document ).hover(
  function() {
   $(".delete-row").addClass("glyphicon glyphicon-remove");
   	var e = $('.delete-row').slice(-1);
	if (!primera_ocacion)
	{$(e).trigger("click"); primera_ocacion=true;}
  }
);
	function foco_detalle(){
		//Valores predeterminados para detalle de pedido
		$("[name*='-unidades']").last().val(1);
		$("[name*='-precio_unitario']").last().val(0);
		$("[name*='-precio_total_neto']").last().val(0);
		$("[name*='-descuento_porcentaje']").last().val(0);
		$("input[name*='-articulo_text']").last().focus();
		$("[name*='-precio_total_neto']").attr("readonly","true");
		$("#id_importe_neto").attr("readonly","true");
		$(".delete-row").addClass("glyphicon glyphicon-remove");

	}

	$('#id_hardware_6').change(function() {
		var value=$(this).attr("checked");
		console.log(value);
		if (value)
		{
			$('#id_descripcion_otros').removeClass("hidden");
	    	$('#lblOtros').removeClass('hidden');
	    	$("#id_descripcion_otros").prop('required',true);
		}
		else
		{
			$('#id_descripcion_otros').addClass("hidden");
	    	$('#lblOtros').addClass('hidden');
	    	$("#id_descripcion_otros").prop('required',false);
		}
	    
	  });
	$('#id_llamada').change(function() {
		var value=$(this).attr("checked");
		console.log(value);
		if (value)
		{
			$('#tipo_llamada').removeClass("hidden");	    	
	    	$("#tipo_llamada").prop('required',true);
		}
		else
		{
			$('#tipo_llamada').addClass("hidden");
	    	$("#tipo_llamada").prop('required',false);
		}
 	});
	$('#id_preprogramado').change(function() {
		var value=$(this).attr("checked");
		console.log(value);
		if (value)
		{
			$('#fecha').removeClass("hidden");	    	
	    	$("#fecha").prop('required',true);
		}
		else
		{
			$('#fecha').addClass("hidden");
	    	$("#fecha").prop('required',false);
		}
 	});
	$("#descripcion_compra").on("input",function(){
		console.log($(this).val());
		$('#id_descripcion').val($(this).val());
	});
	$("#id_descuento_tipo").on("change",function(){
		total();
	});
	$("select[name*='-articulo']").on("change",function(){
		

		var id=$( this ).attr('id');
		var id_articulo=$( this ).val();
		var id_unidades = id.replace("articulo", "unidades");
		var id_precio_unitario = id.replace("articulo", "precio_unitario");
		var id_descuento_porcentaje = id.replace("articulo", "descuento_porcentaje");
		var id_precio_total_neto = id.replace("articulo", "precio_total_neto");
		var id_articulo_clave=id.replace("articulo","articulo_clave");
		var unidades=$("#"+id_unidades).val();
		var id_cliente=$("#id_cliente").val();
		var id_almacen=$("#id_almacen").val();

		if (id_articulo) {
		$.ajax({
		url: '/pedidos/inf_articulo/',
		type: 'get',
		data: {
		'id': id_articulo,
		'id_cliente': id_cliente,
		'id_almacen': id_almacen,
		},
		success: function (data) {
			console.log(id_precio_unitario)
		
				var tipo_cambio=$("#id_tipo_cambio").val();
				
				if(data.existencia==0)
				{
					$("#"+id_unidades).addClass('alert alert-danger');
					$("#"+id_unidades).attr('data-toggle','tooltip');
					$("#"+id_unidades).attr('data-placement','top');
					$("#"+id_unidades).attr('title','Existencia = '+data.existencia);

				}
				$("#"+id_articulo_clave).val(data.clave);
				$("#"+id_precio_unitario).val((parseFloat(data.precio_articulo)*tipo_cambio).toFixed(2))
				$("#"+id_unidades).attr('src',data.existencia);
				$("#"+id_unidades).val(1)
				$("#"+id_precio_total_neto).val((parseFloat(data.precio_articulo)*tipo_cambio).toFixed(2))
				if (parseFloat(data.descuento)>0) 
				{
					debugger
					$("#"+id_descuento_porcentaje).val(parseFloat(data.descuento).toFixed(2));
					$("[name*='-descuento_porcentaje']").trigger("input");
				}
				
				total();
				console.log()
			}
		});
		} else {
	
		}	

	});
	$("[name*='-unidades']").on("input",function(){

		var id=$( this ).attr('id');
		var id_precio_total_neto = id.replace("unidades", "precio_total_neto");
		var id_precio_unitario = id.replace("unidades", "precio_unitario");
		var id_descuento_porcentaje = id.replace("unidades", "descuento_porcentaje");
		var precio_unitario=$("#"+id_precio_unitario).val();
		var descuento_porcentaje=$("#"+id_descuento_porcentaje).val();
		var unidades=$(this).val();
		var existencia=parseInt($( this ).attr('src'));
		var descuento_des=descuento_porcentaje/100
		var total_neto=unidades*precio_unitario;
		var total_neto_descuento=total_neto-(total_neto*descuento_des);
		$("#"+id_precio_total_neto).val(total_neto_descuento.toFixed(2))
		total();
		if(unidades>existencia)
		{
			$(this).addClass('alert alert-danger');
			$(this).attr('data-toggle','tooltip');
			$(this).attr('data-placement','top');
			$(this).attr('title','Existencia = '+existencia);

		}
		else
		{
			$(this).removeClass('alert alert-danger');
			$(this).attr('data-toggle','');
			$(this).attr('data-placement','');
			$(this).attr('title','');
		}
	});
	$("[name*='-precio_unitario']").on("input",function(){
		var id=$( this ).attr('id');
		var id_precio_total_neto = id.replace("precio_unitario", "precio_total_neto");
		var id_unidades = id.replace("precio_unitario", "unidades");
		var id_descuento_porcentaje = id.replace("precio_unitario", "descuento_porcentaje");
		var descuento_porcentaje=$("#"+id_descuento_porcentaje).val();
		var unidades=$("#"+id_unidades).val();
		var precio_unitario=$(this).val();
		
		var descuento_des=descuento_porcentaje/100
		var total_neto=unidades*precio_unitario;
		var total_neto_descuento=total_neto-(total_neto*descuento_des);

		$("#"+id_precio_total_neto).val(total_neto_descuento.toFixed(2))
		total();
	});	
	$("[name*='-descuento_porcentaje']").on("input",function(){

		var id=$( this ).attr('id');
		var id_precio_total_neto = id.replace("descuento_porcentaje", "precio_total_neto");
		var id_unidades = id.replace("descuento_porcentaje", "unidades");
		var id_precio_unitario = id.replace("descuento_porcentaje", "precio_unitario");
		var precio_unitario=$("#"+id_precio_unitario).val();
		var unidades=$("#"+id_unidades).val();
		var descuento_porcentaje=$(this).val();
		
		var descuento_des=descuento_porcentaje/100
		var total_neto=unidades*precio_unitario;
		var total_neto_descuento=total_neto-(total_neto*descuento_des);

		$("#"+id_precio_total_neto).val(total_neto_descuento.toFixed(2))
		total();
	});
	$("#id_descuento_importe").on("input",function(){
			total();
	});
	$("#id_descuento_porcentaje").on("input",function(){
			total();
	});
	$( "#id_cliente" ).change(function() {
	id_cliente= $( this ).val();
	direcciones(id_cliente);
	});
	$( "#id_moneda" ).on("change",function(){
		debugger;
		var moneda=$(this).val();
		console.log(moneda)
		if (moneda==198)
		{
			$.ajax({
			url: 'https://free.currconv.com/api/v7/convert?q=MXN_USD&compact=ultra&apiKey=6c643c5c01ca6033463d',
			type: 'get',
			success: function (data) {
					if(data.MXN_USD)
					{$("#id_tipo_cambio").val(data.MXN_USD)}
				}
			});
		}
		else if(moneda==3596)
		{
			$.ajax({
			url: 'https://free.currconv.com/api/v7/convert?q=MXN_EUR&compact=ultra&apiKey=6c643c5c01ca6033463d',
			type: 'get',
			success: function (data) {
					if(data.MXN_EUR)
					{$("#id_tipo_cambio").val(data.MXN_EUR);}
				}
			});
		}

		else if(moneda==3597)
		{
			$.ajax({
			url: 'https://free.currconv.com/api/v7/convert?q=MXN_GBP&compact=ultra&apiKey=6c643c5c01ca6033463d',
			type: 'get',
			success: function (data) {
					if(data.MXN_GBP)
					{$("#id_tipo_cambio").val(data.MXN_GBP);}
				}
			});
		}
		else
			{$("#id_tipo_cambio").val(1);}
		
	});
	function cambio_moneda()
	{	var moneda_value= $("#id_tipo_cambio").val()
		$( "input[id*='-precio_unitario']" ).each(function() {
		
				var precio_unitario=$( this ).val();
				
				var cambio_precio=precio_unitario*moneda_value;
				$( this ).val(cambio_precio);
				
		});
	}
	function direcciones(id_cliente){
		if (id_cliente) {
		$.ajax({
		url: '/pedidos/info_cliente/',
		type: 'get',
		data: {
		'id': id_cliente
		},
		success: function (data) {
			if(data)
			{
				$('#id_cliente_direccion').html(`<option value="">---------</option>`);
				$('#id_direccion_consignatario').html(`<option value="">---------</option>`);
				for (direccion in data.lista_direccion) {
				$('#id_cliente_direccion').append(`<option ${(data.lista_direccion[direccion].es_ppal == 'S') ? 'selected="selected"' : ''} value="${data.lista_direccion[direccion].id}">${data.lista_direccion[direccion].calle}</option>`);
				$('#id_direccion_consignatario').append(`<option ${(data.lista_direccion[direccion].es_ppal == 'S') ? 'selected="selected"' : ''} value="${data.lista_direccion[direccion].id}">${data.lista_direccion[direccion].calle}</option>`);
				}
						
				$('#id_cliente_clave').val(data.clave);
				console.log(data.condicion_de_pago)
				if(data.condicion_de_pago)
				{
					$('#id_condicion_pago').val(data.condicion_de_pago);					
				}
				else
				{
					$('#id_condicion_pago').val(852);
				}
				$('#id_moneda').val(data.moneda);
				$("#id_moneda").trigger("change");
				$("#listas_detalle").removeClass("hidden");
				$("#importes").removeClass("hidden");


			}

		}
		});
		} else {
		$('#id_cliente_direccion').val(null);
		$('#id_cliente_direccion').html(`<option value="">---------</option>`);
		$('#id_cliente_clave').val(null);
		$('#id_condicion_pago').val(null);
		$('#id_moneda').val(null);
		$("#listas_detalle").addClass("hidden");
		$("#importes").addClass("hidden");
		}

	}
	function total()
	{
		var importe_neto=0;
		var importe_sin_descuento=0;
		$( "input[id*='-precio_total_neto']" ).each(function() {
	
			var precio_total_neto=parseFloat($( this ).val());
			importe_sin_descuento=importe_sin_descuento+precio_total_neto;

		});
		
		var descuento_tipo=$("#id_descuento_tipo").val();
		if(descuento_tipo=="P")
		{
			$("#id_descuento_porcentaje").removeClass('hidden');
			$('#lbl_descuento_porcentaje').removeClass('hidden');
			$("#id_descuento_importe").addClass('hidden');
			$('#lbl_descuento_importe').addClass('hidden');
			var descuento_porcentaje=$("#id_descuento_porcentaje").val();
			var descuento_importe=(importe_sin_descuento*(descuento_porcentaje/100)).toFixed(2)
			importe_neto=importe_sin_descuento-descuento_importe;
			$("#id_descuento_importe").val(descuento_importe);
			$("#descuento_importe").val(descuento_importe);
		}
		else
		{
			$("#id_descuento_porcentaje").addClass('hidden');
			$('#lbl_descuento_porcentaje').addClass('hidden');
			$("#id_descuento_importe").removeClass('hidden');
			$('#lbl_descuento_importe').removeClass('hidden');
			var descuento_importe=$("#id_descuento_importe").val();
			importe_neto=importe_sin_descuento-descuento_importe;
			$("#id_descuento_importe").val(descuento_importe);
			$("#descuento_importe").val(descuento_importe);
		}
		$('#id_importe_neto').val(importe_neto.toFixed(2));
		$('#importe_sin_descuento').val(importe_sin_descuento.toFixed(2));
	}
