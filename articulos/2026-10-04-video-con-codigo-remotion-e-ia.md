titulo: Vídeo hecho con código: Remotion y un asistente de IA, de cero a MP4
fecha: 2026-10-04
resumen: Cómo monto vídeos sin editor de vídeo: Remotion para describirlos en React, un asistente de IA para escribir el código y las skills oficiales para que no se invente nada. Primera de tres partes.
borrador: no
---
Llevo unas semanas haciendo vídeos sin abrir un editor de vídeo. Ni línea de tiempo, ni capas, ni exportaciones a mano. Cada vídeo es un proyecto de código, y el código lo escribe una IA mientras yo miro el resultado y pido cambios.

Esta es la primera de tres entradas sobre cómo lo hago. Aquí va la base: qué es Remotion, cómo se monta el entorno y cómo se trabaja con la IA sin que se invente la mitad de las cosas.

## Por qué vídeo con código

La pregunta razonable es para qué complicarse, si existen CapCut y compañía. Mi respuesta es práctica: porque un vídeo hecho con código se puede repetir.

Si un dato cambia, cambio una línea y el vídeo se vuelve a generar. Si quiero la versión vertical y la horizontal, salen de la misma escena. Si quiero diez vídeos con la misma plantilla, la plantilla es una función. Y todo queda en Git, con su historial, como cualquier otro proyecto.

Yo no vengo del desarrollo, me estoy introduciendo en ello gracias a la IA. Una de las cosas que más rápido he aprendido es la importancia de crear un flujo de trabajo, y lo que explico aquí es justamente eso: un flujo de trabajo para crear vídeos gratis, rápidos y exportables.

## Qué es Remotion

[Remotion](https://www.remotion.dev) es un framework para hacer vídeos con React. Cada fotograma es un componente que se pinta en un navegador sin ventana, y al final todo se codifica en un MP4 normal.

La idea central cabe en una frase: el vídeo es una función del número de fotograma. No hay animaciones que «corren»: hay un `frame` que va de 0 al final, y cada cosa decide cómo se ve en función de ese número.

```tsx
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";

export const MiVideo = () => {
  const frame = useCurrentFrame();
  const opacidad = interpolate(frame, [0, 30], [0, 1], { extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
      <h1 style={{ opacity: opacidad }}>¡Hola!</h1>
    </AbsoluteFill>
  );
};
```

Ese componente se registra como una composición, con su tamaño, sus fotogramas por segundo y su duración:

```tsx
<Composition id="mi-video" component={MiVideo} width={1080} height={1920} fps={30} durationInFrames={150} />
```

Y ya está. Eso es un vídeo vertical de cinco segundos donde un texto aparece fundiendo durante el primer segundo.

Un dato importante antes de seguir: la licencia. Remotion es gratis para particulares, para organizaciones sin ánimo de lucro y para empresas de hasta tres empleados, también para uso comercial. Por encima de eso hay que pagar licencia de empresa. Para un estudio pequeño como el mío, entra en lo gratuito.

## El entorno

Hace falta Node.js. Con eso, cuatro órdenes:

```
npx create-video@latest
npx skills add remotion-dev/skills
npx remotion studio
npx remotion render mi-video out/mi-video.mp4
```

La primera crea el proyecto. La tercera abre Remotion Studio, un editor en el navegador con el vídeo, su línea de tiempo y la posibilidad de avanzar fotograma a fotograma. La cuarta exporta el MP4.

La segunda es la que más me ha cambiado el resultado, y merece su propio apartado.

## Las skills: que la IA no adivine

Mi primer intento fue pedirle a la IA el vídeo sin más contexto. Funcionó, pero con letra pequeña. La IA usaba un componente de audio que Remotion ya ha sustituido por otro, y escribía a mano las duraciones de cada escena cuando se pueden calcular a partir del propio audio.

Nada de eso rompía el vídeo. Pero cada detalle era una vuelta más, y en cuanto cambiaba una frase había que recolocar los números a mano.

Los propios autores de Remotion publican un conjunto de instrucciones pensadas para asistentes de IA: las llaman skills. Son documentos que la IA consulta antes de escribir código, con las buenas prácticas actuales de cada área: audio, subtítulos, fuentes, exportación, mapas. Se instalan con `npx skills add remotion-dev/skills`, y en mi caso fueron doce.

La diferencia se nota en la primera respuesta. Con las skills, la IA usa el componente de audio actual, carga las fuentes con el paquete oficial y te propone calcular la duración del vídeo a partir del audio en vez de escribir números a mano.

Sirven para cualquier asistente que trabaje con archivos en tu ordenador. Yo uso Claude Code, pero las skills están pensadas también para otros.

## El ciclo de trabajo

Con todo montado, el trabajo diario es un ciclo corto:

- Le describo a la IA el vídeo que quiero, con formato, duración y texto concretos.
- Ella escribe o cambia los componentes.
- Lo miro en Studio y le pido correcciones con palabras, no con código: «más lento», «este texto más grande», «que la barra crezca cuando se nombra la cifra».

Cuanto más concreta es la petición, menos vueltas. «Hazme un vídeo vertical de quince segundos que presente mi aplicación, con su logo y tres frases» funciona mucho mejor que «hazme un vídeo bonito de mi app».

Y una costumbre que me ha salvado varias veces: un commit por cada cambio que funciona. Probar ideas es barato cuando volver atrás cuesta un segundo.

## Lo que no te cuentan

Dos cosas que aprendí por las malas en las primeras semanas.

La primera: lo que más delata un vídeo casero no es la animación, son los dibujos. Mi primera versión era una pizarra con dibujos hechos a base de líneas y cajas, y la opinión fue clara: demasiado casera. Lo que lo arregló fue usar iconos de una colección hecha por diseñadores, con licencia libre, en vez de dibujos improvisados. La IA dibuja geometría muy bien. Ilustra mal.

La segunda: exportar es lento si lo haces a ciegas. Un vídeo de tres minutos tarda unos tres o cuatro minutos en exportarse en mi ordenador, un i5 de hace unos años. Si exportas el vídeo entero para comprobar un detalle, pierdes la tarde. Hay una forma mucho mejor de revisar, y la cuento en la tercera entrada.

## Lo que viene

En la segunda parte, la voz, los subtítulos y la música, todo sin pagar: una voz sintética que funciona en tu ordenador, subtítulos palabra a palabra sin transcribir nada, y la reclamación de derechos de autor que nos llevamos por una música que parecía gratis.
