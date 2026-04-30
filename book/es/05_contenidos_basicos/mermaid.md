(mermaid)=
# Diagramas con Kroki (Mermaid)

**Kroki** permite convertir texto en diagramas SVG durante la compilación del libro. Si usas `:type: mermaid`, puedes escribir sintaxis Mermaid y obtener un diagrama que funciona tanto en **HTML** como en **PDF**.

## Diagrama de flujo (`flowchart`)

````md
```{kroki}
:type: mermaid
:align: center

flowchart LR
    A[Muestra] --> B[Preparación]
    B --> C[Medición]
    C --> D[Análisis]
    D --> E[Resultados]
```
````

Resultado:


Como muestra la {numref}`fig-diagrama-05-contenidos-basicos-mermaid-01`, el diagrama queda versionado como imagen estática.

```{figure} ../../_static/generated/diagrams/es/05_contenidos_basicos_mermaid_01.svg
:name: fig-diagrama-05-contenidos-basicos-mermaid-01
:alt: Diagrama: Diagrama de flujo (`flowchart`)
:width: 90%
:align: center

Diagrama: Diagrama de flujo (`flowchart`).
```

````md
```{kroki}
:type: mermaid
:align: center

sequenceDiagram
    participant E as Estudiante
    participant P as Profesor
    participant L as Laboratorio
    E->>P: Entrega informe
    P->>E: Correcciones
    E->>L: Reserva equipo
    L->>E: Confirmación
```
````

Resultado:


Como muestra la {numref}`fig-diagrama-05-contenidos-basicos-mermaid-02`, el diagrama queda versionado como imagen estática.

```{figure} ../../_static/generated/diagrams/es/05_contenidos_basicos_mermaid_02.svg
:name: fig-diagrama-05-contenidos-basicos-mermaid-02
:alt: Diagrama: Diagrama de secuencia (`sequenceDiagram`)
:width: 90%
:align: center

Diagrama: Diagrama de secuencia (`sequenceDiagram`).
```

````md
```{kroki}
:type: mermaid
:align: center

classDiagram
    class Experimento {
        +string nombre
        +date fecha
        +ejecutar()
        +analizar()
    }
    class Muestra {
        +string tipo
        +float masa
        +preparar()
    }
    Experimento --> Muestra : usa
```
````

Resultado:


Como muestra la {numref}`fig-diagrama-05-contenidos-basicos-mermaid-03`, el diagrama queda versionado como imagen estática.

```{figure} ../../_static/generated/diagrams/es/05_contenidos_basicos_mermaid_03.svg
:name: fig-diagrama-05-contenidos-basicos-mermaid-03
:alt: Diagrama: Diagrama de clases (`classDiagram`)
:width: 90%
:align: center

Diagrama: Diagrama de clases (`classDiagram`).
```

````md
```{kroki}
:type: mermaid
:align: center

erDiagram
    ESTUDIANTE ||--o{ INSCRIPCION : realiza
    INSCRIPCION }o--|| ASIGNATURA : corresponde
    ASIGNATURA ||--o{ PRACTICA : incluye
```
````

Resultado:


Como muestra la {numref}`fig-diagrama-05-contenidos-basicos-mermaid-04`, el diagrama queda versionado como imagen estática.

```{figure} ../../_static/generated/diagrams/es/05_contenidos_basicos_mermaid_04.svg
:name: fig-diagrama-05-contenidos-basicos-mermaid-04
:alt: Diagrama: Diagrama entidad-relación (`erDiagram`)
:width: 90%
:align: center

Diagrama: Diagrama entidad-relación (`erDiagram`).
```

````md
```{kroki}
:type: mermaid
:align: center

stateDiagram
    [*] --> Pendiente
    Pendiente --> EnProgreso : iniciar
    EnProgreso --> Completado : finalizar
    EnProgreso --> Error : fallo
    Error --> Pendiente : reintentar
    Completado --> [*]
```
````

Resultado:


Como muestra la {numref}`fig-diagrama-05-contenidos-basicos-mermaid-05`, el diagrama queda versionado como imagen estática.

```{figure} ../../_static/generated/diagrams/es/05_contenidos_basicos_mermaid_05.svg
:name: fig-diagrama-05-contenidos-basicos-mermaid-05
:alt: Diagrama: Diagrama de estados (`stateDiagram-v2`)
:width: 90%
:align: center

Diagrama: Diagrama de estados (`stateDiagram-v2`).
```
La tabla siguiente resume los elementos principales de esta sección.

**Tabla. Direcciones del diagrama de flujo.**

| Código | Dirección |
|--------|-----------|
| `flowchart LR` | Izquierda a derecha |
| `flowchart RL` | Derecha a izquierda |
| `flowchart TB` | Arriba a abajo |
| `flowchart BT` | Abajo a arriba |

```{tip}
Usa siempre `{kroki}` con `:type: mermaid` en lugar de `{mermaid}`. Así el diagrama funcionará en HTML y PDF sin fallbacks manuales.
```
