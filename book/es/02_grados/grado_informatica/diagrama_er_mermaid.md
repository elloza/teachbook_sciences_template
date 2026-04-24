# Diagrama Entidad-Relación con Mermaid

Los diagramas E-R son fundamentales en el diseño de bases de datos.
Con la directiva `{mermaid}` de MyST puedes incluirlos directamente en tu libro.

## Ejemplo: Base de datos de una universidad

**Código:**

````md
```{mermaid}
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

**Resultado (solo HTML):**

```{mermaid}
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

```{raw} latex
\begin{center}
\textbf{Diagrama Entidad-Relación:} Base de datos de una universidad con las entidades ESTUDIANTE, CURSO, PROFESOR y MATRICULA. Los estudiantes se matriculan en cursos a través de la tabla MATRICULA, los profesores imparten cursos, y los cursos tienen múltiples matriculaciones.
\end{center}
```

## Cómo modificarlo

- **Añadir una entidad**: Copia un bloque como `ENTIDAD { ... }` y define sus atributos.
- **Tipos de relación**: Usa `||--o{` (uno a muchos), `||--||` (uno a uno), `}o--o{` (muchos a muchos).
- **Claves primarias**: Marca los atributos con `PK`.
- **Claves foráneas**: Marca los atributos con `FK`.

## Referencia rápida de cardinalidad

| Notación | Significado |
|----------|-------------|
| `||--||` | Uno a uno |
| `||--o{` | Uno a muchos |
| `}o--o{` | Muchos a muchos |
