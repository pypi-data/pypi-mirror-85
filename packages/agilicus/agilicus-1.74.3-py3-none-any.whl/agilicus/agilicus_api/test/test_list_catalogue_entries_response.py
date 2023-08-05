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
from agilicus_api.models.list_catalogue_entries_response import ListCatalogueEntriesResponse  # noqa: E501
from agilicus_api.rest import ApiException

class TestListCatalogueEntriesResponse(unittest.TestCase):
    """ListCatalogueEntriesResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test ListCatalogueEntriesResponse
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = agilicus_api.models.list_catalogue_entries_response.ListCatalogueEntriesResponse()  # noqa: E501
        if include_optional :
            return ListCatalogueEntriesResponse(
                catalogue_entries = [
                    agilicus_api.models.catalogue_entry.CatalogueEntry(
                        id = '123', 
                        catalogue_id = '123', 
                        catalogue_category = '0', 
                        name = 'dotnet_core', 
                        content = 'cr.agilicus.com/dotnet_core/app-image:latest', 
                        tag = 'V1.1', 
                        short_description = '0', 
                        long_description = '0', 
                        created = '2015-07-07T15:49:51.230+02:00', 
                        updated = '2015-07-07T15:49:51.230+02:00', )
                    ], 
                limit = 56
            )
        else :
            return ListCatalogueEntriesResponse(
                limit = 56,
        )

    def testListCatalogueEntriesResponse(self):
        """Test ListCatalogueEntriesResponse"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
