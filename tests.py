from unittest import TestCase, IsolatedAsyncioTestCase

import setup


class TestSetup(TestCase):

    def setUp(self):
        input_content = '''{
  "keywords": [
    "openstack",
    "nova",
    "css"
  ],
  "proxies": [
    "194.126.37.94:8080",
    "13.78.125.167:8080"
  ],
  "type": "Repositories"
}'''
        with open('input.json', 'w') as input_file:
            input_file.write(input_content)

    def test_read_input_file(self):
        input_content = setup.read_input_file()
        self.assertTrue(len(input_content) == 3)

    def test_write_output_file(self):
        output_content = 'TEST'
        setup.write_output_file(output_content)
        with open('output.json') as output_file:
            self.assertTrue(output_file.readlines()[0] == output_content)

    def test_request_url_and_parse_to_xml(self):
        xml = setup.request_url_and_parse_to_xml('https://github.com', None)
        self.assertIsNotNone(xml)

    def test_get_proxy_map(self):
        proxy_map = setup.get_proxy_map(['194.126.37.94:8080'])
        self.assertIn('https://194.126.37.94:8080', proxy_map.get('https'))

    def test_create_result_node(self):
        url = 'https://github.com/torvalds/linux'
        owner = 'torvalds'
        language_stats = {'c': '98.4%'}
        result = setup.create_result_node(url, owner, language_stats)
        self.assertIsNotNone(result)
        self.assertTrue(url, result.get('url'))
        self.assertIsNotNone(result.get('extra'))
        self.assertTrue(owner, result.get('extra').get('owner'))
        self.assertTrue(language_stats, result.get('extra').get('language_stats'))


class TestAsyncio(IsolatedAsyncioTestCase):

    async def test_extract_data(self):
        url = 'https://github.com/angular/angular'
        owner = 'Angular'
        result = await setup.extract_data(url, owner, None)
        print(result)
        self.assertIsNotNone(result)
        self.assertTrue(url, result.get('url'))
