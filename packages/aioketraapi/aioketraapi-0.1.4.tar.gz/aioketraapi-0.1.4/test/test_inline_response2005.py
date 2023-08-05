# coding: utf-8

"""
    Ketra Lighting API

    Control your Ketra lights  # noqa: E501

    The version of the OpenAPI document: 1.4.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import aioketraapi
from aioketraapi.models.inline_response2005 import InlineResponse2005  # noqa: E501
from aioketraapi.rest import ApiException

class TestInlineResponse2005(unittest.TestCase):
    """InlineResponse2005 unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test InlineResponse2005
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = aioketraapi.models.inline_response2005.InlineResponse2005()  # noqa: E501
        if include_optional :
            return InlineResponse2005(
                success = True, 
                error = '0', 
                content = [
                    aioketraapi.models.scene.Scene(
                        id = '0', 
                        content_id = 56, 
                        is_show = True, 
                        show_group_number = 56, 
                        name = '0', 
                        parent_group_ids = [
                            '0'
                            ], )
                    ]
            )
        else :
            return InlineResponse2005(
        )

    def testInlineResponse2005(self):
        """Test InlineResponse2005"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
