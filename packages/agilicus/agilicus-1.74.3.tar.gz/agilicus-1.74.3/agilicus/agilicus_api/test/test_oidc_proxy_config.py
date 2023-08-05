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
from agilicus_api.models.oidc_proxy_config import OIDCProxyConfig  # noqa: E501
from agilicus_api.rest import ApiException

class TestOIDCProxyConfig(unittest.TestCase):
    """OIDCProxyConfig unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test OIDCProxyConfig
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = agilicus_api.models.oidc_proxy_config.OIDCProxyConfig()  # noqa: E501
        if include_optional :
            return OIDCProxyConfig(
                headers = agilicus_api.models.oidc_proxy_header.OIDCProxyHeader(
                    domain_substitution = agilicus_api.models.oidc_proxy_domain_substitution.OIDCProxyDomainSubstitution(
                        standard_headers = agilicus_api.models.oidc_proxy_standard_header.OIDCProxyStandardHeader(
                            location = True, 
                            origin = True, 
                            host = True, ), 
                        other_headers = [
                            agilicus_api.models.oidc_proxy_header_mapping.OIDCProxyHeaderMapping(
                                name = 'Accept-Encoding', 
                                value = '*', )
                            ], ), 
                    header_overrides = agilicus_api.models.oidc_proxy_header_override.OIDCProxyHeaderOverride(
                        request = agilicus_api.models.oidc_proxy_header_user_config.OIDCProxyHeaderUserConfig(
                            set = [
                                agilicus_api.models.oidc_proxy_header_mapping.OIDCProxyHeaderMapping(
                                    name = 'Accept-Encoding', 
                                    value = '*', )
                                ], 
                            add = [
                                agilicus_api.models.oidc_proxy_header_mapping.OIDCProxyHeaderMapping(
                                    name = 'Accept-Encoding', 
                                    value = '*', )
                                ], 
                            remove = [
                                agilicus_api.models.oidc_proxy_header_name.OIDCProxyHeaderName(
                                    name = '0', )
                                ], ), 
                        response = agilicus_api.models.oidc_proxy_header_user_config.OIDCProxyHeaderUserConfig(), ), ), 
                domain_mapping = agilicus_api.models.oidc_proxy_domain_mapping.OIDCProxyDomainMapping(
                    primary_external_name = 'app-1.cloud.egov.city', 
                    primary_internal_name = 'app-1.internal', 
                    other_mappings = [
                        agilicus_api.models.oidc_proxy_domain_name_mapping.OIDCProxyDomainNameMapping(
                            internal_name = 'local_test_app', 
                            external_name = 'app-1', )
                        ], ), 
                auth = agilicus_api.models.oidc_auth_config.OIDCAuthConfig(
                    auth_enabled = True, 
                    client_id = 'admin-portal', 
                    issuer = 'https://auth.cloud.egov.city', 
                    logout_url = '/login/logout.cfm', 
                    scopes = [
                        agilicus_api.models.oidc_proxy_scope.OIDCProxyScope(
                            name = 'urn:agilicus:app:app-1:owner', )
                        ], ), 
                content_manipulation = agilicus_api.models.oidc_proxy_content_manipulation.OIDCProxyContentManipulation(
                    media_types = [
                        agilicus_api.models.oidc_content_type.OIDCContentType(
                            name = 'text/css', )
                        ], )
            )
        else :
            return OIDCProxyConfig(
                headers = agilicus_api.models.oidc_proxy_header.OIDCProxyHeader(
                    domain_substitution = agilicus_api.models.oidc_proxy_domain_substitution.OIDCProxyDomainSubstitution(
                        standard_headers = agilicus_api.models.oidc_proxy_standard_header.OIDCProxyStandardHeader(
                            location = True, 
                            origin = True, 
                            host = True, ), 
                        other_headers = [
                            agilicus_api.models.oidc_proxy_header_mapping.OIDCProxyHeaderMapping(
                                name = 'Accept-Encoding', 
                                value = '*', )
                            ], ), 
                    header_overrides = agilicus_api.models.oidc_proxy_header_override.OIDCProxyHeaderOverride(
                        request = agilicus_api.models.oidc_proxy_header_user_config.OIDCProxyHeaderUserConfig(
                            set = [
                                agilicus_api.models.oidc_proxy_header_mapping.OIDCProxyHeaderMapping(
                                    name = 'Accept-Encoding', 
                                    value = '*', )
                                ], 
                            add = [
                                agilicus_api.models.oidc_proxy_header_mapping.OIDCProxyHeaderMapping(
                                    name = 'Accept-Encoding', 
                                    value = '*', )
                                ], 
                            remove = [
                                agilicus_api.models.oidc_proxy_header_name.OIDCProxyHeaderName(
                                    name = '0', )
                                ], ), 
                        response = agilicus_api.models.oidc_proxy_header_user_config.OIDCProxyHeaderUserConfig(), ), ),
                domain_mapping = agilicus_api.models.oidc_proxy_domain_mapping.OIDCProxyDomainMapping(
                    primary_external_name = 'app-1.cloud.egov.city', 
                    primary_internal_name = 'app-1.internal', 
                    other_mappings = [
                        agilicus_api.models.oidc_proxy_domain_name_mapping.OIDCProxyDomainNameMapping(
                            internal_name = 'local_test_app', 
                            external_name = 'app-1', )
                        ], ),
                content_manipulation = agilicus_api.models.oidc_proxy_content_manipulation.OIDCProxyContentManipulation(
                    media_types = [
                        agilicus_api.models.oidc_content_type.OIDCContentType(
                            name = 'text/css', )
                        ], ),
        )

    def testOIDCProxyConfig(self):
        """Test OIDCProxyConfig"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
