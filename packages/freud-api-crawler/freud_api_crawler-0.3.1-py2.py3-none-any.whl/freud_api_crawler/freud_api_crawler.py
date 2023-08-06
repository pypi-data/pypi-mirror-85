import os
import time
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

    def crawl_endpoint(self, url_part, important_values):
        """ method for iterating over drupal-endpoints
        :param url_part: specific API endpoint, e.g. 'werk' -> {drupalbase}/jsonapi/node/{url_part}
        :type gnd_id: str
        :param important_values: simple attribute names, e.g. ['title', 'field_year']
        :type user: list

        :return: print things
        """

        url = f"{self.endpoint}node/{url_part}?page[limit]={self.page_size}"
        next_page = True
        counter = 0
        auth = ()
        while next_page:
            print(url)
            response = requests.get(url, auth=(self.user, self.pw))
            result = response.json()
            links = result['links']
            for y in result['data']:
                self_uri = y['links']['self']['href']
                print(self_uri)
                attributes = y['attributes']
                for val in important_values:
                    print(attributes[val])
            if links.get('next', False):
                url = links['next']['href']
            else:
                next_page = False
            counter += 1
            print(counter)
            if self.limit > 0:
                if counter >= self.limit:
                    next_page = False
            time.sleep(self.sleep)

    def __init__(
        self,
        endpoint=FRD_API,
        user=FRD_USER,
        pw=FRD_PW,
        page_size=10,
        limit=10,
        sleep=0.5
    ):

        """ initializes the class

        :param endpoint: The API Endpoint
        :type gnd_id: str
        :param user: The API user name
        :type user: str
        :param pw: The user's password
        :type pw: str
        :param page_size: Default page size of api-return -> &page[limit]={self.limit}
        :type pw: int
        :param limit: After how many next-loads the loop should stop
        :type pw: int
        :param sleep: Time to pause crawling loop
        :type pw: float

        :return: A FrdClient instance
        """
        super().__init__()
        self.endpoint = endpoint
        self.user = user
        self.pw = pw
        self.page_size = page_size
        self.limit = limit
        self.sleep = sleep
        if self.pw and self.user:
            self.authenticated = True
        else:
            print("no user and password set")
            self.authenticated = False


class FrdManifestation(FrdClient):

    """class to deal with Manifestations
    :param manifestation_id: The hash ID of a Manifestation Node
    :type gnd_id: str

    :return: A FrdClient instance
    """

    def __init__(
        self,
        manifestation_id=None
    ):
        super().__init__()
        self.manifestation_id = manifestation_id
