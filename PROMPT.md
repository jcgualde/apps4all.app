# Prompt para reconstruir esta web

Lo que sigue es el encargo que, dado de una vez, produce aproximadamente lo
que se construyó el 29/08/2026 a lo largo de una sesión entera de idas y
venidas. No es el prompt que se usó —no hubo uno, hubo una conversación—,
sino el que habría hecho falta sabiendo lo que sabemos ahora.

Sirve para tres cosas: rehacer el proyecto si se pierde, arrancar un sitio
parecido para otro cliente cambiando los datos, y ver de un vistazo todas las
decisiones que hay detrás.

**Cómo usarlo:** cópialo entero y pégalo en una sesión nueva de Claude Code,
dentro de una carpeta vacía. Antes, deja en `assets/` los SVG de la marca y
`a4a-brand.css`, o pide que se generen primero.

---

## El prompt

```
Quiero una web corporativa para mi estudio de aplicaciones, apps4all, en el
dominio apps4all.app. Soy novel en web, git y hosting: explícame todo lo que
hagas o propongas, sin dar jerga por sabida, y avísame cuando algo que pida
choque con una decisión anterior.

Regla que gobierna el proyecto: publicado y modesto gana a perfecto y
pendiente. No propongas rehacer nada con un framework antes de que esté
publicado.

ENTORNO
- Windows, sin Node ni npm. Sí hay git y Python 3.11.
- Alojamiento en Hostinger, plan compartido, carpeta public_html.
- Repositorio privado en GitHub.

MARCA
Aplica la identidad de apps4all sin desviaciones:
- Tinta #12141C, azul #2B6FC2, gris #6B6F7A, gris claro #A8ACB6, blanco.
- El azul es EXCLUSIVO del carácter "4". Nunca en la caja del monograma,
  nunca en el resto de letras. Esa restricción es lo que hace que el 4 se
  lea como "apps for all". En interfaz sí puede usarse azul para botones y
  enlaces, pero no pegado al logotipo.
- Los colores van en un archivo de variables CSS aparte que no se edita.
  Ningún hex suelto en el resto del código.
- Claim: "Crear, añadir, mejorar".
- Los logotipos son SVG ya existentes: úsalos tal cual, no los redibujes.

ESTRUCTURA DEL SITIO
Portada, una página por línea de trabajo, contacto y dos textos legales.
Cada página es una carpeta con index.html, para que la URL sea /contacto/ y
no /contacto.html.

Las líneas de trabajo, cada una con su monograma, su nombre y su color, y
donde lo único que cambia de color es el "4":
- a4c · apps4comercios · verde #1D9E75 · herramientas para el día a día de
  un negocio: capturar documentos, ordenar pedidos.
- a4f · apps4fiestas · coral #D85A30 · programa y avisos de fiestas
  populares, con QR en el cartel.
- a4s · apps4salud · morado #6F66D6 · producto propio, empezando por una
  aplicación de hábitos.
- a4g · apps4games · magenta #C0348B · línea abierta, todavía sin ningún
  trabajo. Existe porque la marca se llama apps4all y la lista no puede ser
  cerrada. Dilo en la propia página, no disimules que está vacía.

El titular de la sección NO debe llevar número ("cualquier tipo de encargo",
no "tres tipos de encargo"): añadir una quinta línea no debe obligar a
reescribir la portada.

TRES IDIOMAS
Castellano, inglés y catalán, en carpetas /es/, /en/ y /ca/ con las mismas
rutas, hreflang entre ellas y un selector en el pie. Los nombres de las
líneas son marca y NO se traducen.

Como no hay Node, escribe un generador propio en Python, sin ninguna
dependencia externa, para que funcione igual en mi equipo y en GitHub
Actions sin instalar nada:
- plantillas/ con el HTML y huecos {{clave}}
- textos/ con un JSON por idioma, más config.json y legal.json
- construir.py, que lo ensambla todo en publico/
- publico/ va en .gitignore y no se edita nunca

El generador debe avisar por pantalla si queda algún dato sin rellenar o
algún hueco de plantilla sin sustituir.

Añade a las hojas de estilo una huella del contenido en la URL
(sitio.css?v=abc12345) para que el navegador no sirva la versión antigua
tras un cambio.

DISEÑO
Referencia: airdroid.com. Fondo mayoritariamente blanco, con el color en
dosis pequeñas. La franja superior de cada página va oscura, en tinta
mezclada con el color de su línea (azul marino en la portada, verde profundo
en comercios, y así). Cabecera blanca con el logotipo normal. Un único
bloque oscuro más al final de la portada. Responsive de verdad: pruébalo a
375 px de ancho y comprueba que nada se sale por los lados y que los
botones miden al menos 44 px de alto.

TEXTOS
Directos y sin palabrería comercial. Tono: "si no es para nosotros, te lo
decimos". Y cuidado con una contradicción fácil: no vendas "sin instalar
nada" como virtud principal, porque es un estudio que vive de hacer
aplicaciones. Cuenta la comodidad real (se abre con un enlace, un QR en el
cartel) y di explícitamente que también se construyen aplicaciones
instalables cuando el caso lo pide.

CONTACTO
Formulario que envía a jcgualde@apps4all.app mediante Web3Forms (sin PHP, sin
servidor), con casilla de aceptación de privacidad, envío sin recargar la
página y aviso de enviado o fallado. La clave va en config.json.

LEGAL
Aviso legal según el artículo 10 de la LSSI-CE y política de privacidad, en
los tres idiomas, con el titular, NIF y domicilio saliendo de config.json.
Sin cookies ni analítica de terceros, y dilo en la política: así no hace
falta banner de consentimiento.

PUBLICACIÓN
Importante, esto tiene truco: el FTP de Hostinger NO responde a las
conexiones que vienen de los servidores de GitHub. Falla con "Timeout
(control socket)" tanto sin cifrar como con FTPS. No pierdas el tiempo ahí.

Monta en su lugar la dirección inversa:
1. GitHub Actions ejecuta construir.py y hace un push forzado del contenido
   de publico/ a una rama llamada `publicado`, con el index.html en su raíz.
   Usa el GITHUB_TOKEN automático y permissions: contents: write.
2. En Hostinger, hPanel → Avanzado → GIT, conectar con GitHub por OAuth y
   desplegar la rama `publicado` en public_html.

La primera publicación hazla a mano con un ZIP, antes de automatizar nada:
sirve para descartar problemas de dominio y certificado por separado. Y ojo,
el dominio .app está en la lista de precarga HSTS: sin certificado SSL activo
no carga en absoluto, no es que dé un aviso.

Genérame tú el ZIP con el index.html en la raíz del archivo, que es el error
clásico.

DOCUMENTACIÓN
README.md con dónde se toca cada cosa, y un PASOS.md con lo que tengo que
hacer yo en Hostinger y GitHub, por fases y sin saltos.

FORMA DE TRABAJAR CONMIGO
- Una cosa cada vez. No me encadenes listas largas de tareas.
- Cuando haya que elegir algo visual, no me lo describas: móntame las
  opciones en una página que pueda mirar y elijo señalando una.
- Comprueba el resultado desde fuera antes de decirme que algo funciona.
- Las contraseñas no me las pidas por chat nunca.
```

---

## Lo que el prompt no puede darte

Tres cosas salieron de la conversación y no de ninguna instrucción, y son
justo las que hicieron el proyecto mejor:

- **La cuarta línea, `apps4games`.** Nació de leer la portada y darse cuenta
  de que "tres tipos de encargo" contradecía el nombre de la marca.
- **Quitar el "sin instalar nada".** Lo detectó quien conocía el negocio, no
  quien escribía el texto.
- **El color de la franja superior.** Hicieron falta tres intentos y una
  página de comparación para acertar. Ningún prompt lo habría clavado a la
  primera, porque nadie sabe qué quiere hasta que lo ve.

Un prompt bueno ahorra las dos primeras horas. Las decisiones siguen siendo
tuyas.
