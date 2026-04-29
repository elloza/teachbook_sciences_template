# Technical Diagrams with Kroki for Physics

Kroki is useful for **block diagrams, signal flow, timing diagrams, and conceptual schematics**. For **electrical circuits with standard symbols**, the recommended tool is **CircuitikZ rendered as an image**.

## When to use each tool

- **Use Kroki** for conceptual explanations, functional blocks, timing, instrumentation, and signal flow.
- **Use WaveDrom through Kroki** for digital signals, buses, clocks, and timing protocols.
- **Use CircuitikZ** for resistors, capacitors, sources, switches, and formal electrical schematics.
- **Use SchemDraw** when you want to build simple circuits from Python inside a notebook.

## 1. Mermaid: instrumentation chain


The following diagram visually summarizes this part of the explanation.

**Diagram: Mermaid: instrumentation chain.**

```{kroki}
:type: mermaid
:align: center

flowchart LR
    G[Generator] --> R[RC Circuit]
    R --> O[Oscilloscope]
    R --> M[Multimeter]
    O --> A[Phase analysis]
    M --> B[Amplitude measurement]
```

## 2. GraphViz: signal flow in an experimental setup


The following diagram visually summarizes this part of the explanation.

**Diagram: GraphViz: signal flow in an experimental setup.**

```{kroki}
:type: graphviz
:align: center

digraph G {
    rankdir=LR;
    Generator -> "RC Circuit";
    "RC Circuit" -> Oscilloscope;
    "RC Circuit" -> "Current sensor";
    Oscilloscope -> "Phase calculation";
    "Current sensor" -> "Impedance calculation";
}
```

## 3. CircuitikZ: teaching circuit as an image

The following circuit is not drawn by hand: it comes from a `.tex` file with CircuitikZ code, rendered beforehand as an image so it works the same way in HTML and PDF.


The {numref}`fig-kroki-diagrams-3` visually summarizes this part of the explanation.

```{figure} ../../../_static/generated/rc_circuit_circuitikz.png
:alt: RC circuit generated with CircuitikZ
:width: 70%
:align: center
:name: fig-kroki-diagrams-3

RC circuit generated from CircuitikZ code.
```

```tex
\begin{circuitikz}
\draw
  (0,0) to[V, l=$5\,\mathrm{V}$] (0,3)
  to[R, l=$R_1$] (3,3)
  to[C, l=$20\,\mu\mathrm{F}$] (3,0)
  -- (0,0);
\end{circuitikz}
```

```{admonition} Important
:class: warning
Kroki supports TikZ, but the public Kroki service does not guarantee that the `circuitikz` package is available. For robust teaching circuits, this project renders CircuitikZ locally as an image.
```

## 4. Wavedrom: input and output signals


The following diagram visually summarizes this part of the explanation.

**Diagram: Wavedrom: input and output signals.**

```{kroki}
:type: wavedrom
:align: center

{ signal: [
  { name: "Vin", wave: "p....|...." },
  { name: "Vout", wave: "0.p..|.p..", phase: 0.5 },
  { name: "I", wave: "0..p.|..p.", phase: 0.75 }
]}
```

## 5. Ditaa: quick experimental bench sketch


The following diagram visually summarizes this part of the explanation.

**Diagram: Ditaa: quick experimental bench sketch.**

```{kroki}
:type: ditaa
:align: center

+----------+      +------------+      +-------------+
| Generator |----->| RC Circuit |----->| Oscilloscope |
+----------+      +------------+      +-------------+
```

## Key idea

Kroki, CircuitikZ, and SchemDraw **complement** each other. They do not compete:

- **Kroki** = system-level visual explanation, blocks, flows, and timing diagrams.
- **CircuitikZ** = formal circuit with standard symbols and LaTeX-quality output.
- **SchemDraw** = programmable circuit from Python, ideal for teaching notebooks.
