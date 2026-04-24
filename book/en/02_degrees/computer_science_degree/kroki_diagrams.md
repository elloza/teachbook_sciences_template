# Diagrams with Kroki for Computer Science

Kroki lets you generate many useful diagram types in Computer Science without depending on browser-side JavaScript. All the following examples work in **HTML and PDF**.

## 1. Mermaid: layered architecture

```{kroki}
:type: mermaid
:align: center

flowchart TB
    UI[Frontend] --> API[REST API]
    API --> APP[Business logic]
    APP --> DB[(Database)]
    APP --> CACHE[(Cache)]
```

## 2. PlantUML: system components

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

## 3. GraphViz: dependency graph

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

## 4. Structurizr: simplified C4 view

```{kroki}
:type: structurizr
:align: center

workspace {
  model {
    user = person "User"
    softwareSystem = softwareSystem "Teaching Platform" {
      web = container "Web"
      api = container "API"
      db = container "Database"
    }
    user -> web "Uses"
    web -> api "Calls"
    api -> db "Reads/writes"
  }
  views {
    container softwareSystem {
      include *
      autoLayout lr
    }
    theme default
  }
}
```

## 5. Wavedrom: digital protocol timing

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

## Key idea

In Computer Science, Kroki is ideal for:

- architecture
- UML
- dependency graphs
- protocols
- C4 diagrams

If the user asks for a fast and portable diagram, Kroki is a great option.
