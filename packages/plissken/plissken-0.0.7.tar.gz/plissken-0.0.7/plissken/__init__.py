import os

from plissken.documents.helpers import prettyDoc
from plissken.documents.package import PackageDoc

__version__ = (
    open(os.path.join(os.path.dirname(__file__), "VERSION"), "r").read().strip()
)
