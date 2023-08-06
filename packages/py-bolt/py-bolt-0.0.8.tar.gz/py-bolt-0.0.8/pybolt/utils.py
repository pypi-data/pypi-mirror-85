import logging
import sys
import os

log_stderr = logging.StreamHandler(sys.stderr)
default_logger = logging.getLogger(__name__)
default_logger.setLevel(logging.DEBUG)
default_logger.addHandler(log_stderr)

package_path = os.path.abspath(os.path.dirname(sys.modules[__package__].__file__))

__all__ = ['default_logger', 'package_path']
