# UML Class Diagram with Kroki (Mermaid)

Class diagrams are essential for modeling object-oriented systems.
With Kroki and `:type: mermaid`, you can represent classes, attributes, methods, and inheritance in both HTML and PDF.

## Example: Geometric Shape Hierarchy

**Code:**

````md
```{kroki}
:type: mermaid
:align: center

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

**Result:**


The following diagram visually summarizes this part of the explanation.

**Diagram: Example: Geometric Shape Hierarchy.**

```{kroki}
:type: mermaid
:align: center

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

## Class notation

- **Attributes**: Listed in the first section. Prefix with `+` (public), `-` (private), `#` (protected).
- **Methods**: Listed in the second section, with return type.
- **Abstract class**: Indicated with `<<abstract>>`.

## Relationship types


The following table summarizes the main elements of this section.

**Table. Relationship types.**

| Notation | Meaning |
|----------|---------|
| `<\|--` | Inheritance (is a) |
| `*--` | Composition |
| `o--` | Aggregation |
| `-->` | Association |
| `..>` | Dependency |
