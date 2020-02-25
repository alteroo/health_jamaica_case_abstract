import os
import requests
from trytond.pool import Pool
from trytond.model import ModelView, ModelSQL, fields
from datetime import datetime
from trytond.config import config
from trytond.modules.health_inpatient import health_inpatient as baseInpatient
from .queryicd11 import query_icd11


def get_icd_url():

    try:
        icd_uri = config.get('icd', 'uri')
    except:
        icd_uri = ''

    if icd_uri:
        return icd_uri
    return os.environ.get('ICD_CONTAINER_URL', 'http://localhost:7654')


class InpatientRegistration(baseInpatient.InpatientRegistration):
    __name__ = 'gnuhealth.inpatient.registration'

    icd10 = fields.Many2One('gnuhealth.pathology', 'ICD 10',
        domain=[('classifier', '=', 'ICD10')] ,select=True)
    
    icd11 = fields.Char('Main Condition Code')
    icd11_description = fields.Function(
        fields.Text('Main Condition Interpretation'), 'get_icd11_information')

    icd11_other = fields.Text('Other Conditions')
    icd11_other_description = fields.Function(
        fields.Text('Other Conditions - Interpretation'), 'get_icd11_other_conditions')

    coding_tool = fields.Function(
        fields.Char('Coding Tool'), 'get_coding_tool_url')

    #  fields.Many2One('gnuhealth.pathology', 'ICD 11', 
        # domain=[('classifier', '=', 'ICD11')], select=True)
    other = fields.Char('Other Condition')
    procedures = fields.Char('Procedures')
    new_diag = fields.Boolean('Newly Diagnosed', select=True)
    re_admiss = fields.Boolean('Re-Admission', select=True)

    def get_coding_tool_url(self, ids=None, name=None):
        url = get_icd_url()
        return '{}/ct11/icd11_mms/en/release'.format(url)

    @classmethod
    def default_coding_tool(cls):
        return get_icd_url()

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
	    super(InpatientRegistration, cls).__setup__()
