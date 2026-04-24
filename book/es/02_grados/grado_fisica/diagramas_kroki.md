# Diagramas Técnicos con Kroki para Física

Kroki es útil para representar **diagramas de bloques, flujo de señales, cronogramas y esquemas conceptuales**. Para **circuitos eléctricos precisos**, la herramienta recomendada sigue siendo **SchemDraw**.

## Cuándo usar Kroki y cuándo SchemDraw

- **Usa Kroki** para explicaciones conceptuales, bloques funcionales, temporización, instrumentación y flujo de señal.
- **Usa SchemDraw** para resistencias, condensadores, fuentes, interruptores y esquemas eléctricos formales.

## 1. Mermaid: cadena de instrumentación

```{kroki}
:type: mermaid
:align: center

flowchart LR
    G[Generador] --> R[Circuito RC]
    R --> O[Osciloscopio]
    R --> M[Multímetro]
    O --> A[Análisis de fase]
    M --> B[Medida de amplitud]
```

## 2. GraphViz: flujo de señal en un montaje

```{kroki}
:type: graphviz
:align: center

digraph G {
    rankdir=LR;
    Generador -> "Circuito RC";
    "Circuito RC" -> Osciloscopio;
    "Circuito RC" -> "Sensor de corriente";
    Osciloscopio -> "Cálculo de desfase";
    "Sensor de corriente" -> "Cálculo de impedancia";
}
```

## 3. Wavedrom: señales de entrada y salida

```{kroki}
:type: wavedrom
:align: center

{ signal: [
  { name: "Vin", wave: "p....|...." },
  { name: "Vout", wave: "0.p..|.p..", phase: 0.5 },
  { name: "I", wave: "0..p.|..p.", phase: 0.75 }
]}
```

## 4. Ditaa: esquema rápido de banco experimental

```{kroki}
:type: ditaa
:align: center

+----------+      +------------+      +-------------+
| Generador |----->| Circuito RC |----->| Osciloscopio |
+----------+      +------------+      +-------------+
```

## Idea clave

Kroki **complementa** a SchemDraw. No compiten:

- **SchemDraw** = circuito exacto
- **Kroki** = explicación visual del sistema
