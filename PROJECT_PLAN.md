# TeachBook Sciences Template — Project Plan (v1)

Este documento define el **plan completo de implementación**
del repositorio `teachbook_sciences_template`.

El objetivo es crear una **plantilla docente reutilizable**
para libros electrónicos interactivos basados en TeachBooks,
orientada a asignaturas de la **Facultad de Ciencias (USAL)**.

Este documento es la **fuente única de verdad** para el agente.
No inventes funcionalidades fuera de este plan.

---

## 1. OBJETIVO GENERAL

Crear un **template estable, simple y pedagógico** que permita
a profesorado universitario **no informático**:

- crear un libro docente electrónico
- combinar texto, código y visualizaciones
- publicar el libro como web
- reutilizar ejemplos por grado y asignatura
- usar asistentes de IA como apoyo continuo

---

## 2. PRINCIPIOS DE DISEÑO (OBLIGATORIOS)

- Priorizar **simplicidad** sobre potencia
- Todo debe funcionar con **VS Code**
- Evitar configuraciones complejas
- No asumir conocimientos de Git
- No activar funcionalidades avanzadas por defecto
- El template debe compilar sin tocar nada
- El contenido debe ser **didáctico y editable**

---

## 3. STACK TECNOLÓGICO (FIJO)

No introducir tecnologías adicionales.

- TeachBooks / Jupyter Book
- MyST Markdown
- Jupyter Notebooks
- Python básico
- GitHub Pages
- VS Code
- Asistentes de IA (Copilot / Antigravity)

---

## 4. ESTRUCTURA FINAL DEL REPOSITORIO

Implementar exactamente esta estructura:

teachbook_sciences_template/
├── book/
│ ├── es/
│ │ ├── intro.md
│ │ ├── 01_tutorial/
│ │ │ ├── 01_que_es_un_teachbook.md
│ │ │ ├── 02_flujo_trabajo.md
│ │ │ ├── 03_edicion_con_ia.md
│ │ │ └── 04_publicacion.md
│ │ ├── 02_grados/
│ │ │ ├── grado_fisica/
│ │ │ │ ├── intro.md
│ │ │ │ └── ejemplo_fisica.ipynb
│ │ │ ├── grado_matematicas/
│ │ │ │ ├── intro.md
│ │ │ │ └── ejemplo_matematicas.ipynb
│ │ │ └── grado_estadistica/
│ │ │ ├── intro.md
│ │ │ └── ejemplo_estadistica.ipynb
│ │ ├── 90_acerca_de.md
│ │ ├── 91_licencias.md
│ │ └── 92_como_citar.md
│ ├── _toc.yml
│ └── _config.yml
├── Agent.md
├── PROJECT_PLAN.md
├── README.md
├── requirements.txt
└── LICENSE


---

## 5. CONTENIDOS A IMPLEMENTAR

### 5.1 Introducción (`intro.md`)
- Qué es un TeachBook
- Contexto USAL
- Enlace a “Cómo citar”
- Badge de Zotero (placeholder)

---

### 5.2 Tutoriales (`01_tutorial/`)
Contenido guiado, paso a paso:

1. Qué es un TeachBook
2. Flujo de trabajo completo
3. Edición con IA desde VS Code
4. Publicación web

Lenguaje:
- claro
- sin jerga técnica
- orientado a docentes

---

### 5.3 Ejemplos por grado (`02_grados/`)

Organización obligatoria:
Grado → Asignatura → Ejemplo


Cada ejemplo debe:
- ser sencillo
- ser realista
- poder borrarse o copiarse
- servir como referencia

---

### 5.4 Secciones finales

#### Acerca de
- autores
- institución
- año
- contexto del curso

#### Licencias
- CC-BY para contenidos
- MIT para código
- atribuciones a TeachBooks / Jupyter Book

#### Cómo citar
- referencia textual
- BibTeX
- mención a DOI futuro (Zenodo)
- referencia a Zotero

---

## 6. AGENTE Y ASISTENCIA CON IA

El archivo `Agent.md` define el comportamiento del asistente.

El agente debe:
- ayudar a crear contenidos
- explicar errores de compilación
- proponer ejemplos didácticos
- priorizar claridad y resultados visibles

---

## 7. FUNCIONALIDADES AVANZADAS (NO IMPLEMENTAR AÚN)

Estas funcionalidades **NO deben activarse**, solo prepararse:

- multidioma (estructura `book/en/`)
- comentarios (giscus / utterances)
- exportación a PDF (ebook)
- DOI automático

Solo documentar puntos de extensión si procede.

---

## 8. CRITERIOS DE FINALIZACIÓN (DEFINITION OF DONE)

El proyecto se considera correcto cuando:

- El libro compila sin errores
- Se puede publicar como web
- La estructura es clara
- El contenido es editable
- El template puede clonarse y usarse
- Un docente no informático puede empezar

---

## 9. ORDEN DE IMPLEMENTACIÓN (OBLIGATORIO)

El agente debe implementar en este orden:

1. Estructura de carpetas
2. `_toc.yml` funcional
3. `_config.yml` mínimo
4. Contenidos base (vacíos o mínimos)
5. Ejemplos sencillos
6. README pedagógico
7. Verificación de compilación

No saltarse pasos.

---

## 10. NORMA FINAL

No optimizar prematuramente.
No añadir funcionalidades no solicitadas.
No romper la simplicidad del template.

Este proyecto es una **herramienta docente**, no un framework.