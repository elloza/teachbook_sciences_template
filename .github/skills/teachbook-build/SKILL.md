---
name: teachbook-build
description: Compila el libro TeachBook generando una versión web HTML local.
---

# Skill: Compilar Libro 📚

Esta skill convierte tus archivos de texto y código en una página web interactiva.

## ¿Qué hace?
- Lee todos los archivos de `book/`.
- Ejecuta los notebooks de código.
- Genera una web estática en la carpeta `book/_build/html/`.

## ¿Cuándo usarla?
- Cuando hayas terminado de escribir una sección.
- Para verificar que todo se ve bien antes de publicar.
- Si quieres ver cómo quedan las fórmulas o gráficos.

## Cómo pedirla al Agente
> "Compila el libro."
> "Quiero ver cómo queda la web."
> "Genera la versión HTML."

El agente te avisará si hay algún error en tu contenido.

## Acción Técnica
El agente ejecutará:
```bash
python scripts/build_book.py
```
