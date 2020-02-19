from trytond.pool import Pool
from trytond.model import ModelView, ModelSQL, fields
from datetime import datetime
from trytond.modules.health_inpatient import health_inpatient as baseInpatient

class InpatientRegistration(baseInpatient.InpatientRegistration):
    __name__ = 'gnuhealth.inpatient.registration'

    icd10 = fields.Many2One('gnuhealth.pathology', 'ICD 10',
        domain=[('classifier', '=', 'ICD10')] ,select=True)
    icd11 = fields.Many2One('gnuhealth.pathology', 'ICD 11', 
        domain=[('classifier', '=', 'ICD11')], select=True)
    other = fields.Char('Other Condition')
    procedures = fields.Char('Procedures')
    new_diag = fields.Boolean('Newly Diagnosed', select=True)
    re_admiss = fields.Boolean('Re-Admission', select=True)

    @classmethod
    def __setup__(cls):
	    super(InpatientRegistration, cls).__setup__()
