import base64
import requests
import json
import io
import sqlmorph_api
import sys
from contextlib import redirect_stdout
import unittest
import os

class TestClass(unittest.TestCase):

    def get_access_token(self):
        url = "https://account.phdata.io/oauth2/ausaxr6ifFEPr3KPY4x6/v1/token"
        client_id = "0oaqmyesrCGbkfnIA4x6"
        client_secret = os.environ['OKTA_CLIENT_SECRET']
        encoded = ("%s:%s" % (client_id, client_secret)).encode('utf-8')
        auth_header = "Basic " + base64.standard_b64encode(encoded).decode('utf-8')
        data = {'grant_type': 'client_credentials'}

        headers = {
            "Authorization": auth_header,
            "Content-Type": "application/x-www-form-urlencoded",
        }

        response = requests.post(url, data=data, headers=headers)
        return response.json().get('access_token')

    def test_shouldPrintToStdoutWhenPassedAFile(self):
        token = self.get_access_token()
        myArgs = [
            '--source', 'impala',
            '--target', 'snowflake',
            '--auth-token', token,
            '--input', './cli/test/statement.sql'
        ]
        output = io.StringIO()
        with redirect_stdout(output):
            sqlmorph_api.runner(myArgs)
        self.assertTrue(output.getvalue())

    def test_shouldCreateDirectoryWithTranslationsWhenPassedDirectory(self):
        token = self.get_access_token()
        target = 'snowflake'
        path = './cli/test'
        myArgs = [
            '--source', 'impala',
            '--target', target,
            '--auth-token', token,
            '--input', path
        ]
        output = io.StringIO()
        with redirect_stdout(output):
            sqlmorph_api.runner(myArgs)
        # We don't expect to get something to stdout in this case
        self.assertFalse(output.getvalue())

        totalSourceFiles = 0
        for root, dirs, files in os.walk(path):
            for file in files:
                totalSourceFiles += 1
        totalTargetFiles = 0
        for root, dirs, files in os.walk("%s.%s" % (path, target)):
            for file in files:
                fileContents = sqlmorph_api.readFile(os.path.join(root, file))
                self.assertTrue(fileContents.get("contents"))
                totalTargetFiles += 1
        self.assertEqual(totalSourceFiles, totalTargetFiles)

if __name__ == '__main__':
    unittest.main()
