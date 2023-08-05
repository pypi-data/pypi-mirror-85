# coding: utf-8

"""
    Pulp 3 API

    Fetch, Upload, Organize, and Distribute Software Packages  # noqa: E501

    The version of the OpenAPI document: v3
    Contact: pulp-list@redhat.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import pulpcore.client.pulp_container
from pulpcore.client.pulp_container.models.paginatedcontainer_manifest_response_list import PaginatedcontainerManifestResponseList  # noqa: E501
from pulpcore.client.pulp_container.rest import ApiException

class TestPaginatedcontainerManifestResponseList(unittest.TestCase):
    """PaginatedcontainerManifestResponseList unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test PaginatedcontainerManifestResponseList
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = pulpcore.client.pulp_container.models.paginatedcontainer_manifest_response_list.PaginatedcontainerManifestResponseList()  # noqa: E501
        if include_optional :
            return PaginatedcontainerManifestResponseList(
                count = 123, 
                next = 'http://api.example.org/accounts/?offset=400&limit=100', 
                previous = 'http://api.example.org/accounts/?offset=200&limit=100', 
                results = [
                    pulpcore.client.pulp_container.models.container/manifest_response.container.ManifestResponse(
                        pulp_href = '0', 
                        pulp_created = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        artifact = '0', 
                        digest = '0', 
                        schema_version = 56, 
                        media_type = '0', 
                        listed_manifests = [
                            '0'
                            ], 
                        config_blob = '0', 
                        blobs = [
                            '0'
                            ], )
                    ]
            )
        else :
            return PaginatedcontainerManifestResponseList(
        )

    def testPaginatedcontainerManifestResponseList(self):
        """Test PaginatedcontainerManifestResponseList"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
