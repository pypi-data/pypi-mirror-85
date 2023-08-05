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
from agilicus_api.models.mfa_enrollment_question_login_info import MFAEnrollmentQuestionLoginInfo  # noqa: E501
from agilicus_api.rest import ApiException

class TestMFAEnrollmentQuestionLoginInfo(unittest.TestCase):
    """MFAEnrollmentQuestionLoginInfo unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test MFAEnrollmentQuestionLoginInfo
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = agilicus_api.models.mfa_enrollment_question_login_info.MFAEnrollmentQuestionLoginInfo()  # noqa: E501
        if include_optional :
            return MFAEnrollmentQuestionLoginInfo(
                issuer_org_id = 'absjfladasdf23', 
                enrollment_expiry = '2015-07-07T15:49:51.230+02:00', 
                user_mfa_methods = ["totp","webauthn"]
            )
        else :
            return MFAEnrollmentQuestionLoginInfo(
                issuer_org_id = 'absjfladasdf23',
                enrollment_expiry = '2015-07-07T15:49:51.230+02:00',
                user_mfa_methods = ["totp","webauthn"],
        )

    def testMFAEnrollmentQuestionLoginInfo(self):
        """Test MFAEnrollmentQuestionLoginInfo"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
