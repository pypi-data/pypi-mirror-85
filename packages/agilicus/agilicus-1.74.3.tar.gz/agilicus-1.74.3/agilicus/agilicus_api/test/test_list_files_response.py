# coding: utf-8

"""
    Agilicus API

    Agilicus API endpoints  # noqa: E501

    The version of the OpenAPI document: 2020.11.06
    Contact: dev@agilicus.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import agilicus_api
from agilicus_api.models.list_files_response import ListFilesResponse  # noqa: E501
from agilicus_api.rest import ApiException

class TestListFilesResponse(unittest.TestCase):
    """ListFilesResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test ListFilesResponse
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = agilicus_api.models.list_files_response.ListFilesResponse()  # noqa: E501
        if include_optional :
            return ListFilesResponse(
                files = [
                    agilicus_api.models.file_summary.FileSummary(
                        id = '123', 
                        name = 'Alice', 
                        tag = 'theme', 
                        label = '0', 
                        size = 56, 
                        visibility = 'private', 
                        public_url = 'https://storage.googleapis.com/agilicus/www/2019/03/446a356a-agilicus-logo-horizontal.svg', 
                        storage_path = '0', 
                        last_accessed = '2015-07-07T15:49:51.230+02:00', 
                        created = '2015-07-07T15:49:51.230+02:00', 
                        updated = '2015-07-07T15:49:51.230+02:00', )
                    ], 
                limit = 56
            )
        else :
            return ListFilesResponse(
                limit = 56,
        )

    def testListFilesResponse(self):
        """Test ListFilesResponse"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
