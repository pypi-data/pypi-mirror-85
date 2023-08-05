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

import agilicus_api
from agilicus_api.api.policy_api import PolicyApi  # noqa: E501
from agilicus_api.rest import ApiException


class TestPolicyApi(unittest.TestCase):
    """PolicyApi unit test stubs"""

    def setUp(self):
        self.api = agilicus_api.api.policy_api.PolicyApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_get_challenge_decision(self):
        """Test case for get_challenge_decision

        evaluate a policy challenge decision  # noqa: E501
        """
        pass

    def test_get_enrollment_decision(self):
        """Test case for get_enrollment_decision

        evaluate a policy enrollment decision  # noqa: E501
        """
        pass

    def test_map_attributes(self):
        """Test case for map_attributes

        map attributes of a user  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
