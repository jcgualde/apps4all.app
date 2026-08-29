#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera "apps4all - Como se hizo esta web.pdf".

    python guia/generar-tutorial.py

Cuenta, para alguien que parte de cero, todo lo que se hizo el 29/08/2026
para pasar de una carpeta vacía a apps4all.app publicada y actualizándose
sola. Incluye los tropiezos, que es donde está lo que de verdad se aprende.

Mismas decisiones de forma que generar-plan-aprendizaje.py: solo reportlab,
Helvetica porque la tipografía de marca aún no está elegida, y sin dibujar
los logotipos, que la guía de marca prohíbe redibujar.
"""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (BaseDocTemplate, Frame, KeepTogether, PageBreak,
                                PageTemplate, Paragraph, Spacer, Table, TableStyle)

TINTA = colors.HexColor("#12141C")
AZUL = colors.HexColor("#2B6FC2")
AZUL_CLARO = colors.HexColor("#5C9BE0")
GRIS = colors.HexColor("#6B6F7A")
GRIS_CLARO = colors.HexColor("#A8ACB6")
BLANCO = colors.white
VERDE = colors.HexColor("#1D9E75")
CORAL = colors.HexColor("#D85A30")
MORADO = colors.HexColor("#6F66D6")
MAGENTA = colors.HexColor("#C0348B")
PAPEL = colors.HexColor("#F2F3F6")

SALIDA = Path(__file__).parent / "apps4all - Como se hizo esta web.pdf"
ANCHO, ALTO = A4
MARGEN = 20 * mm

base = getSampleStyleSheet()
E = {
    "titulo": ParagraphStyle("titulo", parent=base["Title"], fontName="Helvetica-Bold",
                             fontSize=29, leading=33, textColor=BLANCO,
                             alignment=TA_LEFT, spaceAfter=10),
    "subtitulo": ParagraphStyle("subtitulo", parent=base["Normal"], fontName="Helvetica",
                                fontSize=12.5, leading=18, textColor=GRIS_CLARO, spaceAfter=6),
    "h1": ParagraphStyle("h1", parent=base["Heading1"], fontName="Helvetica-Bold",
                         fontSize=19, leading=23, textColor=TINTA, spaceBefore=2, spaceAfter=9),
    "h2": ParagraphStyle("h2", parent=base["Heading2"], fontName="Helvetica-Bold",
                         fontSize=13, leading=17, textColor=TINTA, spaceBefore=15, spaceAfter=5),
    "p": ParagraphStyle("p", parent=base["Normal"], fontName="Helvetica",
                        fontSize=10, leading=15.2, textColor=TINTA, spaceAfter=7),
    "gris": ParagraphStyle("gris", parent=base["Normal"], fontName="Helvetica",
                           fontSize=9.5, leading=14, textColor=GRIS, spaceAfter=7),
    "antetitulo": ParagraphStyle("antetitulo", parent=base["Normal"], fontName="Helvetica-Bold",
                                 fontSize=8, leading=11, textColor=AZUL, spaceAfter=3),
    "celda": ParagraphStyle("celda", parent=base["Normal"], fontName="Helvetica",
                            fontSize=8.8, leading=12.5, textColor=TINTA),
    "celdag": ParagraphStyle("celdag", parent=base["Normal"], fontName="Helvetica",
                             fontSize=8.8, leading=12.5, textColor=GRIS),
    "celdacab": ParagraphStyle("celdacab", parent=base["Normal"], fontName="Helvetica-Bold",
                               fontSize=8.5, leading=12, textColor=BLANCO),
    "codigo": ParagraphStyle("codigo", parent=base["Normal"], fontName="Courier",
                             fontSize=9, leading=13, textColor=TINTA,
                             backColor=PAPEL, borderPadding=7, spaceAfter=8),
}


def p(t, e="p"):
    return Paragraph(t, E[e])


def portada(c, doc):
    c.saveState()
    c.setFillColor(TINTA)
    c.rect(0, 0, ANCHO, ALTO, fill=1, stroke=0)
    for i, col in enumerate((AZUL, VERDE, CORAL, MORADO, MAGENTA)):
        c.setFillColor(col)
        c.rect(MARGEN + i * 22 * mm, ALTO - 42 * mm, 18 * mm, 3, fill=1, stroke=0)
    c.restoreState()


def interior(c, doc):
    c.saveState()
    c.setFillColor(GRIS_CLARO)
    c.setFont("Helvetica", 7.5)
    c.drawString(MARGEN, 12 * mm, "apps4all - Cómo se hizo esta web")
    c.drawRightString(ANCHO - MARGEN, 12 * mm, str(c.getPageNumber()))
    c.setStrokeColor(colors.HexColor("#E4E6EA"))
    c.setLineWidth(0.5)
    c.line(MARGEN, 16 * mm, ANCHO - MARGEN, 16 * mm)
    c.restoreState()


def tabla(filas, anchos):
    return Table(filas, colWidths=anchos, hAlign="LEFT", style=TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("BACKGROUND", (0, 0), (-1, 0), TINTA),
        ("LINEBELOW", (0, 0), (-1, -2), 0.5, colors.HexColor("#E4E6EA")),
    ]))


def cab(*textos):
    return [Paragraph(t, E["celdacab"]) for t in textos]


PASOS = [
    ("01", "Una carpeta y una identidad",
     "Antes de escribir una línea de código ya existían los logotipos y una paleta de colores "
     "cerrada, guardados en un archivo que define cada color con un nombre. Eso permite que "
     "todo el sitio use <b>var(--a4a-azul)</b> en vez de repetir un código de color por todas "
     "partes: el día que se afine la paleta, se cambia un archivo y cambia la web entera.",
     "Las decisiones de forma se toman una vez y se escriben. Repetirlas a mano en cada "
     "página es cómo acaban las webs con seis azules distintos."),

    ("02", "La primera página, en HTML puro",
     "Se descartó usar un framework moderno. Una web de cinco páginas se escribe en HTML y CSS "
     "a mano, sin instalar nada y sin nada que se pueda romper entre tu carpeta y el servidor. "
     "Publicar es copiar archivos.",
     "La herramienta se elige por el problema que tienes hoy, no por la que se lleve. Lo "
     "sofisticado se añade cuando lo simple se queda corto, y no antes."),

    ("03", "Apareció el multiidioma, y con él el generador",
     "Al querer la web en castellano, inglés y catalán, mantener 24 páginas a mano dejó de "
     "tener sentido: cada corrección habría que hacerla tres veces y acabarían descuadrándose. "
     "Se escribió <b>construir.py</b>, un programa de unas 300 líneas que coge unas plantillas "
     "y unos archivos de texto y fabrica el sitio completo.",
     "Aquí se reabrió a propósito una decisión que estaba cerrada. Reabrirla fue correcto "
     "porque el problema había cambiado; lo incorrecto habría sido reabrirla por capricho."),

    ("04", "Git: la máquina del tiempo",
     "El proyecto se puso bajo control de versiones. Cada cambio queda guardado con una "
     "descripción, y se puede volver atrás en cualquier momento. Después se envió a GitHub, "
     "que es una copia de todo eso en internet.",
     "GitHub no es la web: es el archivo histórico. Nadie visita tu repositorio. Sirve para "
     "no perder trabajo y para saber por qué algo se hizo como se hizo."),

    ("05", "Publicar a mano, a propósito",
     "La primera publicación se hizo comprimiendo la web en un ZIP y subiéndola por el "
     "administrador de archivos de Hostinger. Pudiendo automatizarlo desde el principio, se "
     "hizo a mano deliberadamente.",
     "Automatizar antes de comprobar que lo básico funciona es depurar dos cosas a la vez. "
     "Si la web no hubiera cargado, no se habría sabido si el fallo estaba en el dominio, en "
     "el certificado o en la automatización."),

    ("06", "El intento que falló",
     "Se configuró un robot en GitHub para que subiera la web por FTP en cada cambio. Falló "
     "tres veces con el mismo mensaje: <b>Timeout (control socket)</b>. Se probó sin cifrar y "
     "con cifrado. Hostinger no responde en ese puerto cuando la llamada viene de un centro "
     "de datos como el de GitHub.",
     "El mensaje de error importaba. Un &laquo;timeout&raquo; significa que nadie contestó; un error "
     "de credenciales habría significado que contestaron y dijeron que no. Son problemas "
     "distintos y llevan a soluciones distintas."),

    ("07", "Darle la vuelta al problema",
     "En vez de insistir, se invirtió la dirección. Ahora GitHub fabrica la web y la deja "
     "terminada en una rama aparte llamada <b>publicado</b>, y es <b>Hostinger quien va a "
     "buscarla</b>. Esa llamada la hace el servidor de Hostinger, que no está bloqueado.",
     "Cuando una puerta está tapiada, a veces la solución no es empujar más fuerte sino "
     "entrar por el otro lado. La misma tarea, el camino contrario."),
]

TROPIEZOS = [
    ("El navegador enseñaba colores viejos",
     "Se cambiaba un color y no se veía el cambio. El navegador guarda copias de los archivos "
     "para ir más rápido y seguía usando la antigua.",
     "Se añadió una huella al nombre del archivo de estilos: <b>sitio.css?v=74d7101a</b>. Si el "
     "archivo cambia, cambia la huella, y el navegador se ve obligado a descargarlo de nuevo. "
     "El arreglo no era para nosotros: era para cualquiera que visite la web tras un cambio."),

    ("Se subió el ZIP equivocado",
     "Había dos versiones casi idénticas y se publicó la que llevaba los datos del aviso legal "
     "sin rellenar. Estuvo así unas horas, en una web pública.",
     "Comprobar el resultado desde fuera, no fiarse de que &laquo;debería estar bien&raquo;. Se detectó "
     "pidiéndole la página al servidor y buscando el NIF dentro."),

    ("La conexión con Hostinger entró en bucle",
     "Al autorizar Hostinger en GitHub, el regreso falló con <b>Unauthenticated</b>: la ventana "
     "emergente no llevaba la sesión. Después, cada intento llevaba a la pantalla de ajustes en "
     "vez de completar la conexión.",
     "Como la aplicación ya estaba instalada, GitHub no repetía el proceso, y Hostinger nunca "
     "recibía la confirmación. Cada uno esperaba al otro. Se resolvió desinstalando y "
     "volviendo a instalar: forzar el proceso completo desde cero."),

    ("El diseño fue y volvió",
     "La primera versión pareció demasiado blanca. La segunda, demasiado oscura. La tercera, "
     "de un azul demasiado pálido.",
     "Se dejó de adivinar: se midieron los colores de una web que sí gustaba y se montó una "
     "página con cinco variantes reales para elegir señalando una. Enseñar tres opciones "
     "concretas ahorra cinco rondas de descripciones."),

    ("Un texto que se contradecía",
     "Tres páginas presumían de que la aplicación se abre &laquo;sin instalar nada&raquo;, en la web de "
     "un estudio que vive de hacer aplicaciones.",
     "No se borró la ventaja, se contó bien: se elige el formato que menos estorba, y a veces "
     "ese formato es una aplicación de las de instalar. Un beneficio real mal contado hace "
     "más daño que no contarlo."),
]

GLOSARIO = [
    ("Repositorio", "La carpeta del proyecto con todo su historial de cambios. Vive en tu ordenador y tiene una copia en GitHub."),
    ("Commit", "Una foto del proyecto en un momento dado, con una frase que explica qué cambió y por qué."),
    ("Rama (branch)", "Una línea de trabajo paralela. Aquí hay dos: main con los ingredientes, y publicado con la web ya hecha."),
    ("Push", "Enviar a GitHub los cambios guardados en tu ordenador."),
    ("GitHub Actions", "Un robot que ejecuta tareas en los servidores de GitHub cada vez que llega un cambio."),
    ("Workflow", "El archivo que le dice a ese robot qué tiene que hacer, paso a paso."),
    ("Secret", "Una contraseña guardada en GitHub de forma que el robot pueda usarla sin que nadie pueda leerla."),
    ("FTP / FTPS", "El protocolo clásico para copiar archivos a un servidor. FTPS es el mismo, cifrado."),
    ("SSL / HTTPS", "El certificado que cifra la conexión. Sin él, un dominio .app no se abre en absoluto."),
    ("DNS", "La guía telefónica de internet: convierte apps4all.app en la dirección numérica del servidor."),
    ("public_html", "La carpeta del servidor cuyo contenido se publica. Lo que está ahí, se ve."),
    ("Caché", "Copias que guardan navegadores y servidores para ir más rápido. A veces enseñan lo viejo."),
    ("hreflang", "Una marca en el código que le dice a Google que tres páginas son la misma en tres idiomas."),
    ("Sitemap", "Un listado de todas las páginas del sitio, para que los buscadores no se dejen ninguna."),
    ("OAuth", "Autorizar a un servicio a acceder a otro sin darle tu contraseña. Revocable en cualquier momento."),
]


def construir():
    doc = BaseDocTemplate(
        str(SALIDA), pagesize=A4,
        leftMargin=MARGEN, rightMargin=MARGEN, topMargin=MARGEN, bottomMargin=24 * mm,
        title="apps4all - Cómo se hizo esta web", author="apps4all")
    doc.addPageTemplates([
        PageTemplate(id="portada",
                     frames=[Frame(MARGEN, 40 * mm, ANCHO - 2 * MARGEN, ALTO - 90 * mm)],
                     onPage=portada),
        PageTemplate(id="interior",
                     frames=[Frame(MARGEN, 24 * mm, ANCHO - 2 * MARGEN, ALTO - MARGEN - 30 * mm)],
                     onPage=interior),
    ])

    h = []

    # ---- Portada ----
    h.append(p("DE UNA CARPETA VACÍA A UNA WEB PUBLICADA", "antetitulo"))
    h.append(p("Cómo se hizo esta web", "titulo"))
    h.append(Spacer(1, 6))
    h.append(p("El recorrido completo de un día de trabajo: qué se construyó, en qué orden, "
               "por qué se decidió así, y los cinco tropiezos que enseñaron algo. Escrito para "
               "alguien que no ha hecho una web nunca.", "subtitulo"))
    h.append(Spacer(1, 14))
    h.append(p("apps4all &middot; 29 de agosto de 2026", "subtitulo"))
    h.append(PageBreak())

    # ---- Resultado ----
    h.append(p("Qué hay al final", "h1"))
    h.append(p("<b>https://apps4all.app</b> — 24 páginas en castellano, inglés y catalán: una "
               "portada, cuatro líneas de trabajo, un formulario de contacto y dos textos "
               "legales. Se ve bien en el ordenador y en el móvil, no usa cookies, y se "
               "actualiza sola cuando se le envía un cambio.", "p"))
    h.append(p("Lo que sigue no es el manual de la web. Es el relato de cómo se llegó hasta "
               "ahí, incluidas las tres veces que algo no funcionó.", "gris"))

    h.append(p("Las tres piezas, y por qué son tres", "h2"))
    h.append(p("La confusión más habitual al empezar es creer que esto es un solo sitio. Son "
               "tres, y cada uno hace algo distinto:", "p"))
    h.append(tabla([
        cab("Pieza", "Qué es", "Quién la ve"),
        [Paragraph("<b>Tu ordenador</b>", E["celda"]),
         Paragraph("La carpeta donde se escribe. Aquí vive el original.", E["celdag"]),
         Paragraph("Solo tú", E["celdag"])],
        [Paragraph("<b>GitHub</b>", E["celda"]),
         Paragraph("El archivo histórico en internet. Guarda cada versión y por qué se hizo. También ejecuta el robot que fabrica la web.", E["celdag"]),
         Paragraph("Nadie, salvo quien invites", E["celdag"])],
        [Paragraph("<b>Hostinger</b>", E["celda"]),
         Paragraph("El servidor. Lo que hay en su carpeta public_html es lo que ve el mundo.", E["celdag"]),
         Paragraph("Todo internet", E["celdag"])],
    ], [30 * mm, 90 * mm, 50 * mm]))
    h.append(Spacer(1, 8))
    h.append(p("Publicar es mover una copia de la primera a la tercera. Todo lo demás es "
               "decidir quién hace ese viaje y por dónde.", "gris"))
    h.append(PageBreak())

    # ---- Los pasos ----
    h.append(p("El recorrido, paso a paso", "h1"))
    h.append(Spacer(1, 4))
    for n, titulo, texto, leccion in PASOS:
        bloque = [
            p(f"PASO {n}", "antetitulo"),
            p(titulo, "h2"),
            p(texto, "p"),
            tabla([[Paragraph(f"<b>Lo que enseña.</b> {leccion}", E["celdag"])]], [170 * mm]),
            Spacer(1, 12),
        ]
        # La tabla de la lección hereda la cabecera oscura; se corrige aquí.
        bloque[3].setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), PAPEL),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("LINEBEFORE", (0, 0), (0, -1), 3, AZUL),
        ]))
        h.append(KeepTogether(bloque))
    h.append(PageBreak())

    # ---- Tropiezos ----
    h.append(p("Los cinco tropiezos", "h1"))
    h.append(p("Esta es la parte que no suele contarse y la que más enseña. Ninguno de estos "
               "problemas venía de escribir mal el código: venían de que dos sistemas no se "
               "entendían, o de que un texto decía algo que nadie había releído.", "p"))
    h.append(Spacer(1, 6))
    for titulo, que_paso, como in TROPIEZOS:
        h.append(KeepTogether([
            p(titulo, "h2"),
            p(f"<b>Qué pasó.</b> {que_paso}", "p"),
            p(f"<b>Cómo se resolvió.</b> {como}", "gris"),
            Spacer(1, 6),
        ]))
    h.append(PageBreak())

    # ---- Rutina ----
    h.append(p("Cómo se cambia algo a partir de ahora", "h1"))
    h.append(p("Este es el estado final, y es la razón de todo el trabajo anterior. Para "
               "cambiar una palabra de la web ya no hay que abrir Hostinger:", "p"))
    h.append(tabla([
        cab("Quién", "Qué hace"),
        [Paragraph("<b>1. Tú</b>", E["celda"]), Paragraph("Dices qué quieres cambiar.", E["celdag"])],
        [Paragraph("<b>2. El texto</b>", E["celda"]), Paragraph("Se edita en textos/es.json, en.json o ca.json. Un solo sitio para los tres idiomas.", E["celdag"])],
        [Paragraph("<b>3. git push</b>", E["celda"]), Paragraph("El cambio viaja a GitHub.", E["celdag"])],
        [Paragraph("<b>4. El robot</b>", E["celda"]), Paragraph("Ejecuta construir.py, fabrica las 24 páginas y las deja en la rama publicado.", E["celdag"])],
        [Paragraph("<b>5. Hostinger</b>", E["celda"]), Paragraph("Recoge esa rama y la publica en public_html.", E["celdag"])],
    ], [28 * mm, 142 * mm]))
    h.append(Spacer(1, 10))
    h.append(p("Y si algún día todo eso falla, siempre queda el camino de la primera vez: "
               "generar el ZIP, subirlo al administrador de archivos y extraerlo. Tener una "
               "salida manual que funciona es lo que permite experimentar con la automática "
               "sin miedo.", "gris"))

    h.append(p("Las órdenes que se usan a diario", "h2"))
    h.append(p("python construir.py", "codigo"))
    h.append(p("Fabrica la web en la carpeta publico/.", "gris"))
    h.append(p("python -m http.server 4322 --directory publico", "codigo"))
    h.append(p("La abre en el navegador en localhost:4322 para verla antes de publicar.", "gris"))
    h.append(p("git push", "codigo"))
    h.append(p("Envía los cambios y dispara la publicación.", "gris"))
    h.append(PageBreak())

    # ---- Glosario ----
    h.append(p("Lo que todavía falta", "h2"))
    h.append(p("Ningún proyecto se termina; se publica y se sigue. A día de hoy quedan: la "
               "clave del formulario de contacto, las capturas reales de las aplicaciones "
               "para las secciones de muestras, y elegir la tipografía definitiva de la marca "
               "antes de imprimir nada.", "p"))

    h.append(PageBreak())

    h.append(p("Glosario", "h1"))
    h.append(p("Quince palabras que aparecen todo el rato y que nadie explica nunca.", "gris"))
    h.append(Spacer(1, 6))
    filas = [cab("Palabra", "Qué significa")]
    for palabra, definicion in GLOSARIO:
        filas.append([Paragraph(f"<b>{palabra}</b>", E["celda"]),
                      Paragraph(definicion, E["celdag"])])
    h.append(tabla(filas, [34 * mm, 136 * mm]))

    doc.build(h)
    print(f"Escrito: {SALIDA}")


if __name__ == "__main__":
    construir()
