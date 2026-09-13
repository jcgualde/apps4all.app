#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
construir.py — generador del sitio apps4all.app

Qué hace, en una frase: coge las plantillas de `plantillas/`, les mete los
textos de `textos/` y escribe el sitio completo, en los tres idiomas, dentro
de la carpeta `publico/`.

    python construir.py

`publico/` es lo ÚNICO que se sube a Hostinger. Se borra y se vuelve a crear
en cada ejecución, así que nunca hay que editar nada ahí dentro: se perdería.

No usa ninguna librería externa a propósito, para que funcione en cualquier
ordenador con Python y en GitHub Actions sin instalar nada.
"""

import hashlib
import json
import re
import shutil
from pathlib import Path

RAIZ = Path(__file__).parent
PLANTILLAS = RAIZ / "plantillas"
TEXTOS = RAIZ / "textos"
ARTICULOS = RAIZ / "articulos"
SALIDA = RAIZ / "publico"


# --------------------------------------------------------------------------
# Utilidades
# --------------------------------------------------------------------------

def leer_json(ruta):
    with open(ruta, encoding="utf-8") as f:
        return json.load(f)


def leer_plantilla(nombre):
    with open(PLANTILLAS / nombre, encoding="utf-8") as f:
        return f.read()


def rellenar(plantilla, valores):
    """Sustituye {{clave}} por su valor. Lo que no encaje se queda como está,
    y al final se avisa por pantalla para que no pase desapercibido."""
    for clave, valor in valores.items():
        plantilla = plantilla.replace("{{" + clave + "}}", str(valor))
    return plantilla


def resaltar_cuatro(texto):
    """apps4comercios -> apps<span class="a4a-cuatro">4</span>comercios

    Regla de marca: el 4 va siempre en su color y el resto de caracteres no.
    """
    return texto.replace("4", '<span class="a4a-cuatro">4</span>', 1)


def huella(ruta):
    """Ocho caracteres que resumen el contenido de un archivo.

    Se cuelgan de la URL de las hojas de estilo (`sitio.css?v=1a2b3c4d`). Si
    el archivo cambia, cambia la huella, cambia la URL, y el navegador se ve
    obligado a descargarlo de nuevo en lugar de servir la copia vieja que
    tenga guardada. Es el remedio estándar contra "he cambiado el CSS y no
    se ve el cambio".
    """
    return hashlib.sha256(ruta.read_bytes()).hexdigest()[:8]


# --------------------------------------------------------------------------
# Blog
#
# Cada artículo es un archivo de texto en la carpeta `articulos/`. Arriba van
# los datos, luego una línea con tres guiones, y debajo el texto. Así:
#
#     titulo: Lo que aprendí con las licencias de las fotos
#     fecha: 2026-09-07
#     resumen: Una frase que se lee en el listado.
#     borrador: no
#     ---
#     El texto del artículo empieza aquí.
#
# El cuerpo admite un markdown reducido a lo imprescindible, para escribir sin
# pelearse con etiquetas: `##` y `###` para títulos, `- ` para listas, `> `
# para citas, **negrita**, *cursiva*, `código` y [texto](enlace).
#
# Poner `borrador: si` deja el artículo fuera de la web sin borrarlo.
# --------------------------------------------------------------------------

MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
         "agosto", "septiembre", "octubre", "noviembre", "diciembre"]


def escapar_html(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def sobre_la_linea(t):
    """Lo que se sustituye dentro de una línea: negritas, enlaces y demás."""
    t = escapar_html(t)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", t)
    return t


def md_a_html(cuerpo):
    """Convierte el texto del artículo en HTML. A propósito hace poco: si
    algún día hace falta más, se añade aquí y punto."""
    salida = []
    for bloque in re.split(r"\n\s*\n", cuerpo.strip()):
        lineas = [l.rstrip() for l in bloque.strip().split("\n") if l.strip()]
        if not lineas:
            continue
        if all(l.startswith("- ") for l in lineas):
            items = "".join("<li>%s</li>" % sobre_la_linea(l[2:]) for l in lineas)
            salida.append("<ul>%s</ul>" % items)
        elif all(l.startswith(">") for l in lineas):
            texto = " ".join(l.lstrip("> ").strip() for l in lineas)
            salida.append("<blockquote><p>%s</p></blockquote>" % sobre_la_linea(texto))
        elif lineas[0].startswith("### "):
            salida.append("<h3>%s</h3>" % sobre_la_linea(lineas[0][4:]))
        elif lineas[0].startswith("## "):
            salida.append("<h2>%s</h2>" % sobre_la_linea(lineas[0][3:]))
        else:
            salida.append("<p>%s</p>" % sobre_la_linea(" ".join(lineas)))
    return "\n".join("      " + s for s in salida)


def fecha_larga(iso):
    anyo, mes, dia = iso.split("-")
    return "%d de %s de %s" % (int(dia), MESES[int(mes) - 1], anyo)


def leer_articulos():
    """Lee la carpeta de artículos y los devuelve del más nuevo al más viejo."""
    if not ARTICULOS.is_dir():
        return []
    fichas = []
    for ruta in sorted(ARTICULOS.glob("*.md")):
        crudo = ruta.read_text(encoding="utf-8").replace("\r\n", "\n")
        cabecera, separador, cuerpo = crudo.partition("\n---\n")
        if not separador:
            print("  AVISO — %s no tiene la línea de tres guiones; se salta." % ruta.name)
            continue
        datos = {}
        for linea in cabecera.strip().split("\n"):
            if ":" in linea:
                clave, valor = linea.split(":", 1)
                datos[clave.strip()] = valor.strip()
        faltan = [c for c in ("titulo", "fecha", "resumen") if not datos.get(c)]
        if faltan:
            print("  AVISO — a %s le faltan datos: %s. Se salta." % (ruta.name, ", ".join(faltan)))
            continue
        if datos.get("borrador", "no").lower() in ("si", "sí", "yes", "true"):
            continue
        datos["slug"] = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", ruta.stem)
        datos["cuerpo"] = md_a_html(cuerpo)
        datos["fecha_larga"] = fecha_larga(datos["fecha"])
        fichas.append(datos)
    fichas.sort(key=lambda d: d["fecha"], reverse=True)
    return fichas


def tarjeta_articulo(a, base, texto_enlace):
    return f"""        <li class="articulos__ficha">
          <a href="{base}blog/{a['slug']}/">
            <p class="articulos__fecha">
              <time datetime="{a['fecha']}">{a['fecha_larga']}</time>
            </p>
            <h2>{a['titulo']}</h2>
            <p class="articulos__resumen">{a['resumen']}</p>
            <span class="tarjeta__flecha">{texto_enlace} &rarr;</span>
          </a>
        </li>
"""


def escribir(ruta_relativa, contenido):
    destino = SALIDA / ruta_relativa
    destino.parent.mkdir(parents=True, exist_ok=True)
    with open(destino, "w", encoding="utf-8", newline="\n") as f:
        f.write(contenido)


# --------------------------------------------------------------------------
# Trozos de HTML que se repiten
# --------------------------------------------------------------------------

def tarjeta_vertical(v, base, texto_enlace):
    return f"""        <a class="tarjeta tarjeta--enlace vertical-{v['color']}" href="{base}{v['slug']}/">
          <span class="monograma" aria-hidden="true"><span>{resaltar_cuatro(v['mono'])}</span></span>
          <span class="tarjeta__marca">{resaltar_cuatro(v['nombre'])}</span>
          <h3>{v['titulo']}</h3>
          <p>{v['resumen']}</p>
          <span class="tarjeta__pie">{v['etiqueta']}</span>
          <span class="tarjeta__flecha">{texto_enlace} &rarr;</span>
        </a>
"""


def bloque_paso(i, paso, etiqueta):
    return f"""        <article class="tarjeta">
          <p class="paso__numero">{etiqueta} 0{i}</p>
          <h3>{paso['titulo']}</h3>
          <p>{paso['texto']}</p>
        </article>
"""


def bloque_que(item):
    return f"""        <article class="tarjeta tarjeta--lisa">
          <span class="punto" aria-hidden="true"></span>
          <h3>{item['titulo']}</h3>
          <p>{item['texto']}</p>
        </article>
"""


def bloque_muestra(m):
    return f"""        <article class="muestra">
          <div class="muestra__pantalla" aria-hidden="true">
            <div class="muestra__barra"></div>
            <div class="muestra__lineas">
              <span></span><span></span><span></span><span></span>
            </div>
          </div>
          <div class="muestra__texto">
            <p class="etiqueta-estado">{m['estado']}</p>
            <h3>{m['titulo']}</h3>
            <p>{m['texto']}</p>
            <p class="muestra__detalle">{m['detalle']}</p>
          </div>
        </article>
"""


def selector_idioma(idiomas, actual, ruta_sin_idioma, nombres):
    partes = []
    for codigo in idiomas:
        clase = "idiomas__enlace"
        if codigo == actual:
            clase += " idiomas__enlace--activo"
        partes.append(
            f'<a class="{clase}" hreflang="{codigo}" href="/{codigo}/{ruta_sin_idioma}">{nombres[codigo]}</a>'
        )
    return "\n      ".join(partes)


def alternates(idiomas, ruta_sin_idioma, por_defecto, dominio):
    if por_defecto not in idiomas:
        por_defecto = idiomas[0]
    filas = [
        f'<link rel="alternate" hreflang="{c}" href="{dominio}/{c}/{ruta_sin_idioma}">'
        for c in idiomas
    ]
    filas.append(
        f'<link rel="alternate" hreflang="x-default" href="{dominio}/{por_defecto}/{ruta_sin_idioma}">'
    )
    return "\n".join(filas)


# --------------------------------------------------------------------------
# Construcción
# --------------------------------------------------------------------------

def construir():
    config = leer_json(TEXTOS / "config.json")
    legales = leer_json(TEXTOS / "legal.json")
    idiomas = config["idiomas"]
    por_defecto = config["idioma_por_defecto"]
    dominio = config["dominio"].rstrip("/")

    textos = {c: leer_json(TEXTOS / f"{c}.json") for c in idiomas}
    nombres_idioma = {c: textos[c]["nombre_idioma"] for c in idiomas}

    v_marca = huella(RAIZ / "assets" / "css" / "a4a-brand.css")
    v_sitio = huella(RAIZ / "assets" / "css" / "sitio.css")

    base_html = leer_plantilla("base.html")
    t_portada = leer_plantilla("portada.html")
    t_vertical = leer_plantilla("vertical.html")
    t_contacto = leer_plantilla("contacto.html")
    t_legal = leer_plantilla("legal.html")
    t_blog = leer_plantilla("blog.html")
    t_articulo = leer_plantilla("articulo.html")

    # Se vacía el contenido en lugar de borrar la carpeta: si hay un servidor
    # local levantado sobre ella, Windows la tiene bloqueada y rmtree falla.
    SALIDA.mkdir(exist_ok=True)
    for hijo in SALIDA.iterdir():
        shutil.rmtree(hijo) if hijo.is_dir() else hijo.unlink()

    rutas_sitemap = []

    def pagina(codigo, ruta_sin_idioma, contenido, titulo, clase_body="",
               idiomas_pagina=None):
        """Envuelve un contenido en base.html y lo escribe en su carpeta.

        `idiomas_pagina` dice en que idiomas existe esta pagina concreta.
        Por defecto, en todos. El blog solo existe en castellano, y si no
        se acota, las etiquetas hreflang y el selector de idioma apuntan a
        direcciones que devuelven un 404."""
        disponibles = idiomas_pagina or idiomas
        t = textos[codigo]
        ruta = f"/{codigo}/{ruta_sin_idioma}"
        valores = dict(t)
        valores.update({
            "lang": codigo,
            "base": f"/{codigo}/",
            "ruta": ruta,
            "titulo_pagina": titulo,
            "v_marca": v_marca,
            "v_sitio": v_sitio,
            "clase_body": clase_body,
            "nav_blog": (
                f'<a href="/es/blog/">{t["nav_blog_texto"]}</a>'
                if codigo == "es" else ""),
            "contenido": contenido,
            "alternates": alternates(disponibles, ruta_sin_idioma, por_defecto, dominio),
            "selector_idioma": selector_idioma(disponibles, codigo, ruta_sin_idioma, nombres_idioma),
        })
        html = rellenar(base_html, {k: v for k, v in valores.items() if isinstance(v, str)})
        escribir(f"{codigo}/{ruta_sin_idioma}index.html", html)
        rutas_sitemap.append((ruta, ruta_sin_idioma))
        return html

    for codigo in idiomas:
        t = textos[codigo]
        base = f"/{codigo}/"
        verticales = t["verticales"]

        # --- Portada ---
        tarjetas = "".join(tarjeta_vertical(v, base, t["lineas_enlace"]) for v in verticales)
        pasos = "".join(bloque_paso(i, p, t["paso"]) for i, p in enumerate(t["pasos"], 1))
        contenido = rellenar(t_portada, {
            **{k: v for k, v in t.items() if isinstance(v, str)},
            "base": base,
            "tarjetas_verticales": tarjetas,
            "pasos": pasos,
        })
        pagina(codigo, "", contenido, t["meta_titulo"], "pagina-portada")

        # --- Una página por vertical ---
        for v in verticales:
            otras = "".join(
                tarjeta_vertical(o, base, t["lineas_enlace"])
                for o in verticales if o["slug"] != v["slug"]
            )
            contenido = rellenar(t_vertical, {
                **{k: val for k, val in t.items() if isinstance(val, str)},
                **{k: val for k, val in v.items() if isinstance(val, str)},
                "base": base,
                "mono_html": resaltar_cuatro(v["mono"]),
                "nombre_html": resaltar_cuatro(v["nombre"]),
                "bloques_que": "".join(bloque_que(q) for q in v["que"]),
                "muestras": "".join(bloque_muestra(m) for m in v["muestras"]),
                "otras_verticales": otras,
            })
            pagina(codigo, f"{v['slug']}/", contenido,
                   f"{v['nombre']} — {v['titulo']} · apps4all", f"pagina-{v['slug']}")

        # --- Blog (solo en castellano) ---
        # Decidido el 07/09/2026: los artículos van solo en castellano. Si
        # hubiera que escribirlos tres veces no se escribiría ninguno, y lo
        # que se busca aquí es el hábito de publicar cada semana.
        if codigo == "es":
            articulos = leer_articulos()
            lista = "".join(tarjeta_articulo(a, base, t["blog_leer"]) for a in articulos)
            if not lista:
                lista = f'        <li class="articulos__vacio">{t["blog_vacio"]}</li>\n'
            contenido = rellenar(t_blog, {
                **{k: v for k, v in t.items() if isinstance(v, str)},
                "base": base,
                "lista_articulos": lista,
            })
            pagina(codigo, "blog/", contenido, f'{t["blog_titulo"]} · apps4all', "pagina-blog", idiomas_pagina=["es"])

            for a in articulos:
                contenido = rellenar(t_articulo, {
                    **{k: v for k, v in t.items() if isinstance(v, str)},
                    "base": base,
                    "articulo_titulo": a["titulo"],
                    "articulo_fecha": a["fecha_larga"],
                    "articulo_fecha_iso": a["fecha"],
                    "articulo_cuerpo": a["cuerpo"],
                })
                pagina(codigo, f"blog/{a['slug']}/", contenido,
                       f'{a["titulo"]} · apps4all', "pagina-articulo",
                       idiomas_pagina=["es"])

        # --- Contacto ---
        opciones = "\n".join(
            f'            <option value="{o}">{o}</option>' for o in t["form_asunto_opciones"]
        )
        contenido = rellenar(t_contacto, {
            **{k: v for k, v in t.items() if isinstance(v, str)},
            "base": base,
            "correo": config["correo"],
            "web3forms_clave": config["web3forms_clave"],
            "asunto_opciones": opciones,
            "js_enviando": json.dumps(t["form_enviando"], ensure_ascii=False),
            "js_ok": json.dumps(t["form_ok"], ensure_ascii=False),
            "js_error": json.dumps(t["form_error"], ensure_ascii=False),
            "js_enviar": json.dumps(t["form_enviar"], ensure_ascii=False),
            "js_correo": json.dumps(config["correo"], ensure_ascii=False),
        })
        pagina(codigo, "contacto/", contenido, f'{t["contacto_antetitulo"]} · apps4all')

        # --- Legales ---
        datos_legales = {
            "titular": config["titular"],
            "nif": config["nif"],
            "domicilio": config["domicilio"],
            "correo": config["correo"],
            "dominio": dominio,
        }
        for clave, slug, titulo in (
            ("aviso", "legal/aviso-legal/", t["legal_aviso_titulo"]),
            ("privacidad", "legal/privacidad/", t["legal_privacidad_titulo"]),
            # La de a4h: Google Play exige una URL de política por app.
            ("privacidad_a4h", "legal/privacidad-a4h/", t["legal_privacidad_a4h_titulo"]),
        ):
            cuerpo = rellenar("\n".join(legales[codigo][clave]), datos_legales)
            contenido = rellenar(t_legal, {
                **{k: v for k, v in t.items() if isinstance(v, str)},
                "base": base,
                "titulo_legal": titulo,
                "fecha": config["fecha_legal"],
                "cuerpo_legal": cuerpo,
            })
            pagina(codigo, slug, contenido, f"{titulo} · apps4all")

    # --- Assets ---
    shutil.copytree(RAIZ / "assets", SALIDA / "assets")

    # --- Redirección de la raíz al idioma por defecto ---
    escribir("index.html", f"""<!doctype html>
<html lang="{por_defecto}">
<head>
<meta charset="utf-8">
<title>apps4all</title>
<meta http-equiv="refresh" content="0; url=/{por_defecto}/">
<link rel="canonical" href="{dominio}/{por_defecto}/">
<script>location.replace('/{por_defecto}/');</script>
</head>
<body><p><a href="/{por_defecto}/">apps4all</a></p></body>
</html>
""")

    # --- sitemap.xml y robots.txt ---
    urls = "\n".join(
        f"  <url><loc>{dominio}{ruta}</loc></url>" for ruta, _ in rutas_sitemap
    )
    escribir("sitemap.xml",
             '<?xml version="1.0" encoding="UTF-8"?>\n'
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
             f"{urls}\n</urlset>\n")
    escribir("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {dominio}/sitemap.xml\n")

    # --- Avisos ---
    paginas = len(rutas_sitemap)
    print(f"Listo: {paginas} páginas en {len(idiomas)} idiomas -> {SALIDA}")

    pendientes = [k for k, v in config.items()
                  if isinstance(v, str) and v.startswith("PENDIENTE")]
    if pendientes:
        print("\n  AVISO — quedan datos por rellenar en textos/config.json:")
        for k in pendientes:
            print(f"    - {k}")

    sin_rellenar = set()
    for archivo in SALIDA.rglob("*.html"):
        sin_rellenar.update(re.findall(r"\{\{(\w+)\}\}", archivo.read_text(encoding="utf-8")))
    if sin_rellenar:
        print("\n  AVISO — huecos de plantilla sin rellenar:", ", ".join(sorted(sin_rellenar)))


if __name__ == "__main__":
    construir()
