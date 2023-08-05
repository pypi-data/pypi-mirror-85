# RBToolz

RBToolz is a package of generic analytics tools for use in Jupyter Notebooks that currently cover:

  - Wrappers for Plotly/Pandas postprocessing
  - Timeseries manipulation

### Tech

RBToolz wraps around a number of projects:

* Jupyter Notebook
* Pandas
* Plotly
* Orca

### Installation
Install using regular pip 3.7

```sh
$ pip install rbtoolz
```
### Notebook Setup and Plotting Example

Following steps are required to setup notebook and use postprocessing tools.

Rendering to PNG files requires Orca/PIO installation:

```bash
conda install -c plotly plotly-orca psutil
```

* Notebook Cell HTML changes

```python
from IPython.core.display import display, SVG, HTML
from IPython.display import Image
display(HTML("<style>.container { width:100% !important; }</style>"))
```

* Plotly offline functions
```python
import plotly.graph_objs as go
from plotly.offline import init_notebook_mode, iplot
```

* Import auto_plot from RBToolz
```python
from rbtoolz.plotting import auto_plot
```

* Finally run a demo
```python
df = pd.DataFrame([1,2,3],['A','B','C'])
fig = auto_plot(df)
iplot(fig)
```

* And for rendering figure to png

```python
import plotly.io as pio

def save_fig(fig, filename):
    pio.write_image(fig, format="png", file=filename)

save_fig(fig,'data_chart.png')

display(Image('data_chart.png'))
```

License
----

MIT




