# Diagrama de Clases UML con Kroki (Mermaid)

Los diagramas de clases son esenciales para modelar sistemas orientados a objetos.
Con Kroki y `:type: mermaid` puedes representar clases, atributos, métodos y herencia en HTML y PDF.

## Ejemplo: Jerarquía de Figuras Geométricas

**Código:**

````md
```{kroki}
:type: mermaid
:align: center

classDiagram
    class Figura {
        <<abstract>>
        +String color
        +area() float
        +perimetro() float
    }

    class Circulo {
        +float radio
        +area() float
        +perimetro() float
    }

    class Rectangulo {
        +float ancho
        +float alto
        +area() float
        +perimetro() float
    }

    class Triangulo {
        +float base
        +float altura
        +area() float
        +perimetro() float
    }

    Figura <|-- Circulo
    Figura <|-- Rectangulo
    Figura <|-- Triangulo
```
````

**Resultado:**


El diagrama siguiente resume visualmente esta parte de la explicación.

**Diagrama: Ejemplo: Jerarquía de Figuras Geométricas.**

```{kroki}
:type: mermaid
:align: center

classDiagram
    class Figura {
        <<abstract>>
        +String color
        +area() float
        +perimetro() float
    }

    class Circulo {
        +float radio
        +area() float
        +perimetro() float
    }

    class Rectangulo {
        +float ancho
        +float alto
        +area() float
        +perimetro() float
    }

    class Triangulo {
        +float base
        +float altura
        +area() float
        +perimetro() float
    }

    Figura <|-- Circulo
    Figura <|-- Rectangulo
    Figura <|-- Triangulo
```

## Notación de clases

- **Atributos**: Se listan en la primera sección. Prefija con `+` (público), `-` (privado), `#` (protegido).
- **Métodos**: Se listan en la segunda sección, con el tipo de retorno.
- **Clase abstracta**: Indicada con `<<abstract>>`.

## Tipos de relaciones


La tabla siguiente resume los elementos principales de esta sección.

**Tabla. Tipos de relaciones.**

| Notación | Significado |
|----------|-------------|
| `<\|--` | Herencia (es un) |
| `*--` | Composición |
| `o--` | Agregación |
| `-->` | Asociación |
| `..>` | Dependencia |
