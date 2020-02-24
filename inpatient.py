import requests
from trytond.pool import Pool
from trytond.model import ModelView, ModelSQL, fields
from datetime import datetime
from trytond.modules.health_inpatient import health_inpatient as baseInpatient
from .queryicd11 import query_icd11

class InpatientRegistration(baseInpatient.InpatientRegistration):
    __name__ = 'gnuhealth.inpatient.registration'

    icd10 = fields.Many2One('gnuhealth.pathology', 'ICD 10',
        domain=[('classifier', '=', 'ICD10')] ,select=True)
    
    icd11 = fields.Char('Main Condition Code')
    icd11_description = fields.Function(
        fields.Text('Main Condition Interpretation'), 'get_icd11_information')

    # icd11_other = fields.MultiValue(fields.Char('Other Conditions'))
    # icd11_description = fields.Function(
    #     fields.Text('Other Conditions - Interpretation'), 'get_icd11_other_conditions')

    #  fields.Many2One('gnuhealth.pathology', 'ICD 11', 
        # domain=[('classifier', '=', 'ICD11')], select=True)
    other = fields.Char('Other Condition')
    procedures = fields.Char('Procedures')
    new_diag = fields.Boolean('Newly Diagnosed', select=True)
    re_admiss = fields.Boolean('Re-Admission', select=True)

    def get_icd11_information(self, name):
        if not self.icd11:
            return ''
        return self.build_condition_str(self.icd11)

    def get_icd11_other_conditions(self, name):
        if not self.icd11_other:
            return ''
        print("Other")
        print(self.icd11_other)
        # return self.build_condition_str(self.icd11)
        return ''
    
    def build_condition_str(self, code):
        try:
            output = query_icd11(code)
        except requests.exceptions.ConnectionError as e:
            print("Except as e: {}".format(e))
            return 'Error: Cannot connect to the disease database container.'
        except Except as e:
            print("Except as e: {}".format(e))
            return ''
        descriptions = []
        for item in output:
            descriptions.append('{} - {}'.format(item['code'], item['description']))
        return '\n'.join(descriptions)


    @classmethod
    def __setup__(cls):
	    super(InpatientRegistration, cls).__setup__()
