import os
from collections import defaultdict

import requests

FRD_API = os.environ.get('FRD_API', 'https://www.freud-edition.net/jsonapi/')
FRD_USER = os.environ.get('FRD_USER', False)
FRD_PW = os.environ.get('FRD_PW', False)


class FrdClient():

    """Main Class to interact with freud.net-API """

    def list_endpoints(self):
        """ returns a list of existing API-Endpoints
        :return: A PyLobidPerson instance
        """
        if self.authenticated:
            r = requests.get(
                self.endpoint, auth=(self.user, self.pw)
            )
            result = r.json()
            d = defaultdict(list)
            for key, value in result['links'].items():
                url = value['href']
                node_type = url.split('/')[-2]
                d[node_type].append(url)
            return d
        else:
            return {}

        return r.json()

    def __init__(self, endpoint=FRD_API, user=FRD_USER, pw=FRD_PW):

        """ initializes the class

        :param endpoint: The API Endpoint
        :type gnd_id: str
        :param user: The API user name
        :type user: str
        :param pw: The user's password
        :type pw: str

        :return: A FrdClient instance
        """
        super().__init__()
        self.endpoint = endpoint
        self.user = user
        self.pw = pw
        if self.pw and self.user:
            self.authenticated = True
        else:
            print("no user and password set")
            self.authenticated = False
