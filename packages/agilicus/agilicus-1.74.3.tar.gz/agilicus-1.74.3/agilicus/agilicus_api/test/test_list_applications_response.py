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
from agilicus_api.models.list_applications_response import ListApplicationsResponse  # noqa: E501
from agilicus_api.rest import ApiException

class TestListApplicationsResponse(unittest.TestCase):
    """ListApplicationsResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test ListApplicationsResponse
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = agilicus_api.models.list_applications_response.ListApplicationsResponse()  # noqa: E501
        if include_optional :
            return ListApplicationsResponse(
                applications = [
                    agilicus_api.models.application.Application(
                        created = '2015-07-07T15:49:51.230+02:00', 
                        id = '123', 
                        name = 'a', 
                        description = '0', 
                        category = '0', 
                        image = '0', 
                        image_username = '0', 
                        image_password = '0', 
                        image_credentials_type = 'basic_auth', 
                        environments = [
                            agilicus_api.models.environment.Environment(
                                created = '2015-07-07T15:49:51.230+02:00', 
                                name = '0', 
                                maintenance_org_id = '0', 
                                version_tag = '0', 
                                config_mount_path = '0', 
                                config_as_mount = '0', 
                                config_as_env = '0', 
                                secrets_mount_path = '0', 
                                secrets_as_mount = '0', 
                                secrets_as_env = '0', 
                                application_services = [
                                    agilicus_api.models.application_service.ApplicationService(
                                        id = '123', 
                                        name = '0', 
                                        org_id = '0', 
                                        hostname = 'db.example.com', 
                                        ipv4_addresses = [
                                            '192.0.2.1'
                                            ], 
                                        name_resolution = 'static', 
                                        port = 56, 
                                        protocol = 'tcp', 
                                        assignments = [
                                            agilicus_api.models.application_service_assignment.ApplicationServiceAssignment(
                                                app_id = '0', 
                                                environment_name = '0', 
                                                org_id = '0', )
                                            ], 
                                        updated = '2015-07-07T15:49:51.230+02:00', 
                                        service_type = 'vpn', )
                                    ], 
                                serverless_image = '0', 
                                status = agilicus_api.models.environment_status.EnvironmentStatus(
                                    runtime_status = agilicus_api.models.runtime_status.RuntimeStatus(
                                        overall_status = 'good', 
                                        running_replicas = 2, 
                                        error_message = 'CrashLoopBackoff', 
                                        restarts = 5, 
                                        cpu = 0.6, 
                                        memory = 45.2, 
                                        last_apply_time = '2020-06-19T15:35:08Z', 
                                        running_image = 'cr.agilicus.com/applications/iomad:v1.13.0', 
                                        running_hash = 'sha256:2fb759c1adfe40863b89a4076111af8f210e7342d2240f09b08fc445b357112e', 
                                        org_id = '123', ), ), 
                                updated = '2015-07-07T15:49:51.230+02:00', 
                                application_configs = agilicus_api.models.application_config.ApplicationConfig(
                                    oidc_config = agilicus_api.models.oidc_proxy_config.OIDCProxyConfig(
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
                                                ], ), ), ), )
                            ], 
                        org_id = '0', 
                        contact_email = '0', 
                        monitoring_config = agilicus_api.models.application_monitoring_config.ApplicationMonitoringConfig(
                            port = 1, 
                            path = '/metrics', ), 
                        port = 56, 
                        healthcheck_uri = '0', 
                        roles = [
                            agilicus_api.models.role.Role(
                                name = '0', 
                                rules = [
                                    agilicus_api.models.rule.Rule(
                                        host = '0', 
                                        name = 'rules.add', 
                                        method = 'get', 
                                        path = '/.*', 
                                        query_parameters = [
                                            agilicus_api.models.rule_query_parameter.RuleQueryParameter(
                                                name = '0', 
                                                exact_match = '0', )
                                            ], 
                                        body = agilicus_api.models.rule_query_body.RuleQueryBody(
                                            json = [
                                                agilicus_api.models.rule_query_body_json.RuleQueryBodyJSON(
                                                    name = '0', 
                                                    exact_match = '0', 
                                                    match_type = 'string', 
                                                    pointer = '/foo/0/a~1b/2', )
                                                ], ), )
                                    ], )
                            ], 
                        definitions = [
                            agilicus_api.models.definition.Definition(
                                key = '0', 
                                value = '0', )
                            ], 
                        assignments = [
                            agilicus_api.models.application_assignment.ApplicationAssignment(
                                id = '0', 
                                org_id = 'asd901laskbh', 
                                environment_name = 'production', 
                                application_name = 'Blogs', )
                            ], 
                        owned = True, 
                        maintained = True, 
                        assigned = True, 
                        published = 'no', 
                        default_role_id = 'AcaSL40fs22l4Dr4XoAd5y', 
                        default_role_name = 'owner', 
                        icon_url = '0', 
                        updated = '2015-07-07T15:49:51.230+02:00', 
                        location = 'hosted', )
                    ]
            )
        else :
            return ListApplicationsResponse(
        )

    def testListApplicationsResponse(self):
        """Test ListApplicationsResponse"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
