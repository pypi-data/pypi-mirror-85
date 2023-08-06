# atlasify

[![Pipeline status](https://gitlab.cern.ch/fsauerbu/atlasify/badges/master/pipeline.svg)](https://gitlab.cern.ch/fsauerbu/atlasify/-/pipelines)
[![Pylint score](https://gitlab.cern.ch/fsauerbu/atlasify/-/jobs/artifacts/master/raw/pylint.svg?job=pylint)](https://gitlab.cern.ch/fsauerbu/atlasify) 
[![GNU AGPLv3](https://gitlab.cern.ch/fsauerbu/atlasify/-/jobs/artifacts/master/raw/license.svg?job=badges)](https://gitlab.cern.ch/fsauerbu/atlasify/-/blob/master/LICENSE)
[![PyPI](https://gitlab.cern.ch/fsauerbu/atlasify/-/jobs/artifacts/master/raw/pypi.svg?job=badges)](https://pypi.org/project/atlasify/)


The Python package `atlasify` applies the ATLAS style to matplotlib plots. This includes

 - Switching to Arial font (not Helvetica since it's not widely available),
 - Adding ticks on all edges,
 - Making ticks to inward,
 - Adding the ***ATLAS*** badge with optional labels (e.g. Internal),
 - Adding a description below the badge, and
 - Moving the ***ATLAS*** badge outside the axes area.

## Quickstart

The package will use Helvetica. The
package ships with GPL-licensed Nimbus Sans L as a fallback.

The `atlasify` package can be installed using pip.

```console
pip install atlasify
# or 
pip install https://gitlab.cern.ch/fsauerbu/atlasify/-/archive/master/atlasify-master.tar.gz
```


## Usage

To apply the basic style, simply call the method without any arguments.


<!-- write example.py -->
```python
import matplotlib.pyplot as plt
import numpy as np
from atlasify import atlasify

x = np.linspace(-3, 3, 200)
y = np.exp(-x**2)

plt.plot(x, y)
atlasify()
plt.savefig("test_1.pdf")
```

<!-- append example.py
```python
plt.savefig("test_1.png", dpi=300)
plt.clf()
```
-->

![ATLAS style plot](https://gitlab.cern.ch/fsauerbu/atlasify/-/jobs/artifacts/master/raw/test_1.png?job=doxec)

## Label
If the first argument is a string, e.g. `Internal`, it is added after
the ***ATLAS*** badge.

<!-- append example.py -->
```python
plt.plot(x, y)
atlasify("Internal")
plt.savefig("test_2.pdf")
```

<!-- append example.py
```python
plt.savefig("test_2.png", dpi=300)
plt.clf()
```
-->

![ATLAS style plot](https://gitlab.cern.ch/fsauerbu/atlasify/-/jobs/artifacts/master/raw/test_2.png?job=doxec)

## Subtext
The second argument can be used to add text on the second line. Multiple lines
are rendered independently.

<!-- append example.py -->
```python
plt.plot(x, y)
atlasify("Internal", 
         "The Gaussian is defined by the\n"
         "function $f(x) = e^{-x^2}$.\n")
plt.savefig("test_3.pdf")
```

<!-- append example.py
```python
plt.savefig("test_3.png", dpi=300)
plt.clf()
```
-->

![ATLAS style plot](https://gitlab.cern.ch/fsauerbu/atlasify/-/jobs/artifacts/master/raw/test_3.png?job=doxec)

## Enlarge
Usually there is not enought space for the additinal ***ATLAS*** badge. By
default, the method enlarges the y-axis by a factor of `1.3`. The factor can
be changed with the `enlarge` keyword argument.

<!-- append example.py -->
```python
plt.plot(x, y)
atlasify("Internal", enlarge=1.5)
plt.savefig("test_4.pdf")
```

<!-- append example.py
```python
plt.savefig("test_4.png", dpi=300)
plt.clf()
```
-->

![ATLAS style plot](https://gitlab.cern.ch/fsauerbu/atlasify/-/jobs/artifacts/master/raw/test_4.png?job=doxec)

## Changing ATLAS
Plots for the ATLAS upgrade are not tagged wth ***ATLAS*** itself. The text of
the badge can be modified via a module constant.

<!-- append example.py -->
```python
import atlasify as atl
atl.ATLAS = "ITk Strip"

plt.plot(x, y)
atlasify("Test beam")
plt.savefig("test_9.pdf")
```

<!-- append example.py
```python
plt.savefig("test_9.png", dpi=300)
plt.clf()
atl.ATLAS = "ATLAS"
```
-->

![ATLAS style plot](https://gitlab.cern.ch/fsauerbu/atlasify/-/jobs/artifacts/master/raw/test_9.png?job=doxec)

## Resolution, Font and figure size
The font sizes are defined in module constants and can be changed on demand.
Please note that the apparent size of the badge does not change when the
resolution is changed. However, the badge appears to be larger when the figure
size is made smaller.

In the two following plots with different resolution, the badges take the same fraction
of the canvas.
<!-- append example.py -->
```python
plt.plot(x, y)
atlasify("Internal")
plt.savefig("test_5.png", dpi=72)
plt.savefig("test_6.png", dpi=300)
```

<!-- append example.py
```python
plt.clf()
```
-->

![ATLAS style plot](https://gitlab.cern.ch/fsauerbu/atlasify/-/jobs/artifacts/master/raw/test_5.png?job=doxec)
![ATLAS style plot](https://gitlab.cern.ch/fsauerbu/atlasify/-/jobs/artifacts/master/raw/test_6.png?job=doxec)

When a smaller figure size is choose, the badge takes a larger fraction of the
canvas.
<!-- append example.py -->
```python
plt.figure(figsize=(4,3))
plt.plot(x, y)
atlasify("Internal")
plt.savefig("test_7.pdf")
```

<!-- append example.py
```python
plt.savefig("test_7.png", dpi=300)
plt.clf()
```
-->

![ATLAS style plot](https://gitlab.cern.ch/fsauerbu/atlasify/-/jobs/artifacts/master/raw/test_7.png?job=doxec)


<!-- append example.py -->
```python
plt.figure(figsize=(4, 4))
heatmap = np.random.normal(size=(4, 4))

plt.imshow(heatmap)
atlasify("Internal", "Random heatmap, Outside badge", outside=True)
plt.tight_layout()
plt.savefig("test_8.pdf")
```

<!-- append example.py
```python
plt.savefig("test_8.png", dpi=300)
plt.clf()
```
-->

![ATLAS style plot](https://gitlab.cern.ch/fsauerbu/atlasify/-/jobs/artifacts/master/raw/test_8.png?job=doxec)

## Axis labels

The module provides the convenience methods `set_xlabel()` and `set_ylabel()`
to set the axis labels. This will make then automatically aligned to the right
and top. For event more convenience you can call `monkeypatch_axis_labels()`
to change the default align behavior.

<!-- append example.py -->
```python
from atlasify import monkeypatch_axis_labels
monkeypatch_axis_labels()

plt.figure(figsize=(4,3))
plt.plot(x, y)
plt.xlabel(r"$\phi$")
plt.ylabel(r"Depth (a. u.)")
atlasify("Internal")
plt.tight_layout()
plt.savefig("test_10.pdf")
```

<!-- append example.py
```python
plt.savefig("test_10.png", dpi=300)
plt.clf()
```
-->

![ATLAS style plot](https://gitlab.cern.ch/fsauerbu/atlasify/-/jobs/artifacts/master/raw/test_10.png?job=doxec)

## Example
*Real* world example histogram showing two Gaussian blobs representing a *Z*
boson background and a Higgs boson signal.

<!-- append example.py -->
```python
# Unbinned data
Z = np.random.normal(90, 10, size=10000)
H = np.random.normal(125, 10, size=1000)

# Manual binning, or reading from TH1F
bins = np.linspace(50, 200, 31)
Z_counts, _ = np.histogram(Z, bins=bins)
H_counts, _ = np.histogram(H, bins=bins)

plt.figure(figsize=(5,4))

# Drawing shapes
plt.hist(bins[:-1], bins=bins, weights=Z_counts,
                    label="$Z$ boson", histtype='stepfilled')
plt.hist(bins[:-1], bins=bins, weights=H_counts, bottom=Z_counts,
                    label="Higgs boson", histtype='stepfilled')

# Styling
plt.xlabel("Mass $m$ / GeV", ha='right', x=0.95)
plt.ylabel("Events / 5 GeV", ha='right', y=0.95)
plt.xlim((bins[0], bins[-1]))
atlasify("Internal", r"$\sqrt{s} = 13\,\mathrm{TeV}$")
plt.tight_layout()
plt.savefig("test_histo.pdf")
```

<!-- append example.py
```python
plt.savefig("test_histo.png", dpi=300)
plt.clf()
```
-->

![ATLAS style
plot](https://gitlab.cern.ch/fsauerbu/atlasify/-/jobs/artifacts/master/raw/test_histo.png?job=doxec)

<!-- console
```
$ python3 example.py
```
-->



