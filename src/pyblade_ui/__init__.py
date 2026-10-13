"""PyBlade UI: copy-paste components and themes for PyBlade.

Importing the package registers the `cn` template filter the components use:

    # Django: add "pyblade_ui" to INSTALLED_APPS
    # Flask, FastAPI...: import pyblade_ui once, before rendering
"""

from .sidebar import sidebar_open
from .utils import cn, tw_merge

__version__ = "0.1.0"
__all__ = ["cn", "tw_merge", "sidebar_open", "__version__"]
