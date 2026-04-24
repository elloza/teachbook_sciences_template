# Thebe + Pyodide: Live Code

**Thebe** allows readers to run Python code directly in their browser, without installing anything. It works thanks to **Pyodide**, a version of Python compiled to WebAssembly.

```{warning}
Thebe is an **HTML-only** feature. It is not available in PDF export. It also requires the `sphinx-thebe` extension configured in your `_config.yml`.
```

## How does it work?

1. The reader clicks the **"Live Code"** button on the page.
2. Pyodide loads in the browser (may take a few seconds the first time).
3. Code cells become editable and executable.

## Activation button

To show the "Live Code" button on a page, add the directive:

````md
```{thebe-button}
```
````

## Example: executable cell

````md
```{code-block} python
:class: thebe

import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 2 * np.pi, 100)
y = np.sin(x)

plt.figure(figsize=(8, 4))
plt.plot(x, y, label='sin(x)')
plt.title('Sine wave')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
```
````

The reader can modify parameters (e.g., change `np.sin` to `np.cos`) and re-run the cell.

## Required configuration

To enable Thebe, your `_config.yml` must include:

```yaml
sphinx:
  extra_extensions:
    - sphinx_thebe
  config:
    thebe_config:
      use_thebe_lite: true
      always_load: false
```

This configuration uses **Thebe Lite** with Pyodide, which loads Python directly in the browser without needing Binder. This is ideal for books that don't need actual notebooks in the repository.

```{admonition} Simpler alternative
:class: tip
If you don't want to set up Thebe, you can use **Google Colab**. Upload your notebook to Colab and share the link in your TeachBook. Students can run the code in the cloud with no installation.
```
