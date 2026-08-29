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
