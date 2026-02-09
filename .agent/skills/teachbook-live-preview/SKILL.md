---
name: teachbook-live-preview
description: Activa una previsualización en vivo del libro que se actualiza automáticamente al guardar cambios.
---

# Skill: Previsualización en Vivo 👁️

Esta skill te permite ver los cambios en tu libro en tiempo real mientras escribes.

## ¿Qué hace?
- Abre una ventana en tu navegador con el libro.
- **Vigila** tus archivos (`.md`, `.ipynb`, `_config.yml`): si guardas un cambio, recompila automáticamente.
- Si cambias la configuración (título, autor), regenera el entorno al vuelo.
- Actualiza la web para que veas el resultado al instante (**Hot Reloading**).

## ¿Cuándo usarla?
- Mientras estás escribiendo contenido y quieres ver cómo queda.
- Para corregir fórmulas matemáticas o ajustar imágenes.

## Cómo pedirla al Agente
> "Quiero ver el libro en vivo."
> "Activa la vista previa."
> "Enséñame cómo queda."

El agente abrirá el navegador. Para detenerlo, solo tienes que cerrar la terminal o pulsar `Ctrl+C`.

**Nota**: No necesitas configurar servidores ni puertos. Todo es automático.

## Acción Técnica
El agente ejecutará:
```bash
python scripts/preview_book.py
```
