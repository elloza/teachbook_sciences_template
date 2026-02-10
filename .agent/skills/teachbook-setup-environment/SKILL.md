---
name: teachbook-setup-environment
description: Prepara el entorno de desarrollo, instalando dependencias y configurando el entorno virtual.
---

# Skill: Preparar Entorno 🔧

Esta skill configura todo lo necesario para que puedas trabajar en tu ordenador.

## ¿Qué hace?
- Crea un entorno virtual seguro (para no afectar a otros programas).
- Instala las herramientas necesarias (TeachBooks, Python, etc.).

## ¿Cuándo usarla?
- La primera vez que abras el proyecto.
- Si ves que algo "no funciona" o faltan librerías.
- Si cambias de ordenador.

## Cómo pedirla al Agente
Simplemente díselo en lenguaje natural:

> "Prepara el entorno de trabajo, por favor."
> "No me compila, ¿puedes revisar la instalación?"
> "Instala lo que falte."

## Acción Técnica
El agente ejecutará:
- **Producción (Solo lectura/Web):**
  ```bash
  python scripts/setup_env.py
  ```
- **Desarrollo (Con herramientas de prueba):**
  ```bash
  python scripts/setup_env.py --dev
  ```
