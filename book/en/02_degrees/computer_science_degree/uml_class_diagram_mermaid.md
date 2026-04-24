# UML Class Diagram with Mermaid

Class diagrams are essential for modeling object-oriented systems.
Mermaid allows you to represent classes with their attributes, methods, and inheritance relationships.

## Example: Geometric Shape Hierarchy

**Code:**

````md
```{mermaid}
classDiagram
    class Shape {
        <<abstract>>
        +String color
        +area() float
        +perimeter() float
    }

    class Circle {
        +float radius
        +area() float
        +perimeter() float
    }

    class Rectangle {
        +float width
        +float height
        +area() float
        +perimeter() float
    }

    class Triangle {
        +float base
        +float height
        +area() float
        +perimeter() float
    }

    Shape <|-- Circle
    Shape <|-- Rectangle
    Shape <|-- Triangle
```
````

**Result (HTML only):**

```{mermaid}
classDiagram
    class Shape {
        <<abstract>>
        +String color
        +area() float
        +perimeter() float
    }

    class Circle {
        +float radius
        +area() float
        +perimeter() float
    }

    class Rectangle {
        +float width
        +float height
        +area() float
        +perimeter() float
    }

    class Triangle {
        +float base
        +float height
        +area() float
        +perimeter() float
    }

    Shape <|-- Circle
    Shape <|-- Rectangle
    Shape <|-- Triangle
```

```{raw} latex
\begin{center}
\textbf{UML Class Diagram:} Abstract Shape class with color attribute and area(), perimeter() methods. Circle, Rectangle, and Triangle inherit from Shape and implement these methods with their specific attributes.
\end{center}
```

## Class notation

- **Attributes**: Listed in the first section. Prefix with `+` (public), `-` (private), `#` (protected).
- **Methods**: Listed in the second section, with return type.
- **Abstract class**: Indicated with `<<abstract>>`.

## Relationship types

| Notation | Meaning |
|----------|---------|
| `<\|--` | Inheritance (is a) |
| `*--` | Composition |
| `o--` | Aggregation |
| `-->` | Association |
| `..>` | Dependency |
