(mermaid)=
# Diagrams with Kroki (Mermaid)

**Kroki** converts text into SVG diagrams during the book build. If you use `:type: mermaid`, you can write Mermaid syntax and get a diagram that works in both **HTML** and **PDF**.

## Flowchart (`flowchart`)

````md
```{kroki}
:type: mermaid
:align: center

flowchart LR
    A[Sample] --> B[Preparation]
    B --> C[Measurement]
    C --> D[Analysis]
    D --> E[Results]
```
````

Result:


The following diagram visually summarizes this part of the explanation.

**Diagram: Flowchart (`flowchart`).**

```{kroki}
:type: mermaid
:align: center

flowchart LR
    A[Sample] --> B[Preparation]
    B --> C[Measurement]
    C --> D[Analysis]
    D --> E[Results]
```

Description: The flow goes left to right: Sample → Preparation → Measurement → Analysis → Results.

## Sequence diagram (`sequenceDiagram`)

````md
```{kroki}
:type: mermaid
:align: center

sequenceDiagram
    participant S as Student
    participant T as Teacher
    participant L as Laboratory
    S->>T: Submit report
    T->>S: Corrections
    S->>L: Book equipment
    L->>S: Confirmation
```
````

Result:


The following diagram visually summarizes this part of the explanation.

**Diagram: Sequence diagram (`sequenceDiagram`).**

```{kroki}
:type: mermaid
:align: center

sequenceDiagram
    participant S as Student
    participant T as Teacher
    participant L as Laboratory
    S->>T: Submit report
    T->>S: Corrections
    S->>L: Book equipment
    L->>S: Confirmation
```

Description: The student submits a report to the teacher, receives corrections, and then books equipment in the laboratory.

## Class diagram (`classDiagram`)

````md
```{kroki}
:type: mermaid
:align: center

classDiagram
    class Experiment {
        +string name
        +date date
        +run()
        +analyze()
    }
    class Sample {
        +string type
        +float mass
        +prepare()
    }
    Experiment --> Sample : uses
```
````

Result:


The following diagram visually summarizes this part of the explanation.

**Diagram: Class diagram (`classDiagram`).**

```{kroki}
:type: mermaid
:align: center

classDiagram
    class Experiment {
        +string name
        +date date
        +run()
        +analyze()
    }
    class Sample {
        +string type
        +float mass
        +prepare()
    }
    Experiment --> Sample : uses
```

## Entity-relationship diagram (`erDiagram`)

````md
```{kroki}
:type: mermaid
:align: center

erDiagram
    STUDENT ||--o{ ENROLLMENT : makes
    ENROLLMENT }o--|| COURSE : belongs_to
    COURSE ||--o{ LAB : includes
```
````

Result:


The following diagram visually summarizes this part of the explanation.

**Diagram: Entity-relationship diagram (`erDiagram`).**

```{kroki}
:type: mermaid
:align: center

erDiagram
    STUDENT ||--o{ ENROLLMENT : makes
    ENROLLMENT }o--|| COURSE : belongs_to
    COURSE ||--o{ LAB : includes
```

## State diagram (`stateDiagram`)

````md
```{kroki}
:type: mermaid
:align: center

stateDiagram
    [*] --> Pending
    Pending --> InProgress : start
    InProgress --> Completed : finish
    InProgress --> Error : failure
    Error --> Pending : retry
    Completed --> [*]
```
````

Result:


The following diagram visually summarizes this part of the explanation.

**Diagram: State diagram (`stateDiagram`).**

```{kroki}
:type: mermaid
:align: center

stateDiagram
    [*] --> Pending
    Pending --> InProgress : start
    InProgress --> Completed : finish
    InProgress --> Error : failure
    Error --> Pending : retry
    Completed --> [*]
```

## Flowchart directions


The following table summarizes the main elements of this section.

**Table. Flowchart directions.**

| Code | Direction |
|------|-----------|
| `flowchart LR` | Left to right |
| `flowchart RL` | Right to left |
| `flowchart TB` | Top to bottom |
| `flowchart BT` | Bottom to top |

```{tip}
Always use `{kroki}` with `:type: mermaid` instead of `{mermaid}`. This makes the diagram work in both HTML and PDF without manual fallbacks.
```
