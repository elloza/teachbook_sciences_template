# Diagrama de Clases UML con Mermaid

Los diagramas de clases son esenciales para modelar sistemas orientados a objetos.
Mermaid permite representar clases con sus atributos, métodos y relaciones de herencia.

## Ejemplo: Jerarquía de Figuras Geométricas

**Código:**

````md
```{mermaid}
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

**Resultado (solo HTML):**

```{mermaid}
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

```{raw} latex
\begin{center}
\textbf{Diagrama de Clases UML:} Jerarquía de figuras geométricas. La clase abstracta \texttt{Figura} define los métodos comunes \texttt{area()} y \texttt{perimetro()}. Las clases \texttt{Circulo}, \texttt{Rectangulo} y \texttt{Triangulo} heredan de \texttt{Figura} e implementan estos métodos según sus dimensiones específicas.
\end{center}
```

## Notación de clases

- **Atributos**: Se listan en la primera sección. Prefija con `+` (público), `-` (privado), `#` (protegido).
- **Métodos**: Se listan en la segunda sección, con el tipo de retorno.
- **Clase abstracta**: Indicada con `<<abstract>>`.

## Tipos de relaciones

| Notación | Significado |
|----------|-------------|
| `<\|--` | Herencia (es un) |
| `*--` | Composición |
| `o--` | Agregación |
| `-->` | Asociación |
| `..>` | Dependencia |
