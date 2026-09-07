# apps4all.app

Sitio web de apps4all. HTML estático generado con un script de Python, sin
frameworks y sin dependencias externas.

## Qué es esto

Una web de cinco tipos de página (portada, tres líneas de trabajo, contacto y
dos textos legales) publicada en tres idiomas: castellano, inglés y catalán.
Los textos viven en archivos aparte, así que una corrección se hace una vez y
sale en los tres sitios.

## Cómo se trabaja

```bash
python construir.py
```

Eso lee las plantillas y los textos y escribe el sitio completo en `publico/`.
Para verlo en el navegador, desde la raíz del proyecto:

```bash
python -m http.server 4322 --directory publico
```

Y abrir <http://localhost:4322>.

> **Importante:** `--directory publico` no es opcional. Si entras en la carpeta
> `publico` con `cd` antes de levantar el servidor, Windows la deja bloqueada y
> `construir.py` no puede vaciarla en la siguiente ejecución.

## Dónde se toca cada cosa

| Quieres cambiar… | Archivo |
|---|---|
| Un texto, un titular, una muestra de trabajo | `textos/es.json`, `textos/en.json`, `textos/ca.json` |
| El correo, el dominio, la clave de Web3Forms, el NIF | `textos/config.json` |
| El aviso legal o la política de privacidad | `textos/legal.json` |
| La estructura de una página | `plantillas/*.html` |
| Colores, tipografías, espaciados | `assets/css/sitio.css` |
| Los colores de la marca | `assets/css/a4a-brand.css` — **no se edita** |
| Cómo se ensambla todo | `construir.py` |

**`publico/` no se edita nunca.** Se borra y se vuelve a escribir en cada
ejecución de `construir.py`; cualquier cambio hecho ahí se pierde. Por eso está
en `.gitignore`.

## Cómo escribir un artículo del blog

El blog está **solo en castellano**, a propósito: si hubiera que escribir cada
artículo tres veces, no se escribiría ninguno.

Para publicar uno nuevo hay que hacer dos cosas.

**1. Crear el archivo.** Va en la carpeta `articulos/`, con la extensión
`.md`, y el nombre empieza por la fecha para que se ordenen solos:

```
articulos/2026-09-14-lo-que-sea.md
```

Lo que va detrás de la fecha es la dirección que tendrá en la web. En el
ejemplo sería `apps4all.app/es/blog/lo-que-sea/`. Sin acentos, sin eñes y sin
espacios: guiones.

**2. Escribirlo.** Arriba van los datos, después una línea con tres guiones, y
debajo el texto:

```
titulo: Lo que sea
fecha: 2026-09-14
resumen: Una o dos frases. Es lo que se lee en el listado del blog.
borrador: no
---
Aquí empieza el artículo.
```

Los cuatro datos de arriba son obligatorios menos `borrador`. Si pones
`borrador: si`, el artículo se queda en el ordenador y no sale en la web: sirve
para ir escribiendo sin publicar.

### Cómo dar formato al texto

No hace falta escribir HTML. Basta con esto:

| Se escribe | Sale |
|---|---|
| Una línea en blanco entre bloques | Un párrafo nuevo |
| `## Titular` | Un título de sección |
| `### Titular` | Un título más pequeño |
| `- cosa` (varias líneas seguidas) | Una lista de puntos |
| `> frase` | Una cita destacada |
| `**importante**` | **negrita** |
| `*matiz*` | *cursiva* |
| `` `código` `` | Texto en monoespaciada |
| `[texto](https://ejemplo.com)` | Un enlace |

Cualquier otra cosa se escribe tal cual y sale como un párrafo normal.

### Sobre el estilo

Los artículos los escribe él, no Claude. Existe una skill personal,
`mi-estilo`, sacada de leer 145 mensajes suyos, que describe cómo escribe
y qué tics de IA hay que quitar. Se activa sola al redactar o revisar
cualquier texto que salga con su nombre.

El reparto normal es: él manda el borrador y Claude corrige ortografía,
parte párrafos largos y señala lo que no se entiende, **sin reescribir las
frases que ya funcionan**. El blog existe para que coja el hábito de
escribir; si se lo escribe Claude, deja de servir para eso.

### Para verlo antes de publicar

```
python construir.py
```

Y abrir `publico/es/blog/` en el navegador. Si algo del archivo está mal
—falta la línea de tres guiones, o falta el título— el programa lo dice por
pantalla al construir y se salta ese artículo, en vez de romperse.

## Cómo se publica

`git push` a `main`. GitHub Actions ejecuta `construir.py` y sube `publico/` a
`public_html` por FTP. El workflow está en `.github/workflows/deploy.yml` y
necesita tres *secrets* configurados en el repositorio: `FTP_SERVER`,
`FTP_USERNAME` y `FTP_PASSWORD`.

## Decisiones que conviene no reabrir sin motivo

- **Sin frameworks y sin dependencias.** El generador usa solo la librería
  estándar de Python para que funcione en cualquier equipo y en GitHub Actions
  sin instalar nada. Astro entra el día que esto se quede corto, no antes.
- **Una carpeta por idioma** (`/es/`, `/en/`, `/ca/`) con las mismas rutas.
  Son URLs reales, indexables, con `hreflang` entre ellas.
- **Los nombres de vertical no se traducen.** `apps4comercios`, `apps4fiestas`
  y `apps4salud` son marca, y la marca no se traduce.
- **Sin cookies ni analítica de terceros.** Por eso no hay banner de consentimiento.
- **El azul `#2B6FC2` es exclusivo del carácter `4`.** Cada vertical cambia
  únicamente el color de ese `4`, mediante la variable `--color-linea`.

## Lo que falta

- Rellenar `titular`, `nif` y `domicilio` en `textos/config.json`: sin eso, el
  aviso legal no cumple la LSSI.
- Pegar la clave de Web3Forms en `textos/config.json`, o el formulario no envía.
- Dar de alta el buzón `jcgualde@apps4all.app` en Hostinger.
- Sustituir los marcadores de pantalla de las muestras por capturas reales.
- Confirmar con el cliente si su nombre puede aparecer en la ficha de tickets.
