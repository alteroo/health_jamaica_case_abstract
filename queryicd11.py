import requests
import sys


def query_icd11(cluster_code,  host='http://localhost:7654'):
    base_uri = host + '/icd/release/11/2019-04/mms/codeinfo/{}'
    mms_uri = host + '/icd/release/11/2019-04/mms{}'
    cluster_output = []
    last_splitter = ""
    # HTTP header fields to set
    headers = {
            'Accept': 'application/json',
            'Accept-Language': 'en',
            'API-Version': 'v2'}

    def code_to_description(code):
        uri = base_uri.format(code)
        req = requests.get(uri, headers=headers, verify=False)
        output = req.json()
        stem = output['stemId'].split('/mms')[-1]
        stem_uri = mms_uri.format(stem)
        req = requests.get(stem_uri, headers=headers, verify=False)
        output = req.json()
        return output['title']['@value']

    def cluster_walker(cluster):
        # does list contain / codes
        if "/" in cluster:
            last_splitter = "/"
            cluster_list = cluster.split('/')
            for item in cluster_list:
                cluster_walker(item)
        elif "&X" in cluster:
            last_splitter = "&"
            cluster_list = cluster.split('&')
            for item in cluster_list:
                cluster_walker(item)
        else:
            cluster_output.append({'code':cluster,'description':code_to_description(cluster)})

    cluster_walker(cluster_code)
    return cluster_output
