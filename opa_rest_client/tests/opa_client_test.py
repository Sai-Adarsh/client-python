#! /usr/bin/python3
"""
Test Suit for AppGuard GitHub Integration
"""
import json
import unittest
import docker
import sys

from magen_utils_apis.compare_utils import compare_dicts

from opa_rest_client.opa_client_apis import create_opa_policy, create_base_doc, delete_base_doc, get_base_doc, \
    delete_all_base_data_doc, delete_all_policies, delete_policy
from opa_rest_client.opa_docker_apis import run_opa_docker_container
from opa_rest_client.tests.opa_client_test_messages import EXAMPLE_DATA, EXAMPLE_POLICY, OPA_EMPTY_RESP

__author__ = "Reinaldo Penno"
__license__ = "Apache"
__version__ = "0.1"
__email__ = "rapenno@gmail.com"


class TestOpaClient(unittest.TestCase):

    docker_client = client = docker.from_env()
    opa_container = None
    base_doc_url = "http://localhost:8181/v1/data"
    base_policies_url = "http://localhost:8181/v1/policies"

    @classmethod
    def setUpClass(cls):
        try:
            # Start opa container
            cls.opa_container = run_opa_docker_container(cls.docker_client)
            assert cls.opa_container is not None

        except BaseException as e:
            print("Unexpected error:", sys.exc_info()[0])
            raise ValueError("Unexpected error") from e

    @classmethod
    def tearDownClass(cls):
        if cls.opa_container is not None:
            cls.opa_container.stop()

    def setUp(self):
        """
        This function prepares the system for running tests
        """
        pass

    def tearDown(self):
        pass

    def test_create_policy(self):
        pass

    def clean_base_doc(self):
        success, message = delete_base_doc(type(self).base_doc_url + "/networks")
        self.assertTrue(success)
        success, message = delete_base_doc(type(self).base_doc_url + "/ports")
        self.assertTrue(success)
        success, message = delete_base_doc(type(self).base_doc_url + "/servers")
        self.assertTrue(success)
        resp = get_base_doc(type(self).base_doc_url)
        self.assertTrue(resp.success)
        expected_resp = json.loads(OPA_EMPTY_RESP)
        success = compare_dicts(resp.json_body, expected_resp)
        self.assertTrue(success)

    def test_create_data_doc(self):
        success, message = create_base_doc(type(self).base_doc_url, EXAMPLE_DATA)
        self.assertTrue(success)
        self.clean_base_doc()

    def test_create_data_and_policy(self):
        success, message = create_base_doc(type(self).base_doc_url, EXAMPLE_DATA)
        self.assertTrue(success)
        success, message = create_opa_policy(type(self).base_policies_url + "/example1", EXAMPLE_POLICY.encode("utf-8"))
        self.assertTrue(success)
        success, message = delete_policy(type(self).base_policies_url + "/example1")
        self.assertTrue(success)
        self.clean_base_doc()



