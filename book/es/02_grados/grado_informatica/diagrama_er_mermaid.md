# Diagrama Entidad-Relación con Kroki (Mermaid)

Los diagramas E-R son fundamentales en el diseño de bases de datos.
Con Kroki y `:type: mermaid` puedes incluirlos directamente en tu libro y hacer que funcionen tanto en HTML como en PDF.

## Ejemplo: Base de datos de una universidad

**Código:**

````md
```{kroki}
:type: mermaid
:align: center

erDiagram
    ESTUDIANTE {
        int id PK
        string nombre
        string email
    }
    CURSO {
        int id PK
        string nombre
        int creditos
    }
    PROFESOR {
        int id PK
        string nombre
        string departamento
    }
    MATRICULA {
        int id PK
        float nota
        string convocatoria
    }

    ESTUDIANTE ||--o{ MATRICULA : "se matricula"
    CURSO ||--o{ MATRICULA : "tiene"
    PROFESOR ||--o{ CURSO : "imparte"
```
````

**Resultado:**


El diagrama siguiente resume visualmente esta parte de la explicación.

**Diagrama: Ejemplo: Base de datos de una universidad.**

```{kroki}
:type: mermaid
:align: center

erDiagram
    ESTUDIANTE {
        int id PK
        string nombre
        string email
    }
    CURSO {
        int id PK
        string nombre
        int creditos
    }
    PROFESOR {
        int id PK
        string nombre
        string departamento
    }
    MATRICULA {
        int id PK
        float nota
        string convocatoria
    }

    ESTUDIANTE ||--o{ MATRICULA : "se matricula"
    CURSO ||--o{ MATRICULA : "tiene"
    PROFESOR ||--o{ CURSO : "imparte"
```

## Cómo modificarlo

- **Añadir una entidad**: Copia un bloque como `ENTIDAD { ... }` y define sus atributos.
- **Tipos de relación**: Usa `||--o{` (uno a muchos), `||--||` (uno a uno), `}o--o{` (muchos a muchos).
- **Claves primarias**: Marca los atributos con `PK`.
- **Claves foráneas**: Marca los atributos con `FK`.

## Referencia rápida de cardinalidad


La tabla siguiente resume los elementos principales de esta sección.

**Tabla. Referencia rápida de cardinalidad.**

| Notación | Significado |
|----------|-------------|
| `||--||` | Uno a uno |
| `||--o{` | Uno a muchos |
| `}o--o{` | Muchos a muchos |
