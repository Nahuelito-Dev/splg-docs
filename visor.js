/* Visor con acercamiento para diagramas e imágenes.
 *
 * Los diagramas entran en la página achicados para respetar el ancho de la
 * columna, y así no se leen: los de interacción de diseño tienen quince líneas
 * de vida. Acá se abren en grande, entrando enteros en pantalla, y de ahí se
 * acercan con la rueda, con los botones, con doble clic o con el teclado.
 *
 * Sirve igual para lo dibujado por mermaid y para los SVG escritos a mano de
 * las páginas de ramas y versionado, porque el nodo se clona dentro del mismo
 * documento y las variables de color siguen resolviendo.
 */
(function () {
  "use strict";

  /* Lo que se puede ampliar: los diagramas de la página principal, las
     imágenes de casos de uso en UML y los lienzos de las otras dos páginas. */
  var SELECTOR = ".diagram, .umlimg, .lienzo";

  var visor = document.createElement("div");
  visor.className = "visor";
  visor.id = "visor";
  visor.setAttribute("role", "dialog");
  visor.setAttribute("aria-modal", "true");
  visor.setAttribute("aria-label", "Diagrama ampliado");
  visor.innerHTML =
    '<div class="barra">' +
      '<span class="nombre" id="visorNombre"></span>' +
      '<button type="button" data-zoom="-1" title="Alejar">−</button>' +
      '<span id="visorNivel">100%</span>' +
      '<button type="button" data-zoom="1" title="Acercar">+</button>' +
      '<button type="button" data-zoom="0" title="Encuadrar">AJUSTAR</button>' +
      '<button type="button" id="visorCerrar" title="Cerrar (Esc)">CERRAR</button>' +
    "</div>" +
    '<p class="ayuda">Rueda del mouse o + / − para acercar · arrastrar para mover · ' +
      "doble clic para acercar · 0 encuadra · Esc cierra</p>" +
    '<div class="lienzo-visor" id="visorLienzo"><div class="marco" id="visorMarco"></div></div>';

  function montar() {
    document.body.appendChild(visor);
    // El aviso se agrega acá y no en el HTML de cada página para no repetirlo.
    marcarFiguras();
  }

  /* Las páginas de ramas y versionado se dibujan también dentro de la
     documentación, y ahí el contenido llega después de cargar: por eso el
     aviso no se pone una sola vez al arrancar sino cada vez que aparece un
     lienzo nuevo. */
  function marcarFiguras() {
    document.querySelectorAll(".lienzo").forEach(envolver);
  }
  window.marcarFigurasAmpliables = marcarFiguras;
  function envolver(nodo) {
    if (nodo.parentElement && nodo.parentElement.classList.contains("figura")) return;
    var caja = document.createElement("div");
    caja.className = "figura";
    nodo.parentNode.insertBefore(caja, nodo);
    caja.appendChild(nodo);
    var aviso = document.createElement("span");
    aviso.className = "ampliar";
    aviso.textContent = "CLIC PARA AMPLIAR";
    caja.appendChild(aviso);
    nodo.style.cursor = "zoom-in";
  }

  var lienzo, marco, nivelTexto, nombre;
  var escala = 1, desplX = 0, desplY = 0, arrastrando = false, x0 = 0, y0 = 0;

  function aplicar() {
    marco.style.transform =
      "translate(" + desplX + "px," + desplY + "px) scale(" + escala + ")";
    nivelTexto.textContent = Math.round(escala * 100) + "%";
  }
  function encuadrar() {
    // Entrar mostrando el diagrama entero: los de diseño son anchos y al 100%
    // arrancaban cortados, obligando a arrastrar para saber qué había.
    var fig = marco.firstElementChild;
    if (!fig) return;
    // Sin pasar por escala 1: el diagrama completo son 2242 x 8748 y pedirle al
    // navegador que lo dibuje a tamaño real, aunque sea por un cuadro, congela
    // la pestaña. Se calcula el encuadre sobre la medida de maquetado y se
    // aplica una sola vez.
    desplX = 0; desplY = 0;
    // La medida del marco sin transformar. Antes se leia el rectangulo ya
    // escalado y, con el diagrama completo —2242 x 8748—, el navegador pegaba
    // el marco contra el borde del lienzo en vez de centrarlo y el encuadre
    // dejaba la lamina fuera de la vista.
    var w = marco.offsetWidth, h = marco.offsetHeight;
    var disp = lienzo.getBoundingClientRect();
    if (!w || !h) return;
    escala = Math.min(1, (disp.width - 40) / w, (disp.height - 40) / h);
    centrar(w, h, disp);
  }
  function centrar(w, h, disp) {
    desplX = (disp.width  - w * escala) / 2;
    desplY = (disp.height - h * escala) / 2;
    aplicar();
    marco.style.visibility = "";
  }
  function escalar(factor, cx, cy) {
    // Amplia dejando quieto el punto (cx, cy) del lienzo. Si no se indica uno,
    // el que queda quieto es el centro.
    var antes = escala;
    escala = Math.min(6, Math.max(0.03, escala * factor));
    if (escala === antes) return;
    var disp = lienzo.getBoundingClientRect();
    if (cx === undefined) { cx = disp.width / 2; cy = disp.height / 2; }
    desplX = cx - (cx - desplX) / antes * escala;
    desplY = cy - (cy - desplY) / antes * escala;
    sujetar();
    aplicar();
  }
  function acercar(paso) {
    // Pasos proporcionales: con incrementos fijos de 0,25 el diagrama completo
    // saltaba del 9% al 34% de un tirón.
    escalar(Math.pow(1.3, paso));
  }
  function sujetar() {
    // Sin esto se puede arrastrar el diagrama fuera de la pantalla y queda un
    // lienzo vacío del que no se vuelve mas que con AJUSTAR. Se deja siempre
    // una franja visible del ancho de un margen.
    var disp = lienzo.getBoundingClientRect();
    var w = marco.offsetWidth * escala, h = marco.offsetHeight * escala;
    var m = 80;
    desplX = Math.min(disp.width - m, Math.max(m - w, desplX));
    desplY = Math.min(disp.height - m, Math.max(m - h, desplY));
  }
  function rotulo(fig) {
    if (fig.classList.contains("umlimg")) return fig.getAttribute("alt") || "";
    var caja = fig.closest(".figura") || fig;
    var previo = caja.previousElementSibling;
    if (previo && previo.classList.contains("dtitle")) return previo.textContent;
    var pie = caja.parentElement && caja.parentElement.querySelector("figcaption");
    if (pie) return pie.textContent.trim().split(". ")[0];
    var ficha = fig.closest(".card");
    var h = ficha && ficha.querySelector("header h3");
    return h ? h.textContent : "";
  }
  function abrir(fig) {
    // Oculto hasta tener el encuadre: si se pinta con la escala anterior, un
    // diagrama grande se dibuja entero a tamaño real y la pestaña se traba.
    marco.style.visibility = "hidden";
    var copia = fig.cloneNode(true);
    copia.classList.remove("umlimg", "diagram", "lienzo");
    copia.style.cursor = "";
    marco.innerHTML = "";
    marco.appendChild(copia);
    // Un SVG trae el ancho del contenedor donde se dibujó: acá se lo deja
    // crecer con su relación de aspecto.
    var svg = marco.querySelector("svg");
    if (svg) {
      svg.removeAttribute("width");
      svg.removeAttribute("height");
      svg.style.width = "min(92vw, 1500px)";
      svg.style.minWidth = "0";
      svg.style.height = "auto";
    }
    nombre.textContent = rotulo(fig);
    visor.setAttribute("open", "");
    encuadrar();
    // Una imagen embebida grande —el diagrama completo son 300 KB de SVG— todavia
    // no tiene medidas cuando se la acaba de insertar, y el encuadre salia en 100%
    // mostrando una esquina vacia. Se reencuadra cuando el navegador ya la midio.
    if (copia.tagName === "IMG" && !copia.complete) copia.addEventListener("load", encuadrar);
    requestAnimationFrame(encuadrar);
  }
  function cerrar() {
    visor.removeAttribute("open");
    marco.innerHTML = "";
  }

  function arrancar() {
    montar();
    lienzo = document.getElementById("visorLienzo");
    marco = document.getElementById("visorMarco");
    nivelTexto = document.getElementById("visorNivel");
    nombre = document.getElementById("visorNombre");

    document.addEventListener("click", function (ev) {
      if (visor.hasAttribute("open")) return;
      var fig = ev.target.closest && ev.target.closest(SELECTOR);
      if (fig) abrir(fig);
    });
    visor.addEventListener("click", function (ev) {
      var b = ev.target.closest("button");
      if (b) {
        var z = b.getAttribute("data-zoom");
        if (z === "0") encuadrar();
        else if (z) acercar(Number(z));
        if (b.id === "visorCerrar") cerrar();
        return;
      }
      if (ev.target === lienzo) cerrar();
    });
    lienzo.addEventListener("dblclick", function () { acercar(2); });
    lienzo.addEventListener("wheel", function (ev) {
      ev.preventDefault();
      var disp = lienzo.getBoundingClientRect();
      // El trackpad dispara muchas ruedas chicas y el mouse pocas grandes: con
      // un paso fijo, el trackpad pegaba saltos. El paso sale del gesto.
      // ctrlKey es el pellizco del trackpad; ahi el navegador manda un delta
      // mucho mas chico y hay que amplificarlo para que responda igual.
      var d = ev.deltaY * (ev.deltaMode === 1 ? 16 : 1);
      var factor = Math.exp(-d * (ev.ctrlKey ? 0.012 : 0.0022));
      // Un golpe de rueda no puede mas que duplicar o partir al medio.
      factor = Math.min(2, Math.max(0.5, factor));
      escalar(factor, ev.clientX - disp.left, ev.clientY - disp.top);
    }, { passive: false });
    lienzo.addEventListener("pointerdown", function (ev) {
      if (ev.button !== 0 && ev.pointerType === "mouse") return;
      arrastrando = true;
      lienzo.setPointerCapture(ev.pointerId);
      lienzo.classList.add("arrastrando");
      x0 = ev.clientX - desplX;
      y0 = ev.clientY - desplY;
    });
    lienzo.addEventListener("pointermove", function (ev) {
      if (!arrastrando) return;
      ev.preventDefault();
      desplX = ev.clientX - x0;
      desplY = ev.clientY - y0;
      sujetar();
      aplicar();
    });
    function soltar(ev) {
      if (!arrastrando) return;
      arrastrando = false;
      if (ev && ev.pointerId !== undefined && lienzo.hasPointerCapture(ev.pointerId)) {
        lienzo.releasePointerCapture(ev.pointerId);
      }
      lienzo.classList.remove("arrastrando");
    }
    lienzo.addEventListener("pointerup", soltar);
    lienzo.addEventListener("pointercancel", soltar);
    window.addEventListener("keydown", function (ev) {
      if (!visor.hasAttribute("open")) return;
      if (ev.key === "Escape") cerrar();
      if (ev.key === "+" || ev.key === "=") acercar(1);
      if (ev.key === "-") acercar(-1);
      if (ev.key === "0") encuadrar();
      if (ev.key === "1") { escalar(1 / escala); }
      var salto = ev.shiftKey ? 200 : 60;
      if (ev.key === "ArrowLeft")  { desplX += salto; sujetar(); aplicar(); }
      if (ev.key === "ArrowRight") { desplX -= salto; sujetar(); aplicar(); }
      if (ev.key === "ArrowUp")    { desplY += salto; sujetar(); aplicar(); }
      if (ev.key === "ArrowDown")  { desplY -= salto; sujetar(); aplicar(); }
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", arrancar);
  } else {
    arrancar();
  }
})();
