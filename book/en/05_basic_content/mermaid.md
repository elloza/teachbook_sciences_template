(mermaid)=
# Mermaid Diagrams

**Mermaid** lets you create diagrams directly in Markdown without external tools. Diagrams render automatically in HTML.

```{warning}
Mermaid **only works in HTML**. It does not render in PDF. You must always add a text description as an alternative.
```

## Flowchart (`flowchart`)

````md
```{mermaid}
flowchart LR
    A[Sample] --> B[Preparation]
    B --> C[Measurement]
    C --> D[Analysis]
    D --> E[Results]
```
````

Result (HTML):

```{mermaid}
flowchart LR
    A[Sample] --> B[Preparation]
    B --> C[Measurement]
    C --> D[Analysis]
    D --> E[Results]
```

Description: The flow goes left to right: Sample → Preparation → Measurement → Analysis → Results.

## Sequence diagram (`sequenceDiagram`)

````md
```{mermaid}
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

Result (HTML):

```{mermaid}
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
```{mermaid}
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

Result (HTML):

```{mermaid}
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
```{mermaid}
erDiagram
    STUDENT ||--o{ ENROLLMENT : makes
    ENROLLMENT }o--|| COURSE : belongs_to
    COURSE ||--o{ LAB : includes
```
````

Result (HTML):

```{mermaid}
erDiagram
    STUDENT ||--o{ ENROLLMENT : makes
    ENROLLMENT }o--|| COURSE : belongs_to
    COURSE ||--o{ LAB : includes
```

## State diagram (`stateDiagram-v2`)

````md
```{mermaid}
stateDiagram-v2
    [*] --> Pending
    Pending --> InProgress : start
    InProgress --> Completed : finish
    InProgress --> Error : failure
    Error --> Pending : retry
    Completed --> [*]
```
````

Result (HTML):

```{mermaid}
stateDiagram-v2
    [*] --> Pending
    Pending --> InProgress : start
    InProgress --> Completed : finish
    InProgress --> Error : failure
    Error --> Pending : retry
    Completed --> [*]
```

## Flowchart directions

| Code | Direction |
|------|-----------|
| `flowchart LR` | Left to right |
| `flowchart RL` | Right to left |
| `flowchart TB` | Top to bottom |
| `flowchart BT` | Bottom to top |

```{tip}
If your diagram is key to understanding the content, consider using an externally generated image (PNG/SVG) with the `{figure}` directive instead of Mermaid. That way it will also work in PDF.
```
