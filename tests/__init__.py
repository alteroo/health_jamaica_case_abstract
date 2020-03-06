# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

try:
    from trytond.modules.health_jamaica_case_abstract.tests.test_health_jamaica_case_abstract import suite  # noqa: E501
except ImportError:
    from .test_health_jamaica_case_abstract import suite

__all__ = ['suite']
