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

    # Se vacía el contenido en lugar de borrar la carpeta: si hay un servidor
    # local levantado sobre ella, Windows la tiene bloqueada y rmtree falla.
    SALIDA.mkdir(exist_ok=True)
    for hijo in SALIDA.iterdir():
        shutil.rmtree(hijo) if hijo.is_dir() else hijo.unlink()

    rutas_sitemap = []

    def pagina(codigo, ruta_sin_idioma, contenido, titulo, clase_body=""):
        """Envuelve un contenido en base.html y lo escribe en su carpeta."""
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
            "contenido": contenido,
            "alternates": alternates(idiomas, ruta_sin_idioma, por_defecto, dominio),
            "selector_idioma": selector_idioma(idiomas, codigo, ruta_sin_idioma, nombres_idioma),
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
