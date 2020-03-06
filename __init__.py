# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.pool import Pool
from .healthAbstract import *


def register():
    Pool.register(
        CaseAbstract,
        PatientAbstract,
        module='health_jamaica_case_abstract', type_='model')
    Pool.register(
        module='health_jamaica_case_abstract', type_='wizard')
    Pool.register(
        module='health_jamaica_case_abstract', type_='report')
