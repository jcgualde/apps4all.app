#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera el PDF "apps4all - Plan de aprendizaje.pdf".

    python guia/generar-plan-aprendizaje.py

Usa solo reportlab. La tipografía es Helvetica porque la definitiva de la
marca todavía no está elegida (ver la guía de marca, apartado "Estado de la
tipografía"). Los logotipos de a4a no se dibujan aquí a propósito: la guía
prohíbe redibujarlos, y sin poder incrustar el SVG original es preferible
no ponerlos.
"""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (BaseDocTemplate, Frame, PageBreak, PageTemplate,
                                Paragraph, Spacer, Table, TableStyle)

# --- Paleta de marca -------------------------------------------------------
TINTA = colors.HexColor("#12141C")
AZUL = colors.HexColor("#2B6FC2")
GRIS = colors.HexColor("#6B6F7A")
GRIS_CLARO = colors.HexColor("#A8ACB6")
BLANCO = colors.white
VERDE = colors.HexColor("#1D9E75")
CORAL = colors.HexColor("#D85A30")
MORADO = colors.HexColor("#6F66D6")

SALIDA = Path(__file__).parent / "apps4all - Plan de aprendizaje.pdf"

ANCHO, ALTO = A4
MARGEN = 20 * mm

# --- Estilos ---------------------------------------------------------------
base = getSampleStyleSheet()

E = {
    "titulo": ParagraphStyle("titulo", parent=base["Title"], fontName="Helvetica-Bold",
                             fontSize=30, leading=34, textColor=BLANCO, alignment=TA_LEFT,
                             spaceAfter=10),
    "subtitulo": ParagraphStyle("subtitulo", parent=base["Normal"], fontName="Helvetica",
                                fontSize=12.5, leading=18, textColor=GRIS_CLARO, spaceAfter=6),
    "h1": ParagraphStyle("h1", parent=base["Heading1"], fontName="Helvetica-Bold",
                         fontSize=19, leading=23, textColor=TINTA, spaceBefore=4, spaceAfter=8),
    "h2": ParagraphStyle("h2", parent=base["Heading2"], fontName="Helvetica-Bold",
                         fontSize=13.5, leading=17, textColor=TINTA, spaceBefore=14, spaceAfter=5),
    "p": ParagraphStyle("p", parent=base["Normal"], fontName="Helvetica",
                        fontSize=10, leading=15, textColor=TINTA, spaceAfter=7),
    "gris": ParagraphStyle("gris", parent=base["Normal"], fontName="Helvetica",
                           fontSize=9.5, leading=14, textColor=GRIS, spaceAfter=7),
    "antetitulo": ParagraphStyle("antetitulo", parent=base["Normal"], fontName="Helvetica-Bold",
                                 fontSize=8, leading=11, textColor=AZUL, spaceAfter=3),
    "celda": ParagraphStyle("celda", parent=base["Normal"], fontName="Helvetica",
                            fontSize=8.8, leading=12.5, textColor=TINTA),
    "celda_gris": ParagraphStyle("celda_gris", parent=base["Normal"], fontName="Helvetica",
                                 fontSize=8.8, leading=12.5, textColor=GRIS),
    "celda_cab": ParagraphStyle("celda_cab", parent=base["Normal"], fontName="Helvetica-Bold",
                                fontSize=8.5, leading=12, textColor=BLANCO),
    "enlace": ParagraphStyle("enlace", parent=base["Normal"], fontName="Helvetica",
                             fontSize=8.5, leading=12, textColor=AZUL),
}


def p(texto, estilo="p"):
    return Paragraph(texto, E[estilo])


def enlace(texto, url):
    return f'<link href="{url}" color="#2B6FC2">{texto}</link>'


# --- Composición de páginas ------------------------------------------------

def portada(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(TINTA)
    canvas.rect(0, 0, ANCHO, ALTO, fill=1, stroke=0)
    # Tres barras de las verticales, como firma visual discreta.
    for i, c in enumerate((VERDE, CORAL, MORADO)):
        canvas.setFillColor(c)
        canvas.rect(MARGEN + i * 26 * mm, ALTO - 42 * mm, 22 * mm, 3, fill=1, stroke=0)
    canvas.restoreState()


def interior(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(GRIS_CLARO)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(MARGEN, 12 * mm, "apps4all - Plan de aprendizaje")
    canvas.drawRightString(ANCHO - MARGEN, 12 * mm, str(canvas.getPageNumber()))
    canvas.setStrokeColor(colors.HexColor("#E4E6EA"))
    canvas.setLineWidth(0.5)
    canvas.line(MARGEN, 16 * mm, ANCHO - MARGEN, 16 * mm)
    canvas.restoreState()


def tabla(datos, anchos, cabecera=True):
    estilo = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("LINEBELOW", (0, 0), (-1, -2), 0.5, colors.HexColor("#E4E6EA")),
    ]
    if cabecera:
        estilo += [("BACKGROUND", (0, 0), (-1, 0), TINTA)]
    return Table(datos, colWidths=anchos, style=TableStyle(estilo), hAlign="LEFT")


# --- Contenido -------------------------------------------------------------

HABILIDADES = [
    {
        "n": "01",
        "nombre": "HTML y CSS",
        "porque": "Es el material del que está hecha tu web y el de cualquier WebApp "
                  "que entregues. Sin esto dependes de otro para cambiar una coma.",
        "suficiente": "Saber leer una página entera y entender por qué cada cosa está "
                      "donde está. Manejar Flexbox y Grid sin copiar y pegar. Entender "
                      "las variables CSS, que es justo lo que usa tu sitio para los colores.",
        "horas": "30-40 h",
        "recursos": [
            ("Curso", "freeCodeCamp - Responsive Web Design (gratis, en inglés, muy práctico)",
             "https://www.freecodecamp.org/learn/2022/responsive-web-design/"),
            ("Referencia", "MDN Web Docs - Aprender desarrollo web (gratis, en español)",
             "https://developer.mozilla.org/es/docs/Learn"),
            ("Curso", "web.dev - Learn CSS y Learn HTML, de Google (gratis)",
             "https://web.dev/learn/css"),
            ("Libro", "Jon Duckett, HTML y CSS: diseñe y construya sitios web", None),
        ],
    },
    {
        "n": "02",
        "nombre": "Git y GitHub",
        "porque": "Es tu red de seguridad y tu memoria. Sin Git, un error se convierte "
                  "en trabajo perdido; con Git, en un comando. Además es la vía por la "
                  "que se publica tu web.",
        "suficiente": "Ramas, commits, pull requests, resolver un conflicto sin pánico y "
                      "saber volver a un estado anterior. No necesitas nada exótico.",
        "horas": "12-15 h",
        "recursos": [
            ("Libro", "Pro Git, de Scott Chacon (gratis y en español)",
             "https://git-scm.com/book/es/v2"),
            ("Curso", "GitHub Skills - cursos cortos dentro del propio GitHub (gratis)",
             "https://skills.github.com/"),
            ("Práctica", "Learn Git Branching - visual, se aprende jugando (gratis)",
             "https://learngitbranching.js.org/?locale=es_ES"),
        ],
    },
    {
        "n": "03",
        "nombre": "Línea de comandos",
        "porque": "Todo lo que automatiza trabajo vive aquí: generar la web, correr "
                  "pruebas, desplegar. Es la habilidad con mejor relación entre horas "
                  "invertidas y tiempo ahorrado de toda la lista.",
        "suficiente": "Moverte por carpetas, encadenar comandos, entender rutas y "
                      "variables de entorno, y leer un error sin asustarte.",
        "horas": "10-12 h",
        "recursos": [
            ("Curso", "The Missing Semester of Your CS Education, del MIT (gratis, con "
                      "traducción al español)",
             "https://missing-semester-es.github.io/"),
            ("Curso", "Learn Enough Command Line to Be Dangerous",
             "https://www.learnenough.com/command-line-tutorial"),
        ],
    },
    {
        "n": "04",
        "nombre": "Python para automatizar",
        "porque": "Ya lo estás usando sin saberlo: el generador de tu web es Python. "
                  "En tu trabajo de gestoría, además, es lo que convierte tareas de "
                  "media mañana en un script de dos minutos.",
        "suficiente": "Leer y escribir archivos, manejar JSON y CSV, funciones, "
                      "diccionarios y listas. Nada de programación orientada a objetos "
                      "avanzada por ahora.",
        "horas": "25-30 h",
        "recursos": [
            ("Libro", "Al Sweigart, Automate the Boring Stuff with Python (gratis en web)",
             "https://automatetheboringstuff.com/"),
            ("Libro", "Eric Matthes, Python Crash Course (hay edición en español)", None),
            ("Referencia", "Tutorial oficial de Python en español",
             "https://docs.python.org/es/3/tutorial/"),
        ],
    },
    {
        "n": "05",
        "nombre": "Cómo funciona la web por dentro",
        "porque": "DNS, HTTPS, certificados, códigos de estado. Es lo que separa "
                  "'no me carga la web' de 'el certificado aún no está activo y por "
                  "eso el dominio .app no resuelve'. Sin esto se depura a ciegas.",
        "suficiente": "Entender qué pasa entre que escribes una dirección y ves la "
                      "página. Saber leer la pestaña Red de las herramientas del navegador.",
        "horas": "8-10 h",
        "recursos": [
            ("Referencia", "Cloudflare Learning Center - DNS, HTTPS, CDN (gratis, en español)",
             "https://www.cloudflare.com/es-es/learning/"),
            ("Referencia", "MDN - Introducción a HTTP",
             "https://developer.mozilla.org/es/docs/Web/HTTP"),
            ("Práctica", "Las herramientas de desarrollo de tu navegador. F12 y curiosear.", None),
        ],
    },
    {
        "n": "06",
        "nombre": "JavaScript de andar por casa",
        "porque": "Tu formulario de contacto ya lleva JavaScript. Cualquier cosa que "
                  "reaccione en la página sin recargarla lo necesita.",
        "suficiente": "Variables, funciones, eventos, manipular el DOM y entender "
                      "fetch y las promesas. No hace falta ningún framework.",
        "horas": "25-30 h",
        "recursos": [
            ("Curso", "javascript.info - el mejor manual que existe (gratis, en español)",
             "https://es.javascript.info/"),
            ("Libro", "Marijn Haverbeke, Eloquent JavaScript (gratis en web)",
             "https://eloquentjavascript.net/"),
        ],
    },
    {
        "n": "07",
        "nombre": "Diseño de interfaz",
        "porque": "Es lo que hace que un trabajo se perciba como profesional o como "
                  "casero, con el mismo código detrás. Es también lo que más sube el "
                  "precio que puedes pedir.",
        "suficiente": "Jerarquía visual, espaciado, escala tipográfica y contraste. "
                      "Tener criterio, no saber dibujar.",
        "horas": "15-20 h",
        "recursos": [
            ("Libro", "Adam Wathan y Steve Schoger, Refactoring UI (de pago, muy recomendable)",
             "https://www.refactoringui.com/"),
            ("Libro", "Steve Krug, No me hagas pensar (clásico de usabilidad)", None),
            ("Referencia", "Laws of UX - principios de diseño explicados en una página cada uno",
             "https://lawsofux.com/es/"),
        ],
    },
    {
        "n": "08",
        "nombre": "Accesibilidad",
        "porque": "Además de ser lo correcto, en España es obligatorio para el sector "
                  "público. Si quieres vender aplicaciones de fiestas a ayuntamientos, "
                  "esto deja de ser opcional y pasa a ser un requisito del pliego.",
        "suficiente": "Contraste suficiente, navegación por teclado, textos alternativos "
                      "y etiquetas de formulario bien puestas. Saber pasar un validador.",
        "horas": "8-10 h",
        "recursos": [
            ("Curso", "web.dev - Learn Accessibility (gratis)",
             "https://web.dev/learn/accessibility"),
            ("Referencia", "WCAG 2.1, referencia rápida del W3C",
             "https://www.w3.org/WAI/WCAG21/quickref/"),
        ],
    },
    {
        "n": "09",
        "nombre": "Seguridad y protección de datos",
        "porque": "En cuanto una aplicación tuya toca datos de terceros (y la de tickets "
                  "los toca), pasas a ser responsable. Aquí partes con ventaja por tu "
                  "trabajo en la gestoría.",
        "suficiente": "Conocer los fallos habituales, no guardar secretos en el código, "
                      "y saber qué es un contrato de encargado del tratamiento.",
        "horas": "10-12 h",
        "recursos": [
            ("Referencia", "OWASP Top 10 - los diez fallos más comunes",
             "https://owasp.org/www-project-top-ten/"),
            ("Referencia", "Guías de la Agencia Española de Protección de Datos",
             "https://www.aepd.es/guias"),
        ],
    },
    {
        "n": "10",
        "nombre": "Flutter y Dart",
        "porque": "Es tu vía para las aplicaciones móviles de verdad: la de hábitos y "
                  "las de fiestas. Un solo código para Android y iOS.",
        "suficiente": "Widgets, estado, navegación y publicación en las tiendas. "
                      "Empieza después de tener soltura con lo anterior.",
        "horas": "60-80 h",
        "recursos": [
            ("Referencia", "Documentación oficial de Flutter, incluido el codelab inicial",
             "https://docs.flutter.dev/get-started/codelab"),
            ("Referencia", "Recorrido por el lenguaje Dart",
             "https://dart.dev/language"),
            ("Curso", "Flutter Apprentice, de Kodeco (libro y proyecto guiado)", None),
        ],
    },
    {
        "n": "11",
        "nombre": "Presupuestar y vender",
        "porque": "Es la habilidad que decide si esto es un negocio o un hobby caro. "
                  "La mayoría de estudios pequeños no cierran por no saber programar, "
                  "sino por presupuestar por debajo de coste.",
        "suficiente": "Saber poner precio a un alcance, escribir qué no incluye, y "
                      "decir que no a un encargo malo sin sentirte culpable.",
        "horas": "10-15 h",
        "recursos": [
            ("Libro", "Paul Jarvis, Company of One", None),
            ("Libro", "Jonathan Stark, Hourly Billing Is Nuts (gratis registrándote)",
             "https://jonathanstark.com/hbin"),
            ("Práctica", "Escribir tu tarifa y tu modelo de presupuesto. Dos folios.", None),
        ],
    },
]


def construir():
    doc = BaseDocTemplate(
        str(SALIDA), pagesize=A4,
        leftMargin=MARGEN, rightMargin=MARGEN,
        topMargin=MARGEN, bottomMargin=24 * mm,
        title="apps4all - Plan de aprendizaje",
        author="apps4all",
    )

    marco_portada = Frame(MARGEN, 40 * mm, ANCHO - 2 * MARGEN, ALTO - 90 * mm, id="portada")
    marco = Frame(MARGEN, 24 * mm, ANCHO - 2 * MARGEN, ALTO - MARGEN - 30 * mm, id="normal")
    doc.addPageTemplates([
        PageTemplate(id="portada", frames=[marco_portada], onPage=portada),
        PageTemplate(id="interior", frames=[marco], onPage=interior),
    ])

    h = []

    # ---------------- Portada ----------------
    h.append(p("PLAN DE APRENDIZAJE", "antetitulo"))
    h.append(p("Qué aprender, en qué orden y con qué.", "titulo"))
    h.append(Spacer(1, 6))
    h.append(p("Once habilidades para pasar de encargar una web a dirigir un estudio "
               "de aplicaciones. Ordenadas por lo que antes te devuelve el tiempo "
               "invertido, no por dificultad.", "subtitulo"))
    h.append(Spacer(1, 14))
    h.append(p("apps4all &middot; agosto de 2026", "subtitulo"))
    h.append(PageBreak())

    # ---------------- Cómo usarlo ----------------
    h.append(p("Cómo usar este plan", "h1"))
    h.append(p("La trampa de una lista como esta es leerla entera, agobiarse y no "
               "empezar. Para que no pase:", "p"))
    h.append(p("<b>Una habilidad cada vez, y siempre con un trabajo real encima de la "
               "mesa.</b> Aprender HTML mientras cambias los textos de tu propia web "
               "vale por tres cursos hechos en abstracto. Ya tienes el proyecto: úsalo "
               "como campo de pruebas.", "p"))
    h.append(p("<b>Las horas son orientativas y suponen aprender haciendo</b>, no viendo "
               "vídeos. Si dedicas cinco horas a la semana, las tres primeras "
               "habilidades te llevan unos tres meses. Ese es el ritmo realista de "
               "alguien que además trabaja.", "p"))
    h.append(p("<b>No hace falta terminar una para empezar la siguiente.</b> Con "
               "entender lo suficiente para no bloquearte basta: lo demás se aprende "
               "cuando lo necesitas, que es cuando de verdad se fija.", "p"))
    h.append(p("<b>Lo gratuito de esta lista no es peor que lo de pago.</b> En "
               "programación, buena parte del mejor material del mundo es libre. Los "
               "libros de pago están señalados y ninguno es imprescindible.", "p"))

    h.append(p("El orden, de un vistazo", "h2"))
    filas = [[
        Paragraph("Fase", E["celda_cab"]),
        Paragraph("Habilidades", E["celda_cab"]),
        Paragraph("Para qué te desbloquea", E["celda_cab"]),
    ]]
    for fase, habs, para in [
        ("Ahora", "01 HTML y CSS &middot; 02 Git &middot; 03 Línea de comandos",
         "Llevar tu propia web sin depender de nadie y publicar sin miedo a romperla."),
        ("Después", "04 Python &middot; 05 Cómo funciona la web &middot; 06 JavaScript",
         "Construir herramientas de verdad y entender qué falla cuando algo falla."),
        ("Cuando haya clientes", "07 Diseño &middot; 08 Accesibilidad &middot; 09 Seguridad",
         "Entregar trabajo que se paga mejor y poder presentarte a un concurso público."),
        ("Cuando toque móvil", "10 Flutter y Dart",
         "Las aplicaciones de hábitos y de fiestas, en Android y iOS con un solo código."),
        ("En paralelo, siempre", "11 Presupuestar y vender",
         "Que el estudio sea rentable. No esperes a dominar lo técnico para empezar."),
    ]:
        filas.append([
            Paragraph(f"<b>{fase}</b>", E["celda"]),
            Paragraph(habs, E["celda"]),
            Paragraph(para, E["celda_gris"]),
        ])
    h.append(tabla(filas, [26 * mm, 62 * mm, 82 * mm]))
    h.append(PageBreak())

    # ---------------- Fichas ----------------
    for i, hab in enumerate(HABILIDADES):
        h.append(p(f"HABILIDAD {hab['n']} &middot; {hab['horas']}", "antetitulo"))
        h.append(p(hab["nombre"], "h1"))
        h.append(p(f"<b>Por qué.</b> {hab['porque']}", "p"))
        h.append(p(f"<b>Qué es saber lo suficiente.</b> {hab['suficiente']}", "gris"))

        filas = [[
            Paragraph("Tipo", E["celda_cab"]),
            Paragraph("Recurso", E["celda_cab"]),
        ]]
        for tipo, texto, url in hab["recursos"]:
            contenido = enlace(texto, url) if url else texto
            filas.append([
                Paragraph(f"<b>{tipo}</b>", E["celda"]),
                Paragraph(contenido, E["celda"]),
            ])
        h.append(tabla(filas, [22 * mm, 148 * mm]))

        if i % 2 == 1 and i != len(HABILIDADES) - 1:
            h.append(PageBreak())
        else:
            h.append(Spacer(1, 16))

    # ---------------- Cierre ----------------
    h.append(PageBreak())
    h.append(p("Cuatro errores que cuestan meses", "h1"))
    for titulo, texto in [
        ("Estudiar sin publicar nada",
         "El aprendizaje se fija al entregar, no al terminar un curso. Publica cosas "
         "pequeñas y feas antes que perfectas y pendientes: es la misma regla con la "
         "que estamos haciendo tu web."),
        ("Empezar por el framework de moda",
         "React, Next, Tailwind y compañía resuelven problemas que todavía no tienes. "
         "Aprenderlos antes que HTML y CSS deja un hueco que se nota durante años."),
        ("Ver vídeos en lugar de escribir código",
         "Mirar a alguien programar produce la sensación de aprender sin el aprendizaje. "
         "Regla práctica: por cada hora de vídeo, dos escribiendo tú."),
        ("Cobrar por horas para siempre",
         "Cobrar por horas castiga justo lo que vas a mejorar: hacerlo más rápido. En "
         "cuanto tengas dos o tres trabajos parecidos hechos, pasa a precio cerrado."),
    ]:
        h.append(p(titulo, "h2"))
        h.append(p(texto, "p"))

    h.append(p("Una rutina que funciona", "h2"))
    h.append(p("Cinco horas a la semana, repartidas en sesiones de una hora en días "
               "distintos, rinden bastante más que una sesión de cinco horas el "
               "domingo. Y de cada sesión, la última media hora dedícala a aplicar lo "
               "aprendido a algo tuyo: a tu web, a un script de la gestoría, a lo que "
               "sea que ya exista.", "p"))
    h.append(Spacer(1, 10))
    h.append(p("Los enlaces de este documento estaban activos en agosto de 2026. Si "
               "alguno se rompe, busca el título: casi todos estos materiales llevan "
               "años en el mismo sitio.", "gris"))

    doc.build(h)
    print(f"Escrito: {SALIDA}")


if __name__ == "__main__":
    construir()
