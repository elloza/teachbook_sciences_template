# The Rock Cycle with Mermaid

The rock cycle describes the transformations between the three main rock types.
With Mermaid, we can represent this cycle as a flowchart.

## The cycle

**Code:**

````md
```{mermaid}
flowchart LR
    Magma["Magma"]
    Igneous["Igneous Rock"]
    Sedimentary["Sedimentary Rock"]
    Metamorphic["Metamorphic Rock"]

    Magma -->|"Cooling and solidification"| Igneous
    Igneous -->|"Weathering and erosion"| Sedimentary
    Sedimentary -->|"Heat and pressure"| Metamorphic
    Metamorphic -->|"Melting"| Magma
    Igneous -->|"Heat and pressure"| Metamorphic
    Metamorphic -->|"Weathering and erosion"| Sedimentary
    Sedimentary -->|"Melting"| Magma
```
````

**Result (HTML only):**

```{mermaid}
flowchart LR
    Magma["Magma"]
    Igneous["Igneous Rock"]
    Sedimentary["Sedimentary Rock"]
    Metamorphic["Metamorphic Rock"]

    Magma -->|"Cooling and solidification"| Igneous
    Igneous -->|"Weathering and erosion"| Sedimentary
    Sedimentary -->|"Heat and pressure"| Metamorphic
    Metamorphic -->|"Melting"| Magma
    Igneous -->|"Heat and pressure"| Metamorphic
    Metamorphic -->|"Weathering and erosion"| Sedimentary
    Sedimentary -->|"Melting"| Magma
```

```{raw} latex
\begin{center}
\textbf{Flowchart:} The rock cycle showing transformations between Magma, Igneous Rock, Sedimentary Rock, and Metamorphic Rock through processes like cooling/solidification, weathering/erosion, heat/pressure, and melting. Any rock type can transform into any other.
\end{center}
```

## Transition explanation

| Transition | Geological process |
|------------|--------------------|
| Magma → Igneous | Cooling and solidification at the surface or underground |
| Igneous → Sedimentary | Weathering, erosion, transport, and sedimentation |
| Sedimentary → Metamorphic | Heat and pressure (metamorphism) without melting |
| Metamorphic → Magma | Complete melting at extreme temperatures |
| Igneous → Metamorphic | Direct metamorphism through heat and pressure |
| Metamorphic → Sedimentary | Uplift, weathering, and erosion |

## Key point

Any rock type can transform into any other. It is not a linear cycle, but a **transformation network** operating on geological timescales (millions of years).
