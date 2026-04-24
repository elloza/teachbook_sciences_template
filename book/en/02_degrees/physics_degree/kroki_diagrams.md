# Technical Diagrams with Kroki for Physics

Kroki is useful for **block diagrams, signal flow, timing diagrams, and conceptual schematics**. For **precise electrical circuits**, the recommended tool is still **SchemDraw**.

## When to use Kroki and when to use SchemDraw

- **Use Kroki** for conceptual explanations, functional blocks, timing, instrumentation, and signal flow.
- **Use SchemDraw** for resistors, capacitors, sources, switches, and formal electrical schematics.

## 1. Mermaid: instrumentation chain

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

## 3. Wavedrom: input and output signals

```{kroki}
:type: wavedrom
:align: center

{ signal: [
  { name: "Vin", wave: "p....|...." },
  { name: "Vout", wave: "0.p..|.p..", phase: 0.5 },
  { name: "I", wave: "0..p.|..p.", phase: 0.75 }
]}
```

## 4. Ditaa: quick experimental bench sketch

```{kroki}
:type: ditaa
:align: center

+----------+      +------------+      +-------------+
| Generator |----->| RC Circuit |----->| Oscilloscope |
+----------+      +------------+      +-------------+
```

## Key idea

Kroki **complements** SchemDraw. They do not compete:

- **SchemDraw** = exact circuit
- **Kroki** = system-level visual explanation
