# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['saturn_notebook']

package_data = \
{'': ['*']}

install_requires = \
['argh>=0.26.2,<0.27.0',
 'atomicwrites>=1.4.0,<2.0.0',
 'dill>=0.3.2,<0.4.0',
 'importlib_metadata>=1.7.0,<2.0.0',
 'markdown>=3.2.2,<4.0.0',
 'matplotlib>=3.2.2,<4.0.0',
 'more_itertools>=8.4.0,<9.0.0',
 'ptpython>=3.0.2,<4.0.0',
 'pygments>=2.6.1,<3.0.0',
 'rich>=2.2.3,<3.0.0',
 'wurlitzer>=2.0.0,<3.0.0']

entry_points = \
{'console_scripts': ['saturn = saturn_notebook.__main__:main']}

setup_kwargs = {
    'name': 'saturn-notebook',
    'version': '1.0.3',
    'description': 'Plain-text Python notebooks with checkpointing',
    'long_description': "# Saturn\n\n[Screenshots](#screenshots)\n\n## Features\n\n* Plain-text format. Notebooks are regular Python files. Different types of\n  cells are comments with special formatting.\n\n* Checkpoints. Special checkpoint cells allow to save the state of the session\n  or individual variables.\n\n* Terminal graphics support. When using\n  [kitty](https://sw.kovidgoyal.net/kitty/) terminal (or in principle anything\n  that supports its [graphics protocol](https://sw.kovidgoyal.net/kitty/graphics-protocol.html))\n  matplotlib figures are rendered inline in the terminal.\n\n* MPI awareness. When running under MPI, only rank 0 will write out the\n  modified notebook. The REPL will take input on rank 0 and broadcast to other\n  ranks. It's also possible to suppress output from all ranks other than 0.\n\n## Commands and options\n\n* `saturn show notebook.py`\n\n  Display the notebook in the terminal. No computation is performed. Optional\n  `--html OUTPUT.html` flag will produce HTML output.\n\n* `saturn run notebook.py [output.py]`\n\n  Execute a Python notebook, either modifying it in place, or saving the result\n  into a new notebook `output.py`.\n\n  * `-c, --clean`: run from scratch, ignoring the checkpoints.\n  * `-a, --auto-capture`: automatically capture matplotlib figures, without `show()`.\n  * `-r, --repl`:\n    drop into REPL (using [ptpython](https://github.com/prompt-toolkit/ptpython))\n    after all the cells are processed; the results of the REPL interaction will\n    be added to the notebook.\n  * `-n, --dry-run`: don't save the result.\n  * `--only-root-output`: under MPI, suppress output from all ranks other than 0.\n\n* `saturn clean notebook.py [output.py]`\n\n  Remove all binary data from the notebook. Useful for getting rid of large\n  checkpoints.\n\n* `saturn image notebook.py [i out.png]`\n\n  Save `i`-th image from `notebook.py` into `out.png`. If the last two\n  arguments are omitted, show all the images in the notebook together with\n  their indices.\n\n* `saturn version`\n\n  Show version of saturn and its dependencies.\n\n\n## Cell types\n\n* Markdown cells, prefix `#m>`\n\n  ```\n  #m> # Sample notebook\n  #m>\n  #m> Description using markdown **formatting**.\n  ```\n\n* Output cells `#o>`\n\n  There is not usually a reason to modify these by hand, they are filled by\n  Saturn with the output of code cells. If they contain PNG information, it's\n  base64-encoded and wrapped in `{{{` and `}}}` to allow automatic folding.\n\n  ```\n  #o> <matplotlib.image.AxesImage object at 0x114217550>\n  #o> png{{{\n  #o> pngiVBORw0KGgoAAAANSUhEUgAAA8AAAAHgCAYAAABq5QSEAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAP\n  ...\n  #o> pngGAAAgBQEMAAAACkIYAAAAFL4v5JTyvRQ4v1eAAAAAElFTkSuQmCC\n  #o> png}}}\n  ```\n\n  In Vim with `foldmethod=marker`:\n  ```\n  #o> <matplotlib.image.AxesImage object at 0x114217550>\n  +--135 lines: o> png--------------------------------------------------\n  ```\n\n* Checkpoint cells `#chk>`\n\n  These indicate locations, where the code should checkpoint. Checkpointing\n  serializes the session, which is stored base64-encoded in the same cell. The\n  cell also stores the hash of the previous code blocks, and the checkpoint is\n  valid if the prior code blocks haven't changed. By default saturn will resume\n  from the last valid checkpoint. Same folding markers (`{{{` and `}}}`) are used.\n\n  ```\n  #chk>{{{\n  #chk>gANDIJZCQePiVH9SX7wVtBfgrDpcgWu5HUFFiFEeyNF9sVjFcQB9cQEoWAwAAABfX2J1aWx0aW5zX19x\n  ...\n  #chk>wAyP55wdmz+qIkdBjBrYP3EjdHEkYnWGcSUu\n  #chk>}}}\n  ```\n\n  In Vim with `foldmethod=marker`:\n  ```\n  +-- 36 lines: chk>----------------------------------------------------\n  ```\n\n* Variable cells `#var> x,y,z`\n\n  These cells save only the value of the specified variables (which is useful\n  if the full checkpoint is too big). If all the previous code cells haven't\n  changed, the cell's saved content is loaded into the specified variables and\n  the previous code cell is not evaluated.\n\n* Break cells `#---#`\n\n  These are used to break code cells that don't have any other type of a cell\n  between them.\n\n* Code cells\n\n  All contiguous lines, not marked as one of the above, are grouped together\n  into code cells.\n\n* Non-skippable code cells `#no-skip#`\n\n  Adding this line anywhere within the code cell will indicate that it\n  shouldn't be skipped, even if we are restarting from a checkpoint. This is\n  useful, for example, if a cell is modifying `sys.path`, which won't be\n  captured in a checkpoint.\n\n* Non-hashable code cells `#no-hash#`\n\n  Adding this line anywhere within the code cell will indicate that it\n  shouldn't be hashed, meaning that changing this cell (or removing it\n  entirely) won't invalidate the checkpoints below. This should be used only\n  with cells that don't change any variables, e.g., purely output or plotting\n  cells.\n\n## Vim support\n\nAll the binary (non-human-readable) cell content is wrapped in `{{{`, `}}}`\nmarkers. Adding the following comment to the notebook, ensures that Vim starts\nwith all the binary content folded away.\n\n```\n# vim: foldmethod=marker foldlevel=0\n```\n\n## Screenshots\n\nRunning [samples/simple.py](https://github.com/mrzv/saturn/blob/master/samples/simple.py):\n\n* First run performs full computation and saves the checkpoint, as well as the figure output.\n\n![First run](https://github.com/mrzv/saturn/raw/master/resources/screenshots/simple-first-run.png)\n\n* Second run resumes from the checkpoint, since no code before it has changed.\n\n![Second run](https://github.com/mrzv/saturn/raw/master/resources/screenshots/simple-second-run.png)\n\n* Vim folds the binary content.\n\n![Vim folding](https://github.com/mrzv/saturn/raw/master/resources/screenshots/simple-vim.png)\n",
    'author': 'Dmitriy Morozov',
    'author_email': 'dmitriy@mrzv.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mrzv/saturn',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
