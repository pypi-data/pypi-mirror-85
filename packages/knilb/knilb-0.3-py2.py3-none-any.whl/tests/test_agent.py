"""Unit tests for knilb.Agent module.

"""
import unittest
import uuid
import responses
import requests

from knilb import agent


class TestRegister(unittest.TestCase):

    def setUp(self):
        self.args = {'user': str(uuid.getnode()),
                     'passkey': '12345',
                     'cloud': 'http://localhost'}
        self.test_agent = agent.Agent(
            self.args['user'], self.args['passkey'], self.args['cloud'])

    def tearDown(self):
        pass

    @responses.activate
    def test_register_already_registered(self):
        responses.add(responses.POST, self.test_agent.url_devices_collection,
                      json=dict(), status=200)
        status = self.test_agent.register()

        self.assertEqual(status, 200)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_register_new_registration(self):
        responses.add(responses.POST, self.test_agent.url_devices_collection,
                      json=dict(), status=201)
        status = self.test_agent.register()

        self.assertEqual(status, 201)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_register_unauthorized(self):
        responses.add(responses.POST, self.test_agent.url_devices_collection,
                      json=dict(), status=401)

        self.assertRaises(requests.exceptions.RequestException,
                          self.test_agent.register)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_register_forbidden(self):
        responses.add(responses.POST, self.test_agent.url_devices_collection,
                      json=dict(), status=403)
        self.assertRaises(requests.exceptions.RequestException,
                          self.test_agent.register)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_register_connection_error(self):
        responses.add(responses.POST, self.test_agent.url_devices_collection,
                      body=requests.exceptions.ConnectionError())
        self.assertRaises(requests.exceptions.RequestException,
                          self.test_agent.register)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_register_invalid_url(self):
        responses.add(responses.POST, self.test_agent.url_devices_collection,
                      body=requests.exceptions.InvalidURL())
        self.assertRaises(requests.exceptions.RequestException,
                          self.test_agent.register)
        self.assertEqual(len(responses.calls), 1)


class TestDownload(unittest.TestCase):

    def setUp(self):
        self.args = {'user': str(uuid.getnode()),
                     'passkey': '12345',
                     'cloud': 'http://localhost'}
        self.test_agent = agent.Agent(
            self.args['user'], self.args['passkey'], self.args['cloud'])

        self.test_cases_from_cloud = {
            u'case-1': u'2018-08-03T12:00:17.790590',
            u'mycase': u'2018-08-03T12:00:17.790590'}        

    def tearDown(self):
        pass

    @responses.activate
    def test_download_happy_path(self):
        responses.add(responses.GET, self.test_agent.url_devices_item,
                      json=self.test_cases_from_cloud, status=200)
        session = requests.Session()
        tests = self.test_agent._download(session)
        self.assertEqual(tests, self.test_cases_from_cloud)

    @responses.activate
    def test_download_invalid_http_auth_raises_HTTPError(self):
        test_status = 400
        responses.add(responses.GET, self.test_agent.url_devices_item,
                      json=self.test_cases_from_cloud, status=test_status)
        session = requests.Session()
        tests = self.test_agent._download(session)
        self.assertFalse(bool(tests))
        
    @responses.activate
    def test_download_cloud_returns_no_test_cases_in_HTTP_body(self):
        test_body = ''
        responses.add(responses.GET, self.test_agent.url_devices_item,
                      body=test_body, status=200)
        session = requests.Session()
        tests = self.test_agent._download(session)
        self.assertFalse(bool(tests))
