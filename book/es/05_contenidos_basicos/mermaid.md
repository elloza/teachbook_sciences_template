(mermaid)=
# Diagramas Mermaid

**Mermaid** permite crear diagramas directamente en Markdown sin herramientas externas. Los diagramas se renderizan automáticamente en HTML.

```{warning}
Mermaid **solo funciona en HTML**. En PDF no se renderiza. Siempre debes añadir una descripción textual como alternativa.
```

## Diagrama de flujo (`flowchart`)

````md
```{mermaid}
flowchart LR
    A[Muestra] --> B[Preparación]
    B --> C[Medición]
    C --> D[Análisis]
    D --> E[Resultados]
```
````

Resultado (HTML):

```{mermaid}
flowchart LR
    A[Muestra] --> B[Preparación]
    B --> C[Medición]
    C --> D[Análisis]
    D --> E[Resultados]
```

Descripción: El flujo va de izquierda a derecha: Muestra → Preparación → Medición → Análisis → Resultados.

## Diagrama de secuencia (`sequenceDiagram`)

````md
```{mermaid}
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

Resultado (HTML):

```{mermaid}
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
```{mermaid}
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

Resultado (HTML):

```{mermaid}
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
```{mermaid}
erDiagram
    ESTUDIANTE ||--o{ INSCRIPCION : realiza
    INSCRIPCION }o--|| ASIGNATURA : corresponde
    ASIGNATURA ||--o{ PRACTICA : incluye
```
````

Resultado (HTML):

```{mermaid}
erDiagram
    ESTUDIANTE ||--o{ INSCRIPCION : realiza
    INSCRIPCION }o--|| ASIGNATURA : corresponde
    ASIGNATURA ||--o{ PRACTICA : incluye
```

## Diagrama de estados (`stateDiagram-v2`)

````md
```{mermaid}
stateDiagram-v2
    [*] --> Pendiente
    Pendiente --> EnProgreso : iniciar
    EnProgreso --> Completado : finalizar
    EnProgreso --> Error : fallo
    Error --> Pendiente : reintentar
    Completado --> [*]
```
````

Resultado (HTML):

```{mermaid}
stateDiagram-v2
    [*] --> Pendiente
    Pendiente --> EnProgreso : iniciar
    EnProgreso --> Completado : finalizar
    EnProgreso --> Error : fallo
    Error --> Pendiente : reintentar
    Completado --> [*]
```

## Direcciones del diagrama de flujo

| Código | Dirección |
|--------|-----------|
| `flowchart LR` | Izquierda a derecha |
| `flowchart RL` | Derecha a izquierda |
| `flowchart TB` | Arriba a abajo |
| `flowchart BT` | Abajo a arriba |

```{tip}
Si tu diagrama es clave para entender el contenido, considera usar una imagen generada externamente (PNG/SVG) con la directiva `{figure}` en lugar de Mermaid. Así funcionará también en PDF.
```
