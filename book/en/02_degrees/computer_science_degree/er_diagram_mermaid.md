# Entity-Relationship Diagram with Mermaid

E-R diagrams are fundamental in database design.
With the MyST `{mermaid}` directive, you can include them directly in your book.

## Example: University database

**Code:**

````md
```{mermaid}
erDiagram
    STUDENT {
        int id PK
        string name
        string email
    }
    COURSE {
        int id PK
        string name
        int credits
    }
    PROFESSOR {
        int id PK
        string name
        string department
    }
    ENROLLMENT {
        int id PK
        float grade
        string term
    }

    STUDENT ||--o{ ENROLLMENT : "enrolls in"
    COURSE ||--o{ ENROLLMENT : "has"
    PROFESSOR ||--o{ COURSE : "teaches"
```
````

**Result (HTML only):**

```{mermaid}
erDiagram
    STUDENT {
        int id PK
        string name
        string email
    }
    COURSE {
        int id PK
        string name
        int credits
    }
    PROFESSOR {
        int id PK
        string name
        string department
    }
    ENROLLMENT {
        int id PK
        float grade
        string term
    }

    STUDENT ||--o{ ENROLLMENT : "enrolls in"
    COURSE ||--o{ ENROLLMENT : "has"
    PROFESSOR ||--o{ COURSE : "teaches"
```

```{raw} latex
\begin{center}
\textbf{E-R Diagram:} University database with STUDENT, COURSE, PROFESSOR, and ENROLLMENT entities. Relationships: STUDENT enrolls in many ENROLLMENTS, COURSE has many ENROLLMENTS, PROFESSOR teaches many COURSES.
\end{center}
```

## How to modify it

- **Add an entity**: Copy a block like `ENTITY { ... }` and define its attributes.
- **Relationship types**: Use `||--o{` (one-to-many), `||--||` (one-to-one), `}o--o{` (many-to-many).
- **Primary keys**: Mark attributes with `PK`.
- **Foreign keys**: Mark attributes with `FK`.

## Cardinality reference

| Notation | Meaning |
|----------|---------|
| `||--||` | One to one |
| `||--o{` | One to many |
| `}o--o{` | Many to many |
