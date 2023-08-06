var canvas = document.getElementById("canvas");
var ctx = canvas.getContext("2d");
function sleep(delay) {
    var start = new Date().getTime();
    while (new Date().getTime() < start + delay);
}
function clearCanvas() {
    canvas.width = canvas.width;
}
function sendToServer() {
    debugger;
    
  var data = canvas.toDataURL("image/png");
    
    if (data)
    {
    $('#id_data_image').val(data);
    $('.form').submit();
/*    sleep(10000);
    window.close();*/
  }
}
(function() { // Comenzamos una funcion auto-ejecutable
// Configuracion canvas


var s = getComputedStyle(canvas);
var w = s.width;
var h = s.height;
ctx.canvas.width = w.split('px')[0];
ctx.canvas.height = h.split('px')[0];


// Eventos de mouse
var drawing = false;
var mousePos = { x:0, y:0 };
var lastPos = mousePos;
canvas.addEventListener("mousedown", function (e) {
        drawing = true;
  lastPos = getMousePos(canvas, e);
}, false);
canvas.addEventListener("mouseup", function (e) {
  drawing = false;
}, false);
canvas.addEventListener("mousemove", function (e) {
  mousePos = getMousePos(canvas, e);
}, false);

// Tomar posicion relativa del canvas
function getMousePos(canvasDom, mouseEvent) {
  var rect = canvasDom.getBoundingClientRect();
  return {
    x: mouseEvent.clientX - rect.left,
    y: mouseEvent.clientY - rect.top
  };
}
// Obtenga un intervalo regular para dibujar en la pantalla
window.requestAnimFrame = (function (callback) {
        return window.requestAnimationFrame || 
           window.webkitRequestAnimationFrame ||
           window.mozRequestAnimationFrame ||
           window.oRequestAnimationFrame ||
           window.msRequestAnimaitonFrame ||
           function (callback) {
        window.setTimeout(callback, 2);
           };
})();
// Dibujar en el lienzo
function renderCanvas() {
  if (drawing) {
    ctx.beginPath();
    ctx.moveTo(lastPos.x, lastPos.y);
    ctx.lineTo(mousePos.x, mousePos.y);
    ctx.lineWidth = 3;
    ctx.strokeStyle = "#000000";
    ctx.stroke();
    ctx.closePath();
    lastPos = mousePos;
  }
}

// Permitir animación
(function drawLoop () {
  requestAnimFrame(drawLoop);
  renderCanvas();
})();

// Configure eventos táctiles para dispositivos móviles, etc.
canvas.addEventListener("touchstart", function (e) {
        mousePos = getTouchPos(canvas, e);
      e.preventDefault();
  var touch = e.touches[0];
  var mouseEvent = new MouseEvent("mousedown", {
    clientX: touch.clientX,
    clientY: touch.clientY
  });
  canvas.dispatchEvent(mouseEvent);
}, false);
canvas.addEventListener("touchend", function (e) {
  e.preventDefault();
  var mouseEvent = new MouseEvent("mouseup", {});
  canvas.dispatchEvent(mouseEvent);
}, false);
canvas.addEventListener("touchmove", function (e) {
  e.preventDefault();
  var touch = e.touches[0];
  var mouseEvent = new MouseEvent("mousemove", {
    clientX: touch.clientX,
    clientY: touch.clientY
  });
  canvas.dispatchEvent(mouseEvent);
}, false);

// Obtener la posición de un toque en relación con el lienzo
function getTouchPos(canvasDom, touchEvent) {
  var rect = canvasDom.getBoundingClientRect();
  return {
    x: touchEvent.touches[0].clientX - rect.left,
    y: touchEvent.touches[0].clientY - rect.top
  };
}

// Evita el desplazamiento al tocar el lienzo
document.body.addEventListener("touchstart", function (e) {
  if (e.target == canvas) {
    e.preventDefault();
  }
}, false);
document.body.addEventListener("touchend", function (e) {
  if (e.target == canvas) {
    e.preventDefault();
  }
}, false);
document.body.addEventListener("touchmove", function (e) {
  if (e.target == canvas) {
    e.preventDefault();
  }
}, false);




})();
$( window ).resize(function() {
  var s = getComputedStyle(canvas);
  var w = s.width;
  var h = s.height;
  ctx.canvas.width = w.split('px')[0];
  ctx.canvas.height = h.split('px')[0];

  
});