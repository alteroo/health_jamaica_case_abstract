# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.pool import Pool
from .inpatient import *

def register():
    Pool.register(
    	InpatientRegistration,
        module='inpatient', type_='model')
    Pool.register(module='inpatient', type_='wizard')
    
    Pool.register(module='inpatient', type_='report')
