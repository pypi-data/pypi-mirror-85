#!/usr/bin/env python
# -*- coding:utf-8 -*-

import doctest
import test

doctest.testmod(test, optionflags=doctest.NORMALIZE_WHITESPACE |
                                  doctest.ELLIPSIS |
                                  doctest.REPORT_ONLY_FIRST_FAILURE
                )
