import os
import requests
from trytond.pool import Pool
from trytond.model import ModelView, ModelSQL, fields
from datetime import datetime
from trytond.config import config
from .queryicd11 import query_icd11


def get_icd_url():
    try:
        icd_uri = config.get('icd', 'api_uri')
    except:
        icd_uri = ''

    if icd_uri:
        return icd_uri
    return os.environ.get('ICD_CONTAINER_URL', 'http://localhost:7654')


def get_coding_tool_url():
    try:
        icd_uri = config.get('icd', 'coding_tool_uri')
    except:
        icd_uri = '{}/ct11/icd11_mms/en/release'.format(get_icd_url())
    return icd_uri


class CaseAbstract(ModelSQL, ModelView):
    'Medical Record Case Abstract'
    __name__ = 'mrca.mrca'

    icd10 = fields.Many2One('gnuhealth.pathology', 'ICD 10',
        domain=[
            'OR',
            ('classifier', '=', 'ICD10'),
            ('classifier', '=', None)
        ] ,select=True)
    
    patient = fields.Many2One('gnuhealth.inpatient.registration', 'Patient', domain=[('state', '=', 'done')], required=True, select=True)

    icd11 = fields.Char('Main Condition Code')
    icd11_description = fields.Function(
        fields.Text('Main Condition Interpretation'), 'get_icd11_information')

    icd11_other = fields.Text('Other Conditions')
    icd11_other_description = fields.Function(
        fields.Text('Other Conditions - Interpretation'), 'get_icd11_other_conditions')

    coding_tool = fields.Function(
        fields.Char('Coding Tool'), 'get_coding_tool_url')

    icd10_other = fields.Many2Many('mrca.mrca_patient.abstract', 'code', 'code','Other Conditions (ICD 10)')
    icd10_procedures = fields.Many2Many('mrca.mrca_patient.abstract', 'description', 'description','Procedures (ICD 10)')

    new_diag = fields.Boolean('Newly Diagnosed', select=True)
    re_admiss = fields.Boolean('Re-Admission', select=True)

    def get_coding_tool_url(self, ids=None, name=None):
        return get_coding_tool_url()

    @classmethod
    def default_coding_tool(cls):
        return get_coding_tool_url()

    def get_icd_url(self, name=None):
        return get_icd_url()

    def get_icd11_information(self, name):
        if not self.icd11:
            return ''
        return self.build_condition_str(self.icd11)

    def get_icd11_other_conditions(self, name):
        if not self.icd11_other:
            return ''
        codes = self.icd11_other.split('\n')
        descriptions = []
        for code in codes:
            desc = self.build_condition_str(code)
            if not desc or desc in descriptions:
                continue
            title = 'Interpretation for {}'.format(code)
            sep = '-' * (len(title) * 2)
            descriptions.append(
                '{}\n{}\n{}'.format(title, sep, desc)
            )
        return '\n\n'.join(descriptions)
    
    def build_condition_str(self, code):
        host = self.get_icd_url()
        try:
            output = query_icd11(code, host=host)
        except requests.exceptions.ConnectionError as e:
            print("Except as e: {}".format(e))
            return 'Error: Cannot connect to the disease database container.'
        except Exception as e:
            print("Except as e: {}".format(e))
            return ''
        descriptions = []
        for item in output:
            descriptions.append('- {} - {}'.format(item['code'], item['description']))
        return '\n'.join(descriptions)


    @classmethod
    def __setup__(cls):
	    super(CaseAbstract, cls).__setup__()

class PatientAbstract(ModelSQL, ModelView):
    'Pathology-Icpm'
    __name__ = 'mrca.mrca_patient.abstract'

    code = fields.Many2One('gnuhealth.pathology', 'ICD10')
    description = fields.Many2One('gnuhealth.procedure', 'Description')

    @classmethod
    def __setup__(cls):
        super(PatientAbstract, cls).__setup__()
