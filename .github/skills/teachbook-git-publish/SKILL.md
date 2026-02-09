---
name: teachbook-git-publish
description: Gestiona el control de versiones, guardando cambios y publicando en GitHub Pages.
---

# Skill: Guardar y Publicar 🚀

Esta skill se encarga de guardar tu trabajo y subirlo a Internet.

## ¿Qué hace?
- **Guarda** todos tus cambios (Commit).
- **Sube** los cambios a GitHub (Push).
- **Publica** automáticamente la web (gracias a GitHub Pages).

## ¿Cuándo usarla?
- Al terminar una sesión de trabajo.
- Cuando quieras que tus alumnos vean los cambios.

## Cómo pedirla al Agente
> "Guarda mis cambios."
> "Sube todo a la web."
> "Publica la nueva versión."

**Nota**: No hace falta que sepas usar "Git". El agente lo hará por ti de forma segura.

## Acción Técnica
El agente ejecutará:
```bash
python scripts/git_helper.py
```
