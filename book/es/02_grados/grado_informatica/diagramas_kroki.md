# Diagramas con Kroki para Informática

Kroki permite generar muchos tipos de diagramas útiles en Informática sin depender de JavaScript en el navegador. Todos los ejemplos siguientes funcionan en **HTML y PDF**.

## 1. Mermaid: arquitectura por capas


El diagrama siguiente resume visualmente esta parte de la explicación.

**Diagrama: Mermaid: arquitectura por capas.**

```{kroki}
:type: mermaid
:align: center

flowchart TB
    UI[Frontend] --> API[API REST]
    API --> APP[Lógica de negocio]
    APP --> DB[(Base de datos)]
    APP --> CACHE[(Cache)]
```

## 2. PlantUML: componentes del sistema


El diagrama siguiente resume visualmente esta parte de la explicación.

**Diagrama: PlantUML: componentes del sistema.**

```{kroki}
:type: plantuml
:align: center

@startuml
[Web App] --> [API]
[API] --> [Service Layer]
[Service Layer] --> [PostgreSQL]
[Service Layer] --> [Redis]
@enduml
```

## 3. GraphViz: grafo de dependencias


El diagrama siguiente resume visualmente esta parte de la explicación.

**Diagrama: GraphViz: grafo de dependencias.**

```{kroki}
:type: graphviz
:align: center

digraph G {
    rankdir=LR;
    Controller -> Service;
    Service -> Repository;
    Repository -> Database;
    Service -> Cache;
}
```

## 4. Structurizr: vista C4 simplificada


El diagrama siguiente resume visualmente esta parte de la explicación.

**Diagrama: Structurizr: vista C4 simplificada.**

```{kroki}
:type: structurizr
:align: center

workspace {
  model {
    user = person "Usuario"
    softwareSystem = softwareSystem "Plataforma Docente" {
      web = container "Web"
      api = container "API"
      db = container "Database"
    }
    user -> web "Usa"
    web -> api "Llama"
    api -> db "Lee/escribe"
  }
  views {
    container softwareSystem {
      include *
      autoLayout lr
    }
    styles {
      element "Software System" {
        background #1168BD
        color #FFFFFF
      }
      element "Container" {
        background #438DD5
        color #FFFFFF
      }
      element "Person" {
        background #08427B
        color #FFFFFF
      }
    }
  }
}
```

```{admonition} Nota sobre PDF
:class: tip
En diagramas C4 conviene definir colores explícitos. Algunos temas por defecto pueden producir texto blanco sobre fondo blanco al convertir SVG a PDF.
```

## 5. Wavedrom: protocolo digital


El diagrama siguiente resume visualmente esta parte de la explicación.

**Diagrama: Wavedrom: protocolo digital.**

```{kroki}
:type: wavedrom
:align: center

{ signal: [
  { name: "clk", wave: "p....|...." },
  { name: "req", wave: "0.1..|0..." },
  { name: "ack", wave: "0..1.|0..." },
  { name: "data", wave: "x.=x.|.=x.", data: ["A", "B"] }
]}
```

## Idea clave

En Informática, Kroki es ideal para:

- arquitectura
- UML
- redes de dependencias
- protocolos
- diagramas C4

Si el usuario pide un diagrama rápido y portable, Kroki es una gran opción.
