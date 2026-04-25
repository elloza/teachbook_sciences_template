# 1. ¿Qué es un TeachBook?

Un **TeachBook** es un libro docente digital construido a partir de archivos de texto, código y recursos multimedia, que luego se compila para obtener una **web navegable** y, en muchos casos, también una **versión PDF**.

Dicho de forma simple:

- tú editas **contenido fuente**
- el sistema lo **compila**
- obtienes un libro **bonito, funcional y publicable**

```{figure} ../../_static/images/1_Que_es_un_teachbook.png
---
name: fig-que-es-un-teachbook
alt: Esquema visual de qué es un TeachBook
width: 85%
align: center
---
Un TeachBook parte de contenido editable y genera una web docente publicable.
```

## Atribución y origen

Esta plantilla se apoya en el ecosistema original de:

- [TeachBooks](https://teachbooks.io/)
- [Jupyter Book](https://jupyterbook.org/)

Y esta adaptación concreta ha sido preparada para la **Facultad de Ciencias de la Universidad de Salamanca (USAL)**.

Es importante entender esto bien: **no partimos de cero**. Partimos de herramientas existentes, probadas y mantenidas, y sobre ellas construimos una plantilla adaptada a uso docente real.

## De qué se parte y qué se obtiene

La idea base del sistema es esta:

| Se parte de... | Y se obtiene... |
|---|---|
| archivos `.md` y `.ipynb` | páginas web del libro |
| imágenes, bibliografía y recursos estáticos | contenido enriquecido |
| configuración del libro (`_config_*.yml`) | navegación, tema, idioma, extensiones |
| índice (`_toc_*.yml`) | estructura visible del libro |

## Ventajas para la docencia

1. **Accesibilidad**: el libro se puede leer como web desde cualquier dispositivo.
2. **Reproducibilidad**: el contenido sale de archivos fuente versionables.
3. **Mantenibilidad**: actualizar una página es mucho más fácil que rehacer apuntes enteros.
4. **Escalabilidad**: puedes empezar con una sola página y crecer poco a poco.
5. **Compatibilidad**: el mismo proyecto puede servir para web y PDF.

## Qué añade esta plantilla respecto a la base original

Sobre la base de TeachBooks / Jupyter Book, en este proyecto hemos añadido cosas muy útiles para profesorado y alumnado:

### 1. Estructura multiidioma

El libro está preparado para trabajar en:

- español
- inglés

con índices y contenido sincronizados.

### 2. Exportación a PDF

Además de la web, esta plantilla prepara una salida PDF pensada para impresión o distribución offline.

### 3. Automatización con scripts sencillos

No hace falta aprender un flujo complejo desde el primer día. El proyecto trae scripts para:

- preparar el entorno
- compilar la web
- abrir vista previa en vivo
- exportar PDF
- convertir PDF a Markdown

### 4. Integración con agentes de IA

La plantilla está preparada para que un agente te ayude a:

- crear contenido
- reorganizar capítulos
- añadir multimedia
- mantener la estructura del libro

## Qué NO es un TeachBook

No es:

- una presentación PowerPoint
- una web hecha con React o frameworks pesados
- un PDF estático disfrazado de web

La idea central es que el contenido sea **editable, estructurado y reutilizable**.

## Idea práctica para empezar

No intentes construir un libro enorme el primer día.

Empieza por algo pequeño:

- una portada
- un capítulo corto
- una imagen
- una ecuación
- una sección con dos o tres páginas

Cuando eso funcione bien, amplías.
