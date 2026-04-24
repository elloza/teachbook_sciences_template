# Ciclo de las Rocas con Mermaid

El ciclo de las rocas describe las transformaciones entre los tres tipos principales de rocas.
Con Mermaid podemos representar este ciclo como un diagrama de flujo.

## El ciclo

**Código:**

````md
```{mermaid}
flowchart LR
    Magma["Magma"]
    Ignea["Roca Ígnea"]
    Sedimentaria["Roca Sedimentaria"]
    Metamorfica["Roca Metamórfica"]

    Magma -->|"Enfriamiento y solidificación"| Ignea
    Ignea -->|"Meteorización y erosión"| Sedimentaria
    Sedimentaria -->|"Calor y presión"| Metamorfica
    Metamorfica -->|"Fusión"| Magma
    Ignea -->|"Calor y presión"| Metamorfica
    Metamorfica -->|"Meteorización y erosión"| Sedimentaria
    Sedimentaria -->|"Fusión"| Magma
```
````

**Resultado (solo HTML):**

```{mermaid}
flowchart LR
    Magma["Magma"]
    Ignea["Roca Ígnea"]
    Sedimentaria["Roca Sedimentaria"]
    Metamorfica["Roca Metamórfica"]

    Magma -->|"Enfriamiento y solidificación"| Ignea
    Ignea -->|"Meteorización y erosión"| Sedimentaria
    Sedimentaria -->|"Calor y presión"| Metamorfica
    Metamorfica -->|"Fusión"| Magma
    Ignea -->|"Calor y presión"| Metamorfica
    Metamorfica -->|"Meteorización y erosión"| Sedimentaria
    Sedimentaria -->|"Fusión"| Magma
```

```{raw} latex
\begin{center}
\textbf{Ciclo de las Rocas:} Red de transformaciones entre los tres tipos de rocas. El magma se enfría formando roca ígnea, que se meteoriza en sedimentaria, y esta se transforma en metamórfica por calor y presión. La roca metamórfica puede fundirse de nuevo en magma, completando el ciclo. Cualquier tipo de roca puede transformarse en cualquier otro.
\end{center}
```

## Explicación de las transiciones

| Transición | Proceso geológico |
|------------|-------------------|
| Magma → Roca Ígnea | Enfriamiento y solidificación del magma en superficie o en profundidad |
| Roca Ígnea → Sedimentaria | Meteorización, erosión, transporte y sedimentación |
| Sedimentaria → Metamórfica | Calor y presión (metamorfismo) sin llegar a fundir |
| Metamórfica → Magma | Fusión completa por temperaturas extremas |
| Ígnea → Metamórfica | Metamorfismo directo por calor y presión |
| Metamórfica → Sedimentaria | Exhumación, meteorización y erosión |

## Punto clave

Cualquier tipo de roca puede transformarse en cualquier otro. No es un ciclo lineal, sino una **red de transformaciones** que opera a escalas de tiempo geológicas (millones de años).
