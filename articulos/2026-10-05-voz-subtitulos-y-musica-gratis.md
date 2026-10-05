titulo: Voz, subtítulos y música sin pagar: lo que funciona en Remotion (y lo que no)
fecha: 2026-10-05
resumen: Una voz sintética que corre en tu propio ordenador, subtítulos palabra a palabra sin transcribir nada y la reclamación de derechos que nos llevamos por una música gratuita. Segunda de tres partes.
borrador: no
---
En la primera parte monté el esqueleto: Remotion, un asistente de IA y las skills oficiales. El vídeo se ve. Ahora toca que se oiga, y que se entienda sin sonido.

Aquí no hay atajos: la voz es lo que más delata un vídeo hecho por máquinas, y la música es donde más fácil es meterse en un lío legal. Cuento lo que probé, lo que descarté y por qué.

## La voz: probar de oído, no de catálogo

Hay servicios de pago que hoy suenan casi humanos. ElevenLabs es el más conocido. Pero yo quería algo gratis, que funcionara en mi ordenador y que pudiera usar en vídeos comerciales. Eso deja fuera más opciones de las que parece: varios modelos abiertos muy buenos, como XTTS o F5-TTS, tienen licencias que prohíben el uso comercial.

Probé cuatro, siempre con la misma frase y escuchando el resultado:

- **Las voces de Windows.** Gratis y sin instalar nada. Suenan a lo que son.
- **Piper**, con dos voces en castellano entrenadas con datos libres. Claras, pero planas.
- **Kokoro**, un modelo de 82 millones de parámetros con licencia Apache 2.0. Su voz masculina en español, «Alex», fue la que elegimos.
- **ElevenLabs**, como referencia de lo que se consigue pagando.

Kokoro no suena humano. Pero suena digno, corre en el procesador sin tarjeta gráfica y no depende de ningún servicio externo. Reconozco que le falta sentimiento y es muy plano, pero como primera aproximación al tema me vale.

## Tres ajustes que cambian mucho

La voz en bruto salía acelerada y monótona. Lo que más mejoró el resultado no fue cambiar de modelo, sino cómo le paso el texto.

**Generar frase a frase, y trozo a trozo.** Corto cada frase del guion en los signos de puntuación, genero cada trozo por separado y meto silencios reales entre ellos. Medio segundo después de un punto, menos de dos décimas después de una coma. Es lo que hace una persona al hablar, y el modelo por sí solo no lo hace bien.

**Bajar la velocidad.** Al 85 % de la velocidad normal, la voz pierde buena parte de su prisa artificial.

**Marcar el énfasis en el propio guion.** Cada línea del guion puede llevar ajustes delante, y una barra marca una pausa larga:

```
{velocidad=0.8 volumen=1.25} En la tercera parte: | trucos para sacarle todo el partido a Remotion.
```

Es poca cosa, pero permite que el gancho y el cierre suenen distintos del resto.

Un último detalle práctico: los nombres en inglés hay que escribirlos como se pronuncian. Si el guion dice «Claude Code», un modelo en español lo leerá como si fuera castellano, sílaba a sílaba. Si dice «clod coud», lo dice bien.

## Subtítulos sin transcribir

La mayoría de la gente ve los vídeos en el móvil y sin sonido. Sin subtítulos, el vídeo pierde a la mitad del público antes de empezar.

La vía habitual es transcribir el audio con Whisper. La skill oficial de subtítulos de Remotion lo propone así. Pero en nuestro caso hay un atajo: la voz sale de nuestro propio guion. Ya sabemos qué se dice. Solo falta saber cuándo.

Como genero el audio trozo a trozo, sé con exactitud dónde empieza y acaba cada trozo. Dentro de cada uno detecto dónde suena voz de verdad, quitando el silencio de los bordes, y reparto las palabras según su longitud. El resultado es una lista con el momento de cada palabra:

```json
{ "text": " 240.000", "startMs": 2083, "endMs": 3533 }
```

No es exacto al milisegundo: dentro de un trozo de dos o tres palabras, el reparto es una estimación. Pero como los trozos son cortos, el error se queda en décimas de segundo, y en pantalla no se nota.

Dos ventajas que no tendría transcribiendo. Los subtítulos dicen exactamente lo que dice el guion, sin faltas. Y puedo hacer que se lea una cosa y se vea otra:

```
Solo el año pasado se formaron [240.000|doscientos cuarenta mil] hogares nuevos.
```

La voz lee «doscientos cuarenta mil» y el subtítulo enseña «240.000».

### Cómo se muestran

Frases cortas, de tres a seis palabras, con la palabra que suena resaltada. Dos detalles que aprendí mirando el vídeo en el móvil:

- **En vertical, en el centro.** La franja de abajo la tapan los botones de TikTok, Instagram y YouTube Shorts.
- **Sin palabras sueltas.** Si al final de una frase quedan una o dos palabras, se suman a la página anterior. Una palabra sola en pantalla parece un error.

Para YouTube, en vez de grabarlos en la imagen, genero un archivo `.srt` con las mismas frases y lo subo junto al vídeo. YouTube lee esos subtítulos, y eso le ayuda a entender de qué trata el vídeo y a mostrarlo en las búsquedas.

## La música: gratis no es lo mismo que libre

Aquí va la lección cara.

Para el fondo elegí una pista de un banco de música gratuito. Me tomé la molestia de descartar todas las que llevaban la etiqueta de Content ID, el sistema con el que YouTube identifica música con dueño. Elegí una que no la tenía.

Al subir el vídeo, YouTube la reclamó igualmente, a nombre de una canción que no tenía nada que ver. No es raro: hay quien registra música gratuita como si fuera suya. La reclamación no borra el vídeo, pero el reclamante puede quedarse con los ingresos o bloquearlo en algunos países.

Lo resolví con la herramienta de YouTube Studio que quita solo la música y deja la voz. Pero la conclusión para los siguientes vídeos fue clara:

- **Para YouTube**, música de su propia Biblioteca de audio, que está pensada para no dar reclamaciones.
- **Para TikTok e Instagram**, la música de la propia aplicación, que tiene la licencia pagada por la plataforma.
- **Y en Remotion, la música como interruptor.** Cada vídeo tiene una opción `musica`, y sacar una versión sin ella es una sola orden.

Cuando sí hay música, baja sola mientras habla la voz y sube en los silencios. En Remotion es una función del fotograma, como todo:

```ts
const volumenMusica = (f: number) => {
  const hablando = Math.max(
    ...voces.map((v) => interpolate(f, [v.desde - 8, v.desde, v.desde + v.dura, v.desde + v.dura + 10], [0, 1, 1, 0], fijo)),
  );
  return 0.18 + (0.06 - 0.18) * hablando;
};
```

## Conclusión

Es un comienzo, y no es malo, pero no me acaba de convencer del todo. Como alternativa gratuita es lo mejor que he encontrado, pero creo que debo mejorar.

## Lo que viene

En la tercera parte, seis trucos de Remotion que usamos para trabajar rápido: revisar sin exportar, sacar dos formatos de una misma escena, variantes sin duplicar código, que el vídeo se ajuste solo a la voz, animaciones suaves y miniaturas hechas con el mismo código.
