# Lo que tienes que hacer tú

Esquema de trabajo de apps4all.app. Lo que aparece aquí es lo que **no puedo
hacer yo**: son cuentas, contraseñas, paneles con tu sesión iniciada y
decisiones que solo puedes tomar tú.

Está ordenado por fases. **No saltes de fase.** El orden no es estético: cada
fase descarta un problema antes de que se mezcle con el siguiente, que es la
diferencia entre depurar una cosa y depurar tres a la vez.

---

## Fase 0 — Desbloquear (≈45 min, hoy)

Sin esto no se puede publicar nada.

### 0.1 Crear el buzón de correo — 5 min

- [ ] hPanel → **Correos electrónicos** → crear `jcgualde@apps4all.app`.
- [ ] Comprueba que recibes un correo de prueba antes de seguir.

Por qué primero: la clave de Web3Forms se da de alta contra un correo que ya
exista, y el aviso legal obliga a publicar una dirección de contacto real.

### 0.2 Dar de alta el formulario en Web3Forms — 5 min

- [ ] Entra en <https://web3forms.com>, pon `jcgualde@apps4all.app` y pulsa
      *Create Access Key*.
- [ ] Te llega la clave por correo. Es un código largo tipo
      `a1b2c3d4-e5f6-...`.
- [ ] Pégala en `textos/config.json`, en `web3forms_clave`, sustituyendo el
      texto `PENDIENTE-...`.

Esa clave **va en el HTML y es pública**; no es un secreto y no pasa nada. Lo
único que permite es mandarte correo a ti. No la confundas con las claves de
FTP, que sí lo son.

### 0.3 Rellenar los datos del aviso legal — 5 min

En `textos/config.json`, sustituye los tres `PENDIENTE`:

- [ ] `titular` — tu nombre y apellidos, o la razón social si facturas por sociedad.
- [ ] `nif` — tu NIF o el CIF de la sociedad.
- [ ] `domicilio` — dirección completa.

Es obligatorio por el artículo 10 de la LSSI-CE en cuanto la web es de una
actividad económica. No es opcional y las sanciones existen.

### 0.4 Comprobar el SSL — 5 min + espera

- [ ] hPanel → **Seguridad → SSL** → certificado gratuito para `apps4all.app`.
- [ ] Activa **Forzar HTTPS**.
- [ ] Espera a que ponga *Activo*.

Recuerda: `.app` **solo funciona por HTTPS**. Sin el certificado en verde no
verás la web, y no será culpa de los archivos.

### 0.5 Regenerar y mirar — 2 min

```bash
python construir.py
```

```bash
python -m http.server 4322 --directory publico
```

- [ ] Abre <http://localhost:4322> y lee la web entera, en los tres idiomas.
- [ ] Apunta lo que quieras cambiar. Los textos están en `textos/es.json`,
      `en.json` y `ca.json`.

---

## Fase 1 — Publicar a mano (≈20 min)

El objetivo no es el despliegue definitivo: es **ver la web viva** y descartar
de golpe los problemas de dominio y certificado.

- [ ] Comprime el **contenido de `publico/`** en un ZIP. Ojo: el `index.html`
      tiene que quedar en la raíz del ZIP, no dentro de una carpeta `publico`.
      Es el error clásico y deja la web convertida en un listado de archivos.
- [ ] hPanel → **Administrador de archivos** → entra en `public_html`.
- [ ] Borra el `index.html` o `default.php` de bienvenida de Hostinger si los hay.
      La carpeta `.well-known`, si existe, **se queda**.
- [ ] Sube el ZIP y pulsa **Extraer**.
- [ ] Abre `https://apps4all.app` (con **https**).
- [ ] Prueba el formulario de contacto y comprueba que te llega el correo.

Si no carga, en este orden: (a) el SSL aún en proceso, (b) el ZIP se extrajo
dentro de una subcarpeta, (c) DNS todavía propagándose.

**Cuando esto funcione, ya tienes web.** Todo lo que viene después es comodidad.

---

## Fase 2 — Automatizar el despliegue (≈20 min, una sola vez)

A partir de aquí, `git push` publica. Se acabó el ZIP.

### 2.1 Subir el proyecto a GitHub

- [ ] Dime tu **usuario de GitHub** y si al crear el repositorio marcaste
      *Add a README*. Con eso te doy las órdenes exactas.

### 2.2 Guardar las claves de FTP en GitHub

- [ ] hPanel → **Archivos → Cuentas FTP**. Anota servidor, usuario y contraseña.
- [ ] En GitHub: **Settings → Secrets and variables → Actions → New repository
      secret**, y crea tres: `FTP_SERVER`, `FTP_USERNAME`, `FTP_PASSWORD`.

⚠️ **Las claves de FTP no me las pegues nunca en el chat, ni las escribas en
ningún archivo del proyecto.** Un secreto que ha llegado a estar en un commit
está comprometido aunque lo borres después: queda en el historial para siempre.

### 2.3 Probar

- [ ] Cambia una palabra en `textos/es.json`, haz `git push`, y mira la pestaña
      **Actions** del repositorio. En un minuto debería estar en la web.

---

## Fase 3 — Que la web trabaje (semanas siguientes)

Por orden de rentabilidad, no de dificultad.

- [ ] **Capturas reales de la WebApp de tickets.** Hoy las muestras son
      marcadores de posición grises. Una captura real vale más que tres
      párrafos de texto: es lo que convierte la web en una carta de venta.
- [ ] **Permiso al cliente.** Pregunta a la gestoría si puedes citarla por su
      nombre y enseñar capturas. Hasta que digan que sí, se queda anonimizada.
      Un caso con nombre convence mucho más que "una gestoría de Barcelona".
- [ ] **Un segundo trabajo que enseñar**, aunque sea pequeño o interno.
      Con uno solo, la web parece un experimento; con dos, un estudio.
- [ ] **Dar de alta el dominio en Google Search Console** y enviar el
      `sitemap.xml` que ya genera el script. Es gratis y es la única forma de
      saber si alguien te encuentra.
- [ ] **Enlazar la web desde tu firma de correo y tu LinkedIn.** El tráfico de
      los primeros meses no viene de Google, viene de gente que ya te conoce.

---

## Fase 4 — Trabajar de forma profesional y rentable

Esto ya no es la web: es el negocio alrededor. Lo pongo porque lo has pedido y
porque es donde se gana o se pierde el dinero.

### Antes de aceptar el primer encargo

- [ ] **Una tarifa escrita**, aunque sea para ti solo. Precio por hora de
      referencia y precio cerrado por tipo de trabajo. Sin esto, presupuestarás
      por intuición y siempre a la baja.
- [ ] **Un modelo de presupuesto** de una página: alcance, qué NO incluye, plazo,
      precio, forma de pago. El apartado de "qué no incluye" es el que evita
      discusiones.
- [ ] **Condiciones de mantenimiento.** Una aplicación viva necesita horas
      todos los meses. Si no se cobran desde el principio, se regalan para
      siempre.
- [ ] **Pago por fases**: una parte al encargar, el resto al entregar. Es lo
      normal en el sector y filtra a los clientes que no iban en serio.

### En cada proyecto

- [ ] **Un repositorio por proyecto, privado, desde el primer día.**
- [ ] **Copia de seguridad de lo que no está en el repositorio**: bases de
      datos, credenciales, material del cliente.
- [ ] **Un documento de decisiones por proyecto** (tres líneas por decisión:
      qué, por qué, cuándo). Es lo que te salva cuando vuelvas al proyecto
      dentro de ocho meses.
- [ ] **Contrato de encargado del tratamiento** si vas a manejar datos
      personales de terceros, que es exactamente el caso de la WebApp de
      tickets. Esto lo sabes mejor que yo por tu trabajo en la gestoría.

### Rutina que evita casi todos los desastres

| Cuándo | Qué |
|---|---|
| En cada cambio | Rama nueva, commit con mensaje buscable, pull request aunque trabajes solo |
| Cada semana | Mirar Actions: que no haya despliegues fallando en silencio |
| Cada mes | Revisar horas dedicadas frente a lo presupuestado. Es el único dato que dice si un tipo de trabajo es rentable |
| Cada trimestre | Repasar los `PENDIENTE` de los proyectos y cerrarlos o descartarlos |

---

## Lo que sigue pendiente de decidir

- Tipografía definitiva de la marca y vectorizado del logotipo. Hoy los SVG
  usan fuentes del sistema y se dibujan distinto en cada equipo. Para pantalla
  vale; **antes de imprimir nada** hay que cerrarlo.
- Si la ficha de la gestoría se publica con nombre o anonimizada.
- Si en algún momento interesa analítica (Plausible o Umami, sin cookies, para
  no tener que poner banner de consentimiento).
