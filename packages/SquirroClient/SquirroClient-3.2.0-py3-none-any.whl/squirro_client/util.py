from __future__ import division
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
import warnings


def deprecation(message):
    warnings.warn(message, DeprecationWarning, stacklevel=2)


# Enable deprecation warnings.
warnings.simplefilter("default")
