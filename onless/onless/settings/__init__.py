from .base import *

try:
    from onless.settings.local import *
except:
    pass

try:
    from onless.settings.production import *
except:
    pass

