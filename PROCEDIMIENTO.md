# apps4all.app — procedimiento de puesta en marcha

Documento de trabajo. Objetivo: **que exista una web en https://apps4all.app esta misma semana**, aunque sea pequeña, y que a partir de ahí crecer sea añadir archivos, no rehacer nada.

Regla que gobierna todo el documento: *publicado y modesto gana a perfecto y pendiente.*

---

## 0. Decisiones ya tomadas (y por qué)

Están cerradas a propósito, igual que las convenciones de proyecto del estudio. Si alguna no te encaja, dilo y la cambiamos ahora — reabrirlas dentro de tres semanas es exactamente el tiempo que este documento intenta ahorrar.

| Ámbito | Decisión | Por qué |
|---|---|---|
| Tecnología | **HTML + CSS a mano, sin compilación** | En esta máquina no hay Node ni npm instalados. Sin compilación, "desplegar" es copiar archivos: no hay nada que se pueda romper entre tu carpeta y el servidor. |
| Framework | Ninguno, de momento | Astro entra más adelante sin tirar nada (ver §6). Meterlo hoy son dos o tres horas de instalación antes de escribir la primera línea visible. |
| Repositorio | GitHub, **privado**, `apps4all-web` | Convención del estudio: GitHub desde el primer commit. Privado aunque el contenido acabe siendo público — el repo guarda borradores y notas, no solo el HTML final. |
| Hosting | Hostinger, plan compartido, carpeta `public_html` | Ya lo tienes pagado. |
| Despliegue | Manual la primera vez → GitHub Actions por FTP en cuanto se vea la web | Ver §5. Automatizar antes de comprobar que el dominio funciona es depurar dos cosas a la vez. |
| Idioma | Castellano, con `lang="es"` | Catalán y/o inglés cuando haya contenido que traducir. La estructura de §4 ya lo permite. |
| Analítica | Ninguna en la v1 | Sin cookies de terceros no hace falta banner de consentimiento. Cuando la quieras: Plausible o Umami (sin cookies) antes que Google Analytics. |

### El detalle que rompe todo si no se sabe

**El dominio `.app` obliga a HTTPS.** Google, que gestiona ese TLD, lo tiene en la *lista de precarga HSTS* de los navegadores. Consecuencia práctica: `http://apps4all.app` **no carga con un aviso — no carga en absoluto**. Chrome, Firefox, Safari y Edge se niegan a conectar antes incluso de preguntar al servidor.

No es un problema (Hostinger da certificado gratis), pero invierte el orden de trabajo: **el SSL tiene que estar activo antes de subir el primer archivo**, o vas a ver una página en blanco y a pensar que has subido mal los archivos. Está como paso 1.3.

---

## 1. Lo que tienes que hacer tú (~40 minutos)

Ninguno de estos pasos lo puedo hacer yo: son cuentas, contraseñas y paneles web con tu sesión iniciada.

### 1.1 Comprobar el dominio — 5 min

- [ ] hPanel de Hostinger → **Dominios**. ¿Aparece `apps4all.app`?
  - **Sí, y está en Hostinger** → perfecto, no toques nada.
  - **Sí, pero registrado en otro sitio** (Namecheap, GoDaddy, Porkbun…) → anota dónde. Habrá que apuntar los *nameservers* a Hostinger, y eso tarda entre 1 y 24 horas en propagarse. Hazlo lo primero de todo.
  - **No lo tienes** → cómpralo antes de seguir. Un `.app` ronda los 15-20 €/año. Mejor directamente en Hostinger: te ahorras el paso de los nameservers y la espera.

Resultado: `_______________________________`

### 1.2 Crear el sitio en Hostinger — 5 min

- [ ] hPanel → **Sitios web → Añadir sitio web → Sitio vacío**. No elijas WordPress ni el creador de webs: los dos dejan archivos suyos en `public_html` que luego estorban.
- [ ] Asócialo al dominio `apps4all.app`.
- [ ] En **Administrador de archivos**, comprueba que existe `public_html` y anota su ruta completa (suele ser `/home/uXXXXXXXXX/domains/apps4all.app/public_html`).

Ruta: `_______________________________`

### 1.3 Activar el SSL — 5 min + espera

- [ ] hPanel → **Seguridad → SSL** → instalar el certificado gratuito para `apps4all.app`.
- [ ] Activa también **Forzar HTTPS**.
- [ ] Espera a que el panel diga *Activo*. Puede tardar de 5 minutos a 1 hora.

Hasta que esto esté en verde, la web no se puede ver. No es culpa de los archivos (ver el aviso de §0).

### 1.4 Sacar las credenciales de FTP — 5 min

- [ ] hPanel → **Archivos → Cuentas FTP**. Anota **servidor**, **usuario** y **puerto** (21 para FTP).
- [ ] Si no recuerdas la contraseña, cámbiala ahí mismo.

⚠️ **No me pegues estas credenciales en el chat.** Las necesitas tú en el paso 5.2 y van a un sitio concreto: los *Secrets* de GitHub. En el repositorio nunca — ni en un comentario, ni "temporalmente".

### 1.5 Cuenta de GitHub — 10 min

- [ ] ¿Tienes cuenta? Si no: https://github.com/signup
- [ ] Anota tu nombre de usuario: `_______________________________`
- [ ] Git en este equipo ya está configurado como `jcgualde <jcgualde@yahoo.es>`. Solo falta que ese correo esté también en tu cuenta de GitHub (Settings → Emails) para que los commits te aparezcan atribuidos.
- [ ] **Opcional pero recomendable:** instalar GitHub CLI. Convierte "crear repo, subirlo y configurarlo" en una línea, hoy y en cada proyecto futuro.

```bash
winget install --id GitHub.cli
```

Después, en una terminal nueva (elige *GitHub.com* → *HTTPS* → *Login with a web browser*):

```bash
gh auth login
```

### 1.6 Decidir el contenido — 10 min

Es lo único que no puede salir de una plantilla. Escríbeme las respuestas en el chat, en sucio y sin redactar — de redactar me encargo yo:

- [ ] **Qué proyectos reales puedes enseñar.** Nombre, una línea de qué hace, y si puedes decir el nombre del cliente o hay que anonimizarlo ("una gestoría de Barcelona"). Si hoy solo hay uno, con uno vale.
- [ ] **Cómo quieres que te contacten.** ¿Un correo `hola@apps4all.app`? ¿Formulario? ¿WhatsApp? Recomendación para la v1: correo a secas. Un formulario en hosting compartido necesita PHP y acaba en la carpeta de spam del destinatario.
- [ ] **Datos para el aviso legal** (obligatorio en España por la LSSI-CE cuando la web es de una actividad económica): nombre o razón social, NIF, domicilio y correo de contacto.

---

## 2. Lo que hago yo (siguiente sesión, 1-2 h)

Cuando tengas hecho lo de §1:

1. Estructura completa de §4, con `git init` y el primer commit.
2. Portada con el logotipo horizontal, el claim **Crear, añadir, mejorar** y las tres líneas de trabajo (comercios, fiestas, producto propio), cada una con el `4` en su color de vertical.
3. `proyectos/`, `contacto/` y los dos textos legales.
4. `README.md`, `CLAUDE.md` y `decisiones.md` a partir de las plantillas del estudio.
5. El workflow de GitHub Actions de §5.2, listo para que solo tengas que pegar los *Secrets*.
6. Verificación en el navegador antes de darlo por bueno.

---

## 3. Procedimiento de GitHub

### 3.1 Crear el repositorio

**Con GitHub CLI** (si instalaste `gh`), desde `D:\Claude\Code\apps4all-web`:

```bash
git init && git add -A && git commit -m "chore: estructura inicial del sitio de apps4all"
```

```bash
gh repo create apps4all-web --private --source=. --remote=origin --push
```

**Sin GitHub CLI**, por la web:

1. https://github.com/new
2. Nombre `apps4all-web`, visibilidad **Private**.
3. **No** marques "Add a README", ni `.gitignore`, ni licencia — el repositorio tiene que llegar vacío o el primer `push` chocará.
4. Copia la URL que te da y, desde la carpeta del proyecto:

```bash
git remote add origin https://github.com/TU-USUARIO/apps4all-web.git
```

```bash
git branch -M main && git push -u origin main
```

La primera vez se abre una ventana del navegador para autenticarte (Git Credential Manager). A partir de ahí no vuelve a pedirlo.

### 3.2 Cómo se trabaja a partir de ahí

Convenciones del estudio, aplicadas a la web:

- `main` **siempre desplegable**. Lo que está en `main` es lo que hay publicado.
- Cada cambio en su rama: `feat/pagina-proyectos`, `fix/logo-movil`.
- Commits buscables, formato convencional:

  ```
  feat(proyectos): añadir ficha de la webapp de tickets
  fix(css): corregir el claim cortado en pantallas de 320 px
  ```

  "cambios" y "actualización" convierten el historial en ruido. El commit tiene que contener las palabras por las que lo buscarías dentro de un año.
- Pull request aunque trabajes solo. No es burocracia: es leerte tu propio diff antes de publicarlo, y es la revisión de código más barata que existe.
- **Un issue por cada cosa que dejes a medias**, aunque lo cierres tú en diez minutos. Es donde vive el contexto de "por qué esto está sin terminar", y es lo primero que buscarás al volver de un parón.
- Etiqueta de versión en cada despliegue (`v1.0`, `v1.1`), para poder responder a "esto antes se veía bien".

### 3.3 Lo que nunca entra en el repositorio

El `.gitignore` cubrirá esto, pero la regla importa más que el archivo:

- Contraseñas FTP, tokens, claves de API — **jamás**, ni en una rama, ni en un commit que "luego borro". Un secreto que ha llegado a estar en un commit está comprometido aunque lo borres: queda en el historial.
- `.env` fuera; `.env.example` dentro, con las claves vacías.

---

## 4. Estructura del proyecto

Pensada para que crecer sea *añadir una carpeta*, nunca reorganizar.

```
apps4all-web/
├── index.html                  portada
├── proyectos/index.html        listado de trabajos
├── servicios/index.html        (cuando toque)
├── contacto/index.html
├── legal/
│   ├── aviso-legal.html
│   └── privacidad.html
├── assets/
│   ├── marca/                  los SVG de la skill marca-a4a, sin tocar
│   ├── css/
│   │   ├── a4a-brand.css       variables de marca — no se edita
│   │   └── sitio.css           todo el estilo propio del sitio
│   └── img/
├── .github/workflows/deploy.yml
├── .gitignore
├── README.md                   las cinco preguntas
├── CLAUDE.md                   contexto para asistentes de código
├── decisiones.md               tres líneas por decisión
└── PROCEDIMIENTO.md            este documento
```

Dos detalles que parecen menores y no lo son:

- **Cada página es una carpeta con `index.html`.** Así la URL es `apps4all.app/proyectos/` y no `apps4all.app/proyectos.html`. Cuando dentro de un año pases a Astro, las URLs no cambian y no pierdes el posicionamiento acumulado.
- **`a4a-brand.css` se copia tal cual y no se edita.** Todo color sale de sus variables (`var(--a4a-azul)`), nunca un hex suelto. El día que se afine la paleta, se cambia un archivo y cambia el sitio entero.

### Marca

Se aplica la skill `marca-a4a` sin desviaciones. Lo relevante para la web:

- Logotipo horizontal en la cabecera, con el claim debajo, alineado a su izquierda. Mínimo 120 px de ancho con claim; por debajo se quita el claim, no se encoge.
- **El azul `#2B6FC2` es solo del carácter `4`.** No va en la caja del monograma ni en el resto de letras. Esa restricción es lo que hace que el 4 se lea como "apps **for** all". Si el azul se reparte, la idea se pierde.
- En interfaz sí puede usarse azul para botones y enlaces, pero no pegado al logotipo.
- Favicon: `a4a-icono-minimo-4.svg`.
- Las tres verticales cambian **solo** el color del 4: verde `#1D9E75` comercios, coral `#D85A30` fiestas, morado `#6F66D6` producto propio.

**Pendiente conocido:** los SVG usan una pila de fuentes del sistema y el texto no está vectorizado, así que el logotipo se dibuja algo distinto en cada equipo. Para pantalla vale. Antes de imprimir cualquier cosa —tarjetas, rótulos— hay que elegir la tipografía definitiva y pasar el logotipo a curvas.

---

## 5. Procedimiento de Hostinger

### 5.1 Primera subida, a mano (10 min)

El objetivo de este paso no es el despliegue definitivo, es **ver la web funcionando** para descartar problemas de dominio y de SSL antes de automatizar nada.

1. Comprime el **contenido** de la carpeta del proyecto en un ZIP. Ojo: el ZIP debe llevar `index.html` en su raíz, no una carpeta `apps4all-web` que a su vez contenga el `index.html`. Es el error clásico y deja la web convertida en un listado de directorios.
2. hPanel → **Administrador de archivos** → entra en `public_html`.
3. Si hay un `default.php` o un `index.html` de bienvenida de Hostinger, bórralos. Si hay una carpeta `.well-known`, esa se queda.
4. Sube el ZIP y usa **Extraer** desde el propio administrador.
5. Abre `https://apps4all.app` (con **https**, ver §0).

**Si no carga**, el orden de comprobación de más probable a menos: (a) el SSL todavía en proceso, (b) el ZIP se extrajo dentro de una subcarpeta, (c) los DNS aún propagándose, si el dominio venía de fuera.

### 5.2 Despliegue automático desde GitHub (15 min, una sola vez)

A partir de aquí, `git push` a `main` publica la web. Se acabó el ZIP.

1. En GitHub: **Settings → Secrets and variables → Actions → New repository secret**. Crea tres:

   | Nombre | Valor |
   |---|---|
   | `FTP_SERVER` | el servidor FTP de 1.4 (p. ej. `ftp.apps4all.app`) |
   | `FTP_USERNAME` | el usuario FTP |
   | `FTP_PASSWORD` | la contraseña FTP |

2. El archivo `.github/workflows/deploy.yml` (te lo dejo escrito en la siguiente sesión) queda así:

   ```yaml
   name: Desplegar en Hostinger
   on:
     push:
       branches: [main]
     workflow_dispatch:

   jobs:
     desplegar:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - name: Subir por FTP
           uses: SamKirkland/FTP-Deploy-Action@v4.3.5
           with:
             server: ${{ secrets.FTP_SERVER }}
             username: ${{ secrets.FTP_USERNAME }}
             password: ${{ secrets.FTP_PASSWORD }}
             server-dir: public_html/
             exclude: |
               **/.git*
               **/.git*/**
               **/*.md
               .github/**
   ```

3. Prueba: cambia una palabra, `git push`, y mira la pestaña **Actions** del repositorio. En un minuto debería estar en la web.

`workflow_dispatch` está ahí para poder relanzar el despliegue desde la web de GitHub sin tener que inventarse un commit.

**Por qué esto y no el "Git" de hPanel:** Hostinger tiene despliegue por Git integrado, pero con repositorio privado hay que darle de alta una clave de despliegue y en la práctica da más guerra que los tres *secrets* de arriba. Si algún día el repo pasa a público, es una alternativa válida.

### 5.3 Correo del dominio

Si quieres `hola@apps4all.app`: hPanel → **Correos electrónicos**. El plan compartido de Hostinger incluye correo con límites. Si te quedas corto, Zoho Mail tiene plan gratuito para un dominio.

---

## 6. Cómo se crece a partir de la v1

En este orden. Cada escalón se justifica solo cuando el anterior se ha quedado corto — no antes.

| Cuándo | Qué |
|---|---|
| Ahora | Portada + contacto + legal, publicado. **Este es el objetivo.** |
| Cuando haya 2-3 trabajos | Página de proyectos con una ficha por trabajo. Sigue siendo HTML suelto. |
| Cuando repetir la cabecera en 6 archivos moleste | **Aquí entra Astro.** Instalas Node y Astro se traga el HTML que ya existe casi sin tocarlo: mueves cabecera y pie a un *layout* y las páginas se quedan igual. El despliegue cambia en una línea (`dist/` en vez de la raíz). Ese es el momento correcto, no antes. |
| Cuando quieras publicar seguido | Blog o notas en Markdown. Astro lo trae de serie. |
| Cuando alguien pida presupuesto por la web | Formulario. En estático se resuelve con Formspree o Web3Forms, sin montar servidor. |
| Cuando importe de dónde llega la gente | Analítica sin cookies (Plausible, Umami). Con cookies necesitarías banner de consentimiento. |
| Cuando haya una app propia que enseñar | Subdominio o carpeta por producto: `apps4all.app/habitos/`. La estructura de §4 ya lo aguanta. |

**Lo que no hay que hacer nunca**, porque es el camino conocido a no tener web: rehacer la v1 antes de publicarla. Si algo del diseño no te gusta, se publica igual y se arregla la semana siguiente sobre algo que ya está vivo.

---

## 7. Lo que queda por decidir

Se resuelve cuando toque, no hoy:

- Tipografía definitiva de la marca (candidatas: Söhne, Aeonik, General Sans) y vectorizado del logotipo.
- Si la web lleva catalán además de castellano.
- Si los proyectos de cliente se enseñan con nombre o anonimizados. Hay que pedir permiso a cada cliente antes de publicar su nombre o sus capturas.
