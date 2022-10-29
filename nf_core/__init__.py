#!/usr/bin/env python
""" Main nf_core module file.

Shouldn't do much, as everything is under subcommands.
"""

import pkg_resources as _pkg_resources

__version__ = _pkg_resources.get_distribution("nf_core").version
