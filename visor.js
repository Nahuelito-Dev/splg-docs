/* Visor de diagramas e imágenes, sobre Viewer.js (https://fengyuanchen.github.io/viewerjs/).
 *
 * Los diagramas entran en la página achicados al ancho de la columna y así no
 * se leen. Al hacer clic se abren en Viewer.js como una galería con todos los
 * diagramas de la página: ← y → pasan de uno a otro, la rueda acerca donde está
 * el puntero, se arrastra para mover, F pone pantalla completa y abajo quedan
 * las miniaturas.
 *
 * Viewer.js trabaja con imágenes. Las de PlantUML ya lo son; lo que dibuja
 * mermaid y los SVG hechos a mano de ramas y versionado se pasan a imagen al
 * abrir el visor, resolviendo antes las variables de color de la página, que
 * fuera del documento no existen.
 */
(function () {
  "use strict";

  var SELECTOR = ".diagram, .umlimg, .lienzo";
  var CDN = "https://cdnjs.cloudflare.com/ajax/libs/viewerjs/1.11.6/";

  /* ---------- la librería ---------- */
  var cargada = null;
  function cargarViewer() {
    if (cargada) return cargada;
    cargada = new Promise(function (ok, mal) {
      if (window.Viewer) { ok(); return; }
      var css = document.createElement("link");
      css.rel = "stylesheet";
      css.href = CDN + "viewer.min.css";
      document.head.appendChild(css);
      var js = document.createElement("script");
      js.src = CDN + "viewer.min.js";
      js.onload = function () { ok(); };
      js.onerror = function () { cargada = null; mal(new Error("No se pudo cargar Viewer.js")); };
      document.head.appendChild(js);
    });
    return cargada;
  }

  /* ---------- aviso "ampliar" en los lienzos de ramas y versionado ---------- */
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

  /* ---------- títulos ---------- */
  function titulo(fig) {
    // El título que el propio diagrama lleva dibujado ("DSD — CU-005 …"): es el
    // único que no se confunde con el rótulo de la sección de al lado.
    if (fig.classList.contains("umlimg")) return fig.getAttribute("alt") || "Diagrama";
    var svg = fig.querySelector("svg");
    if (svg) {
      var textos = svg.querySelectorAll("text");
      for (var i = 0; i < textos.length; i++) {
        var t = (textos[i].textContent || "").trim();
        if (/^(DSS|DSD|Diagrama|Modelo|CU-)\b/.test(t) || / — /.test(t)) return t;
      }
    }
    var caja = fig.closest(".figura") || fig;
    var previo = caja.previousElementSibling;
    if (previo && previo.classList.contains("dtitle")) return previo.textContent.trim();
    var pie = caja.parentElement && caja.parentElement.querySelector("figcaption");
    if (pie) return pie.textContent.trim().split(". ")[0];
    var ficha = fig.closest(".card");
    var h = ficha && ficha.querySelector("header h3");
    return h ? h.textContent.trim() : "Diagrama";
  }

  /* ---------- de figura a imagen ---------- */
  var variables = null;
  function resolverVariables(texto) {
    if (texto.indexOf("var(--") < 0) return texto;
    if (!variables) variables = getComputedStyle(document.documentElement);
    return texto.replace(/var\((--[\w-]+)(?:\s*,\s*([^)]+))?\)/g, function (_, nombre, defecto) {
      var v = variables.getPropertyValue(nombre).trim();
      return v || (defecto || "").trim() || "currentColor";
    });
  }
  var PROPIEDADES = ["fill", "fill-opacity", "stroke", "stroke-width", "stroke-dasharray",
    "stroke-linecap", "stroke-linejoin", "stroke-opacity", "opacity", "font-family", "font-size",
    "font-weight", "font-style", "letter-spacing", "text-anchor", "dominant-baseline", "marker-end",
    "marker-start", "visibility", "display"];
  function copiarEstilos(origen, destino) {
    var a = [origen].concat(Array.prototype.slice.call(origen.querySelectorAll("*")));
    var b = [destino].concat(Array.prototype.slice.call(destino.querySelectorAll("*")));
    for (var i = 0; i < a.length && i < b.length; i++) {
      var cs = getComputedStyle(a[i]), estilo = "";
      for (var j = 0; j < PROPIEDADES.length; j++) {
        var v = cs.getPropertyValue(PROPIEDADES[j]);
        // Las referencias a marcadores salen como URL absoluta de la página;
        // dentro de la imagen sólo vale el fragmento.
        if (v) estilo += PROPIEDADES[j] + ":" +
          v.replace(/url\(["']?[^#"')]*(#[^"')]+)["']?\)/g, "url($1)").replace(/"/g, "'") + ";";
      }
      b[i].setAttribute("style", estilo);
    }
  }
  function srcDe(fig) {
    if (fig.tagName === "IMG") return fig.currentSrc || fig.src;
    var svg = fig.tagName.toLowerCase() === "svg" ? fig : fig.querySelector("svg");
    if (!svg) return null;
    if (svg.__srcVisor) return svg.__srcVisor;
    var clon = svg.cloneNode(true);
    // Los SVG hechos a mano de ramas y versionado se pintan con el CSS de la
    // página; como imagen suelta lo pierden (salían negros y sin trazo). Se
    // copia el estilo ya calculado de cada elemento. Mermaid trae su propio
    // <style> y no lo necesita.
    if (!svg.querySelector("style")) copiarEstilos(svg, clon);
    clon.setAttribute("xmlns", "http://www.w3.org/2000/svg");
    clon.setAttribute("xmlns:xlink", "http://www.w3.org/1999/xlink");
    // Tamaño real del dibujo, no el de la columna: si no, al abrirlo las letras
    // quedan del tamaño achicado de la página.
    var vb = svg.viewBox && svg.viewBox.baseVal;
    var r = svg.getBoundingClientRect();
    var w = vb && vb.width ? vb.width : r.width, h = vb && vb.height ? vb.height : r.height;
    clon.setAttribute("width", Math.round(w));
    clon.setAttribute("height", Math.round(h));
    clon.removeAttribute("style");
    // Fondo blanco: fuera de la página el SVG es transparente y sobre el fondo
    // oscuro del visor no se ven las líneas.
    var fondo = document.createElementNS("http://www.w3.org/2000/svg", "rect");
    fondo.setAttribute("x", vb && vb.width ? vb.x : 0);
    fondo.setAttribute("y", vb && vb.width ? vb.y : 0);
    fondo.setAttribute("width", "100%");
    fondo.setAttribute("height", "100%");
    fondo.setAttribute("fill", "#FFFFFF");
    if (vb && vb.width) { fondo.setAttribute("width", vb.width); fondo.setAttribute("height", vb.height); }
    clon.insertBefore(fondo, clon.firstChild);
    var texto = resolverVariables(new XMLSerializer().serializeToString(clon));
    svg.__srcVisor = "data:image/svg+xml;charset=utf-8," + encodeURIComponent(texto);
    return svg.__srcVisor;
  }

  /* ---------- abrir ---------- */
  var visor = null, galeria = null;
  function figurasDeLaPagina() {
    return Array.prototype.filter.call(document.querySelectorAll(SELECTOR), function (f) {
      return f.offsetParent !== null && !(galeria && galeria.contains(f));
    });
  }
  function nombreArchivo(t) {
    t = (t || "diagrama").normalize("NFD").replace(/[̀-ͯ]/g, "");
    return t.replace(/[^\w-]+/g, "-").replace(/-+/g, "-").replace(/^-|-$/g, "").slice(0, 90) || "diagrama";
  }
  function descargar() {
    if (!visor || !visor.image) return;
    var img = visor.image, a = document.createElement("a");
    a.href = img.src;
    a.download = nombreArchivo(img.alt) + (/^data:image\/png/.test(img.src) ? ".png" : ".svg");
    document.body.appendChild(a);
    a.click();
    a.remove();
  }
  function pantallaCompleta() {
    var raiz = document.documentElement;
    if (document.fullscreenElement) { if (document.exitFullscreen) document.exitFullscreen(); }
    else if (raiz.requestFullscreen) raiz.requestFullscreen();
  }
  var temporizadorAviso = 0;
  function avisar(texto) {
    var c = document.querySelector(".viewer-container.viewer-in");
    if (!c) return;
    var p = c.querySelector(".visor-aviso");
    if (!p) { p = document.createElement("div"); p.className = "visor-aviso"; c.appendChild(p); }
    p.textContent = texto;
    p.classList.add("ver");
    clearTimeout(temporizadorAviso);
    temporizadorAviso = setTimeout(function () { p.classList.remove("ver"); }, 3500);
  }
  function encuadreLegible() {
    // Viewer.js abre el diagrama entero. Un diagrama de interacción largo,
    // entero, queda con letras de 4 px: en ese caso se ajusta al ancho y se
    // arranca desde arriba, para leerlo bajando como una página.
    var v = visor, d = v.imageData;
    if (!d || !d.naturalWidth) return;
    var anchoUtil = window.innerWidth - 80, altoUtil = window.innerHeight - 190;
    var entero = Math.min(anchoUtil / d.naturalWidth, altoUtil / d.naturalHeight);
    var ancho = Math.min(1.5, anchoUtil / d.naturalWidth);
    // Un diagrama gigante (el completo de casos de uso: 4900 × 4600) entero queda con letra
    // de 2 px y ajustado al ancho tampoco se lee: se abre a tamaño real desde el ángulo
    // superior izquierdo, donde se lee, y se recorre arrastrando; 0 lo muestra entero.
    if (ancho < 0.4) {
      v.zoomTo(1, false);
      v.moveTo(40, 40);
      avisar("Tamaño real: arrastrá para recorrerlo · 0 lo muestra entero");
      return;
    }
    // Sólo cuando entero no se lee (menos de la mitad del tamaño real).
    if (entero < 0.5 && ancho > entero * 1.4) {
      v.zoomTo(ancho, false);
      var dd = v.imageData;
      v.moveTo((window.innerWidth - dd.width) / 2, 24);
    }
  }
  function abrir(fig) {
    var figuras = figurasDeLaPagina();
    var inicio = Math.max(0, figuras.indexOf(fig));
    cargarViewer().then(function () {
      if (visor) { visor.destroy(); visor = null; }
      if (galeria) galeria.remove();
      galeria = document.createElement("ul");
      galeria.className = "galeria-visor";
      galeria.hidden = true;
      figuras.forEach(function (f) {
        var src = srcDe(f);
        if (!src) return;
        var li = document.createElement("li");
        var img = document.createElement("img");
        img.src = src;
        img.alt = titulo(f);
        li.appendChild(img);
        galeria.appendChild(li);
      });
      document.body.appendChild(galeria);
      var varias = figuras.length > 1;
      visor = new window.Viewer(galeria, {
        initialViewIndex: inicio,
        className: "visor-splg",
        backdrop: true,
        button: true,
        navbar: varias ? 4 : false,
        title: [1, function (img, datos) {
          return img.alt + (varias ? "   ·   " + (this.index + 1) + " / " + this.length : "");
        }],
        toolbar: {
          zoomOut: { show: 1, size: "large" },
          oneToOne: { show: 1, size: "large" },
          zoomIn: { show: 1, size: "large" },
          reset: { show: 1, size: "large" },
          prev: { show: varias ? 1 : 0, size: "large" },
          next: { show: varias ? 1 : 0, size: "large" },
          pantalla: { show: 1, size: "large", click: pantallaCompleta },
          descargar: { show: 1, size: "large", click: descargar }
        },
        tooltip: true,
        movable: true,
        zoomable: true,
        rotatable: false,
        scalable: false,
        transition: true,
        keyboard: true,
        loop: true,
        zoomRatio: 0.2,
        minZoomRatio: 0.03,
        maxZoomRatio: 8,
        viewed: encuadreLegible,
        hidden: function () {
          if (document.fullscreenElement && document.exitFullscreen) document.exitFullscreen();
          if (visor) { visor.destroy(); visor = null; }
          if (galeria) { galeria.remove(); galeria = null; }
        }
      });
      visor.show();
    }).catch(function () {
      // Sin red no hay librería: se abre la imagen sola en otra pestaña.
      var src = srcDe(fig);
      if (src) window.open(src, "_blank");
    });
  }

  function arrancar() {
    marcarFiguras();
    document.addEventListener("click", function (ev) {
      if (ev.target.closest && ev.target.closest(".viewer-container")) return;
      var fig = ev.target.closest && ev.target.closest(SELECTOR);
      if (fig) abrir(fig);
    });
    document.addEventListener("keydown", function (ev) {
      if (!visor || !document.querySelector(".viewer-container.viewer-in")) return;
      if (ev.key === "f" || ev.key === "F") pantallaCompleta();
      if (ev.key === "w" || ev.key === "W") encuadreLegible();
      if (ev.key === "0") visor.reset();
    });
    // Se baja de entrada, en segundo plano: el primer clic no espera la red.
    if ("requestIdleCallback" in window) window.requestIdleCallback(cargarViewer);
    else setTimeout(cargarViewer, 1500);
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", arrancar);
  else arrancar();
})();
