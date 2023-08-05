
import requests
import time
import sys
from requests.auth import HTTPBasicAuth

endpoint = 'https://api.scrapezone.com/scrape'


class ScrapezoneClient:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def scrape(self, payload):
        auth = HTTPBasicAuth(self.username, self.password)
        request = requests.post(endpoint, json=payload, auth=auth)
        response = request.json()

        if request.status_code == 200:
            results = self.getResults(response['job_id'])
            return results

        raise Exception('Request Error')

    def getResults(self, job_id):
        try:
            while True:
                print('Waiting for results..')
                auth = HTTPBasicAuth(self.username, self.password)
                request = requests.get(f'{endpoint}/{job_id}', auth=auth)
                response = request.json()

                if request.status_code == 200:

                    if response['status'] == 'done':
                        data = requests.get(response['parsed_results_json'])
                        return data.json()

                    if response['status'] == 'faulted':
                        return

                    time.sleep(2)
                else:
                    raise Exception('Request Error')

        except:
            print("Unexpected error:", sys.exc_info()[0])
