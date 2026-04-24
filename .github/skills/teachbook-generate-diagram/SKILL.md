---
name: teachbook-generate-diagram
description: >
  Genera diagramas para el libro usando Kroki: Mermaid, PlantUML, GraphViz, Excalidraw, etc.
  Los diagramas se renderizan como imágenes SVG que funcionan tanto en HTML como en PDF.
  Trigger phrases: "diagrama", "diagrama de flujo", "ER", "UML", "mermaid",
  "flowchart", "diagrama de clases", "diagrama entidad relación", "diagrama de secuencia",
  "diagrama de estados", "diagrama de gantt", "plantuml", "graphviz", "excalidraw",
  "kroki", "generar diagrama", "crear diagrama".
---

# Skill: Generar Diagramas con Kroki

## Qué es Kroki

Kroki convierte texto en diagramas. El profesor escribe la sintaxis del diagrama (Mermaid, PlantUML, etc.) y Kroki la convierte en una imagen SVG durante la compilación del libro. La imagen se incrusta directamente, funcionando **tanto en HTML como en PDF**.

## Ventajas

- ✅ Funciona en **HTML y PDF** (se renderiza como imagen SVG)
- ✅ Soporta **20+ tipos** de diagramas (Mermaid, PlantUML, GraphViz, Excalidraw, etc.)
- ✅ No requiere JavaScript ni herramientas externas instaladas
- ✅ No necesita fallbacks manuales

## Requisito

Necesita conexión a internet **durante la compilación** (no al leer el libro). GitHub Actions siempre tiene internet, así que el despliegue funciona siempre.

## Sintaxis MyST

### Mermaid (recomendado — el más sencillo)

````markdown
```{kroki}
:type: mermaid
:align: center

flowchart LR
    A[Inicio] --> B[Proceso]
    B --> C[Fin]
```
````

### Con título (caption)

````markdown
```{kroki-figure}
:type: mermaid
:align: center
:caption: Flujo del método científico

graph TD
    A[Observación] --> B[Hipótesis]
    B --> C[Experimentación]
    C --> D{¿Resultados válidos?}
    D -->|Sí| E[Conclusión]
    D -->|No| B
```
````

### Otros tipos de diagrama soportados

````markdown
```{kroki}
:type: plantuml
:align: center

@startuml
Alice -> Bob: Hello
Bob --> Alice: Hi!
@enduml
```
````

````markdown
```{kroki}
:type: graphviz
:align: center

digraph G {
    A -> B -> C;
    A -> C;
}
```
````

````markdown
```{kroki}
:type: excalidraw
:align: center

{"type":"excalidraw","version":2,"elements":[...]}
```
````

## Plantillas por tipo de diagrama (Mermaid)

### Flowchart (diagrama de flujo)

````markdown
```{kroki}
:type: mermaid
:align: center

graph TD
    A[Observación] --> B[Hipótesis]
    B --> C[Experimentación]
    C --> D{¿Resultados válidos?}
    D -->|Sí| E[Conclusión]
    D -->|No| B
```
````

Direcciones: `graph TD` (arriba→abajo), `graph LR` (izquierda→derecha), `flowchart TD`, `flowchart LR`.

### Diagrama ER (entidad-relación)

````markdown
```{kroki}
:type: mermaid
:align: center

erDiagram
    EXPERIMENTO ||--o{ MEDICION : tiene
    EXPERIMENTO {
        string nombre
        date fecha
        string responsable
    }
    MEDICION {
        float valor
        string unidad
        datetime timestamp
    }
```
````

### Diagrama de clases (UML)

````markdown
```{kroki}
:type: mermaid
:align: center

classDiagram
    class Organismo {
        +String nombre
        +String reino
        +clasificar()
    }
    class Animal {
        +String habitat
        +moverse()
    }
    Organismo <|-- Animal
```
````

### Diagrama de secuencia

````markdown
```{kroki}
:type: mermaid
:align: center

sequenceDiagram
    participant E as Estudiante
    participant L as Laboratorio
    participant P as Profesor
    E->>L: Enviar muestra
    L->>L: Analizar muestra
    L-->>P: Enviar resultados
    P-->>E: Devolver informe
```
````

### Diagrama de estados

````markdown
```{kroki}
:type: mermaid
:align: center

stateDiagram-v2
    [*] --> Liquido
    Liquido --> Gas : Evaporación
    Gas --> Liquido : Condensación
    Liquido --> Solido : Congelación
    Solido --> Liquido : Fusión
```
````

### Diagrama de Gantt

````markdown
```{kroki}
:type: mermaid
:align: center

gantt
    title Cronograma del experimento
    dateFormat  YYYY-MM-DD
    section Preparación
    Diseño experimental   :a1, 2025-01-01, 7d
    Recopilar material    :a2, after a1, 3d
    section Ejecución
    Realizar mediciones   :a3, after a2, 14d
```
````

## Tipos de diagrama soportados por Kroki

| Tipo | `:type:` | Descripción |
|---|---|---|
| Mermaid | `mermaid` | El más versátil. Flowcharts, ER, UML, secuencias, Gantt... |
| PlantUML | `plantuml` | Diagramas UML completos. Sintaxis `@startuml` / `@enduml`. |
| GraphViz | `graphviz` | Diagramas de nodos y aristas. Usa sintaxis DOT. |
| Excalidraw | `excalidraw` | Diagramas dibujados a mano (estilo pizarra). JSON. |
| Bytefield | `bytefield` | Diagramas de campos de bits (electrónica/protocolos). |
| BlockDiag | `blockdiag` | Diagramas de bloques simples. |
| SeqDiaq | `seqdiag` | Diagramas de secuencia (alternativa simple). |
| ActDiag | `actdiag` | Diagramas de actividad. |
| NwDiag | `nwdiag` | Diagramas de red. |
| PacketDiag | `packetdiag` | Diagramas de paquetes de red. |
| RackDiag | `rackdiag` | Diagramas de rack de servidores. |
| Vega / Vega-Lite | `vega` / `vegalite` | Gráficos y visualizaciones de datos. JSON. |
| Ditaa | `ditaa` | Diagramas ASCII convertidos a imágenes. |
| Erd | `erd` | Diagramas entidad-relación (sintaxis propia). |
| Nomnoml | `nomnoml` | Diagramas de clases UML minimalistas. |
| SvgBob | `svgbob` | Diagramas ASCII convertidos a SVG. |
| Umlet | `umlet` | Diagramas UML. |
| WaveDrom | `wavedrom` | Diagramas de formas de onda digitales. |
| Pikchr | `pikchr` | Diagramas técnicos (tipo PIC). |
| Structurizr | `structurizr` | Diagramas C4 (arquitectura software). |

## Reglas

| Regla | Detalle |
|---|---|
| Tipo por defecto | Usar **Mermaid** (`:type: mermaid`) salvo que el usuario pida otro. |
| Simplicidad | Máximo **10-15 nodos**. Si necesitas más, divide en varios diagramas. |
| Etiquetas | Usar **español** para los textos (salvo que el contenido sea en inglés). |
| Caption | Siempre añadir `:caption:` descriptivo usando `{kroki-figure}`. |
| Alineación | Usar `:align: center` por defecto. |
| HTML y PDF | Los diagramas **funcionan en ambos formatos**. No necesita fallbacks. |
| Validación | Verificar la sintaxis antes de insertar. Un error de sintaxis rompe la página. |
| Sin `{mermaid}` | **NO** usar la directiva `{mermaid}` (requiere sphinxcontrib-mermaid, no funciona en PDF). Usar siempre `{kroki}` con `:type: mermaid`. |

## Flujo de trabajo

1. Preguntar qué tipo de diagrama necesita el usuario y qué concepto quiere representar.
2. Elegir el tipo adecuado (Mermaid por defecto, PlantUML para UML complejo, etc.).
3. Generar el código del diagrama usando la plantilla correspondiente.
4. Insertar en el archivo `.md` usando `{kroki}` con `:type: <tipo>`.
5. Si el usuario quiere título/caption, usar `{kroki-figure}` en lugar de `{kroki}`.
