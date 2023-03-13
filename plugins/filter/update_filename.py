# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# Apache 2.0
# (see COPYING)

"""
filter plugin file for update SAP software sownload centeri filename: update_filename
"""

# sys.path.append('/tmp/ansible_collection/ansible_collections/community/sap_launchpad/plugins')

from ansible.errors import AnsibleFilterError
from ..module_utils.sap_launchpad_software_center_download_search_fuzzy import *

DOCUMENTATION = """
  name: update_filename
  author: SLL OSI Community
  version_added: "0.1"
  short_description: searches for name of SAP Product
  description:
    - returns the updated filename of an SAP product in the software download center
  options:
    arg:
      description: old filename
      type: string
      required: true
    suser_id:
      description: SAP S-User ID
      type: string
      required: true
    suser_password:
      description: SAP S-User password
      type: string
  notes:
"""

EXAMPLES = r"""
#### examples
# new_name => IMDB_CLIENT20_014_24-80002082.SAR
- debug:
    msg: "{{ 'IMDB_CLIENT20_014_22-80002082.SAR' | update_filename('suser_id','suser_password') }}"

"""

RETURN = """
  data:
    description: returns the updated name
    type: string
"""

class FilterModule(object):
    def filters(self):
        return {
            'update_filename': self.find_newname
        }

def update_filename(self, filename, username, password):

     # TODO: Zerlege Filename !!
     # input_search_file=sys.argv[1]
     # input_search_file_name_and_version_only=sys.argv[2]
    _filename_noext=_filename.split(".")[0]
    _filename_id_only=_filename_noext.split("-")[1]
    _filename_name_and_version_only=_filename_noext.split("_")[0]
    
    sap_sso_login(username, password)
    query_result = search_software_fuzzy(_filename_id_only)
    if len(query_result) >= 2:
        if '70SWPM' in query_result[0]['Title']:
            return (query_result[-1]['Title'])
        elif any('DBATL' in sublist['Title'] for sublist in query_result):
            for sublist in query_result:
                if sublist['Title'].startswith('DBATL'):
                    return(sublist['Title'])
        elif any('SYBCTRL' in sublist['Title'] for sublist in query_result):
            for sublist in query_result:
                if sublist['Title'].startswith('SYBCTRL'):
                    return(sublist['Title'])
        elif any('IMDB_CLIENT20' in sublist['Title'] for sublist in query_result):
            input_imdb_client = _filename_name_and_version_only[:-2]
            list_imdb_client = []
            for sublist in query_result:
                if sublist['Title'].startswith(input_imdb_client):
                    list_imdb_client.append(sublist['Title'])
            list_imdb_client.sort(reverse=True)
            return(list_imdb_client[0])
        elif any('IMDB_AFL' in sublist['Title'] for sublist in query_result):
            input_imdb_afl = _filename_name_and_version_only[:-1]
            list_imdb_afl = []
            for sublist in query_result:
                if sublist['Title'].startswith(input_imdb_afl):
                    list_imdb_afl.append(sublist['Title'])
            list_imdb_afl.sort(reverse=True)
            return(list_imdb_afl[0])
        elif any('IMDB_LCAPPS' in sublist['Title'] for sublist in query_result):
            input_imdb_lcapps = _filename_name_and_version_only[:-1]
            list_imdb_lcapps = []
            for sublist in query_result:
                if sublist['Title'].startswith(input_imdb_lcapps):
                    list_imdb_lcapps.append(sublist['Title'])
            list_imdb_lcapps.sort(reverse=True)
            return(list_imdb_lcapps[0])
        elif any('IMDB_SERVER' in sublist['Title'] for sublist in query_result):
            for sublist in query_result:
                input_imdb_server = _filename_name_and_version_only[:-1]
                if sublist['Title'].startswith(input_imdb_server):
                    return(sublist['Title'])
        # As SAP WebDisp file name numbering does not use preceeding 0's, manually filter out v7 which is older than v69:
        elif any('SAPWEBDISP' in sublist['Title'] for sublist in query_result):
            input_webdisp = _filename_name_and_version_only[:-2]
            list_webdisp = []
            for sublist in query_result:
                if sublist['Title'].startswith(input_webdisp) and not sublist['Title'].startswith('SAPWEBDISP_SP_7'):
                    list_webdisp.append(sublist['Title'])
            list_webdisp.sort(reverse=True)
            return(list_webdisp[0])
        else:
            raise AnsibleFilterError("\nERROR. More than 1 result, manual intervention required....")
            for item in query_result:
                raise AnsibleFilterError('Identified ' + item['Title'] + ' : ' + item['Description'] + ', ' + item['Infotype'],end='\n')
    else:
        return(query_result[0]['Title'])
