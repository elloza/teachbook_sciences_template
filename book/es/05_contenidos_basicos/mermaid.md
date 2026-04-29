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


El diagrama siguiente resume visualmente esta parte de la explicación.

**Diagrama: Diagrama de flujo (`flowchart`).**

```{kroki}
:type: mermaid
:align: center

flowchart LR
    A[Muestra] --> B[Preparación]
    B --> C[Medición]
    C --> D[Análisis]
    D --> E[Resultados]
```

Descripción: El flujo va de izquierda a derecha: Muestra → Preparación → Medición → Análisis → Resultados.

## Diagrama de secuencia (`sequenceDiagram`)

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


El diagrama siguiente resume visualmente esta parte de la explicación.

**Diagrama: Diagrama de secuencia (`sequenceDiagram`).**

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

Descripción: El estudiante entrega un informe al profesor, recibe correcciones, y luego reserva un equipo en el laboratorio.

## Diagrama de clases (`classDiagram`)

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


El diagrama siguiente resume visualmente esta parte de la explicación.

**Diagrama: Diagrama de clases (`classDiagram`).**

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

## Diagrama entidad-relación (`erDiagram`)

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


El diagrama siguiente resume visualmente esta parte de la explicación.

**Diagrama: Diagrama entidad-relación (`erDiagram`).**

```{kroki}
:type: mermaid
:align: center

erDiagram
    ESTUDIANTE ||--o{ INSCRIPCION : realiza
    INSCRIPCION }o--|| ASIGNATURA : corresponde
    ASIGNATURA ||--o{ PRACTICA : incluye
```

## Diagrama de estados (`stateDiagram-v2`)

````md
```{kroki}
:type: mermaid
:align: center

stateDiagram-v2
    [*] --> Pendiente
    Pendiente --> EnProgreso : iniciar
    EnProgreso --> Completado : finalizar
    EnProgreso --> Error : fallo
    Error --> Pendiente : reintentar
    Completado --> [*]
```
````

Resultado:


El diagrama siguiente resume visualmente esta parte de la explicación.

**Diagrama: Diagrama de estados (`stateDiagram-v2`).**

```{kroki}
:type: mermaid
:align: center

stateDiagram-v2
    [*] --> Pendiente
    Pendiente --> EnProgreso : iniciar
    EnProgreso --> Completado : finalizar
    EnProgreso --> Error : fallo
    Error --> Pendiente : reintentar
    Completado --> [*]
```

## Direcciones del diagrama de flujo


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
