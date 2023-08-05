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

import pulpcore.client.pulp_ansible
from pulpcore.client.pulp_ansible.api.ansible_copy_api import AnsibleCopyApi  # noqa: E501
from pulpcore.client.pulp_ansible.rest import ApiException


class TestAnsibleCopyApi(unittest.TestCase):
    """AnsibleCopyApi unit test stubs"""

    def setUp(self):
        self.api = pulpcore.client.pulp_ansible.api.ansible_copy_api.AnsibleCopyApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_copy_content(self):
        """Test case for copy_content

        Copy content  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
