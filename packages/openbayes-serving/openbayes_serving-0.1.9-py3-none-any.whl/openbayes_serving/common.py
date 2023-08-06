# -*- coding: utf-8 -*-

# -- stdlib --
import functools
import os
import sys

# -- third party --
# -- own --

# -- code --
@functools.lru_cache(1)
def detect_env():
    if sys.platform == 'win32':
        return 'local'

    if os.environ.get('OPENBAYES_JOB_URL'):
        return 'gear'

    if os.environ.get('OPENBAYES_SERVING_PRODUCTION'):
        return 'production'

    return 'local'
