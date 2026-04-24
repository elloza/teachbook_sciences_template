# Thebe + Pyodide: Live Code

**Thebe** allows readers to run Python code directly in their browser, without installing anything. It works thanks to **Pyodide**, a version of Python compiled to WebAssembly.

```{warning}
Thebe is an **HTML-only** feature. It is not available in PDF export.
```

## How does it work?

1. Click the **"Live Code"** button below.
2. Pyodide loads in the browser (may take a few seconds the first time).
3. Code cells become editable and executable — try it!

---

## Try it: executable code

Click the button to activate interactive mode. Then you can edit and run the cells.

```{thebe-button}
```

````{div} full-width
```{code-block} python
:class: thebe

import numpy as np

# Create an array from 0 to 2π
x = np.linspace(0, 2 * np.pi, 100)

# Calculate sine and cosine
y_sin = np.sin(x)
y_cos = np.cos(x)

print(f"Mean of sine: {np.mean(y_sin):.4f}")
print(f"Mean of cosine: {np.mean(y_cos):.4f}")
print(f"Max value of sine: {np.max(y_sin):.4f}")
print("It works! Try changing np.sin to another function.")
```
````

````{div} full-width
```{code-block} python
:class: thebe

import matplotlib.pyplot as plt
import numpy as np

# Modifiable parameters
frequency = 2    # Hz
amplitude = 1.0  # Scale
phase = 0        # Radians

t = np.linspace(0, 2*np.pi, 200)
signal = amplitude * np.sin(frequency * t + phase)

plt.figure(figsize=(8, 3))
plt.plot(t, signal, 'b-', linewidth=2, label=f'{amplitude}·sin({frequency}t + {phase})')
plt.title('Interactive Sine Wave')
plt.xlabel('Time (rad)')
plt.ylabel('Amplitude')
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()
```
````

---

## How to add this to your pages

### 1. Activation button

Add this directive where you want the "Live Code" button to appear:

````md
```{thebe-button}
```
````

### 2. Executable cell

Use `code-block` with the `thebe` class:

````md
```{code-block} python
:class: thebe

import numpy as np
print("Hello from the browser!")
```
````

### 3. `_config.yml` configuration

Your `_config.yml` must include the `sphinx-thebe` extension:

```yaml
sphinx:
  extra_extensions:
    - sphinx_thebe
  config:
    thebe_config:
      use_thebe_lite: true
      always_load: false
```

This configuration uses **Thebe Lite** with Pyodide, which loads Python directly in the browser without needing Binder.

```{admonition} Simpler alternative
:class: tip
If you don't want to set up Thebe, you can use **Google Colab**. Upload your notebook to Colab and share the link in your TeachBook. Students can run the code in the cloud with no installation.
```
