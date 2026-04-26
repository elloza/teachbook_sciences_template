# Diagramas Técnicos con Kroki para Física

Kroki es útil para representar **diagramas de bloques, flujo de señales, cronogramas y esquemas conceptuales**. Para **circuitos eléctricos con símbolos normalizados**, la herramienta recomendada es **CircuitikZ renderizado como imagen**.

## Cuándo usar cada herramienta

- **Usa Kroki** para explicaciones conceptuales, bloques funcionales, temporización, instrumentación y flujo de señal.
- **Usa WaveDrom vía Kroki** para señales digitales, buses, relojes y protocolos temporales.
- **Usa CircuitikZ** para resistencias, condensadores, fuentes, interruptores y esquemas eléctricos formales.
- **Usa SchemDraw** cuando quieras construir circuitos sencillos desde Python dentro de un notebook.

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

## 3. CircuitikZ: circuito docente como imagen

El circuito siguiente no se dibuja a mano: procede de un archivo `.tex` con código CircuitikZ, renderizado previamente como imagen para que funcione igual en HTML y PDF.

```{figure} ../../../_static/generated/circuito_rc_circuitikz.png
:alt: Circuito RC generado con CircuitikZ
:width: 70%
:align: center

Circuito RC generado desde código CircuitikZ.
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

```{admonition} Importante
:class: warning
Kroki soporta TikZ, pero el servicio público de Kroki no garantiza tener disponible el paquete `circuitikz`. Para circuitos docentes robustos, en este proyecto se renderiza CircuitikZ localmente a imagen.
```

## 4. Wavedrom: señales de entrada y salida

```{kroki}
:type: wavedrom
:align: center

{ signal: [
  { name: "Vin", wave: "p....|...." },
  { name: "Vout", wave: "0.p..|.p..", phase: 0.5 },
  { name: "I", wave: "0..p.|..p.", phase: 0.75 }
]}
```

## 5. Ditaa: esquema rápido de banco experimental

```{kroki}
:type: ditaa
:align: center

+----------+      +------------+      +-------------+
| Generador |----->| Circuito RC |----->| Osciloscopio |
+----------+      +------------+      +-------------+
```

## Idea clave

Kroki, CircuitikZ y SchemDraw **se complementan**. No compiten:

- **Kroki** = explicación visual del sistema, bloques, flujos y cronogramas.
- **CircuitikZ** = circuito formal con símbolos normalizados y acabado LaTeX.
- **SchemDraw** = circuito programable desde Python, ideal para notebooks docentes.
