titulo: Seis trucos de Remotion que usamos para trabajar rápido
fecha: 2026-10-05
resumen: Revisar sin exportar, dos formatos de una misma escena, variantes con props, duración calculada a partir del audio, animaciones con spring y miniaturas con el mismo código. Tercera y última parte.
borrador: no
---
En las dos primeras partes monté el entorno y le puse voz, subtítulos y música a los vídeos. Esta última va de oficio: seis cosas de Remotion que, juntas, son la diferencia entre hacer un vídeo y poder hacer veinte.

Todas las hemos usado en los vídeos de esta misma serie.

Aviso: es la parte más técnica de las tres. Yo no entiendo todo el código que hay aquí, y no ha hecho falta. Lo que sí hace falta es saber qué pedir. Cada uno de estos trucos nació de una petición mía con el vídeo delante: «¿podemos tener versión horizontal para YouTube?», «sácame también las verticales sin música», «no puede ser que lo primero que se vea sea una pantalla en blanco». La IA pone el código. El criterio lo tienes que poner tú.

## 1. Revisar sin exportar

Exportar un vídeo de tres minutos me lleva tres o cuatro minutos. Si para comprobar un detalle hay que exportarlo entero, el día se va en esperas.

Remotion puede sacar un solo fotograma como imagen, en segundos:

```
npx remotion still mi-video out/mi-video.png --frame=0
```

Mi rutina antes de exportar nada: saco el final de cada escena, cuando ya está todo dibujado, y los junto en una sola imagen. Con un vistazo veo si algo se monta encima de otra cosa o se sale de la pantalla.

Y hay un fotograma que hay que mirar siempre: el primero. Lo aprendí con un vídeo en el que el 90 % de la gente se fue antes de cinco segundos. Empezaba con una pantalla en blanco y en silencio, porque la primera escena entraba fundiendo y la voz arrancaba tarde. Desde entonces, el fotograma 0 de cada vídeo ya tiene el titular, la imagen clave y la voz sonando.

## 2. Un vídeo, dos formatos

YouTube quiere horizontal. TikTok, Instagram y los Shorts, vertical. Hacer dos vídeos es duplicar trabajo y equivocarse en uno de los dos.

En Remotion, el mismo componente puede registrarse dos veces, con tamaños distintos y una prop que le dice en qué formato está:

```tsx
<Composition id="tutorial" component={Tutorial} defaultProps={{ formato: "vertical" }}
  width={1080} height={1920} fps={30} durationInFrames={total} />
<Composition id="tutorial-youtube" component={Tutorial} defaultProps={{ formato: "horizontal" }}
  width={1920} height={1080} fps={30} durationInFrames={total} />
```

Cada escena dibuja su contenido en un lienzo fijo, y un componente de disposición lo coloca: arriba y abajo en vertical, a izquierda y derecha en horizontal. Escribo la escena una vez y salen las dos versiones.

## 3. Variantes sin duplicar nada

Las props no sirven solo para el formato. Son interruptores. Nuestros vídeos tienen dos más: `subtitulos` y `musica`.

Para YouTube saco el horizontal sin subtítulos grabados, porque los subo aparte como archivo `.srt`. Para el móvil, el vertical con ellos. Y cuando YouTube nos reclamó la música de un vídeo, la versión sin música salió con una sola orden:

```
npx remotion render tutorial-youtube out/sin-musica.mp4 --props='{"formato":"horizontal","musica":false}'
```

Ni una línea de código nueva.

## 4. Que el vídeo se ajuste a la voz

Al principio escribía a mano en qué fotograma empezaba cada escena. Funcionaba hasta que cambiaba una frase del guion. Entonces había que recolocarlo todo.

Ahora la duración sale del audio. El programa que genera la voz guarda lo que dura cada frase, y una función calcula a partir de ahí dónde empieza cada escena y cada frase:

```ts
const planificar = (escenas: EscenaPlan[], duraciones: number[], fps: number) => {
  let t = 0;
  let frase = 0;
  const calculadas = escenas.map((e) => {
    const desde = t;
    let cursor = desde + (e.antes ?? 10);
    const voces = [];
    for (let k = 0; k < e.frases; k++) {
      const dura = Math.ceil(duraciones[frase] * fps);
      voces.push({ frase, desde: cursor, dura });
      cursor += dura + (k < e.frases - 1 ? (e.entre ?? 8) : 0);
      frase++;
    }
    t = cursor + (e.despues ?? 24);
    return { desde, largo: t - desde, voces };
  });
  return { escenas: calculadas, total: t };
};
```

Dentro de cada escena, los dibujos no se colocan en fotogramas fijos, sino en momentos de la voz: «cuando la frase va por la mitad» o «cuando dice la palabra *música*», que se busca en los subtítulos. Si la voz cambia, todo se recoloca solo.

Remotion tiene además `calculateMetadata`, que permite que la duración total de la composición se calcule al cargar. Para vídeos que dependen de archivos externos es la forma recomendada.

## 5. Animaciones suaves

En Remotion no hay transiciones automáticas. Si mueves algo de un fotograma al siguiente, salta. Las dos funciones que lo arreglan son `interpolate`, que convierte un tramo de fotogramas en un tramo de valores, y `spring`, que simula un muelle:

```tsx
const frame = useCurrentFrame();
const { fps } = useVideoConfig();
const crece = spring({ frame: frame - inicio, fps, config: { damping: 200 } });
const alto = valor * escala * crece;
```

Con eso, una barra de un gráfico crece con naturalidad y una cifra puede contar de cero a su valor mientras la voz la nombra. La regla que sigo: nada entra ni sale de golpe. Todo funde, crece o se desliza, aunque sea en un tercio de segundo.

## 6. La miniatura, con el mismo código

La miniatura de YouTube es una imagen de 1280×720. En Remotion, una imagen fija es una composición de un solo fotograma: un `Still`.

```tsx
<Still id="miniatura" component={Miniatura} width={1280} height={720} />
```

```
npx remotion still miniatura out/miniatura.jpg --image-format=jpeg
```

La ventaja es que la miniatura usa los mismos componentes, letras y colores que el vídeo. Si cambio el título de un capítulo, cambian a la vez el vídeo y su miniatura. Y una regla de diseño que conviene programar: dejar libre la esquina de abajo a la derecha, porque ahí YouTube pone la duración.

## Para cerrar

Ninguno de estos trucos es complicado por separado. Lo que cambia las cosas es tenerlos todos a la vez: una escena se escribe una vez, se revisa en segundos, sale en dos formatos y con las variantes que haga falta, se ajusta sola a la voz y trae su miniatura.

Una confesión: la primera versión de esta tercera parte no hablaba de Remotion, sino de consejos generales para hacer vídeos. La descarté, porque eso ya lo cuenta mucha gente. Probar, mirar el resultado y tirar lo que no sirve también forma parte del método. Sin miedo a experimentar: con Git, volver atrás cuesta un segundo.

Con esto, la serie está completa. Todo lo que hemos usado es gratis, y el código lo ha escrito una IA.
