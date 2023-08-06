import os
import pandas as pd
import requests

from typing import Iterator


class DrsClient:
    """
    DRS client for DNAstack's DRS API's.

    :param base_url: Base url to search on

    :Example:
        from search_python_client.search import DrsClient\n
        base_url = 'https://drs.covidcloud.ca/ga4gh/drs/v1/'\n
        drs_client = DrsClient(base_url=base_url)

    """

    def __init__(self, base_url: str):
        self.base_url = base_url

    def __str__(self):
        return f'DrsClient(base_url={self.base_url})'

    def __repr__(self):
        return f'DrsClient(base_url={self.base_url})'

    def _get(self, url: str) -> dict:
        """
        Executes get request and returns dict formatted json response

        :param url: Url to search on
        :returns: dict formatted json response
        :raises HTTPError: If response != 200

        """
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def get_object_info(self, object_id: str) -> pd.DataFrame:
        """
        List all info associated with object.

        :param object_info: Object id of choice
        :returns: Dataframe formatted responses
        :raises HTTPError: If response != 200

        """
        return pd.DataFrame(
            self._get(os.path.join(self.base_url, 'objects', object_id))
        )


class SearchClient:
    """
    Search client for DNAstack's search API's.

    :param base_url: Base url to search on

    :Example:
        from search_python_client.search import SearchClient\n
        base_url = 'https://ga4gh-search-adapter-presto-covid19-public.prod.dnastack.com/'\n
        search_client = SearchClient(base_url=base_url)

    """

    def __init__(self, base_url: str):
        self.base_url = base_url

    def __str__(self):
        return f'SearchClient(base_url={self.base_url})'

    def __repr__(self):
        return f'SearchClient(base_url={self.base_url})'

    def _get(self, url: str) -> dict:
        """
        Executes get request and returns dict formatted json response

        :param url: Url to search on
        :returns: dict formatted json response
        :raises HTTPError: If response != 200

        """
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def _get_paginated(self, url: str) -> Iterator:
        """
        Executes get request for paginated responses

        :param url: Url to search on
        :returns: List of dict formatted json responses
        :raises HTTPError: If response != 200

        """
        basename = os.path.basename(url)
        json_response = self._get(url)
        while True:
            try:
                json_response = self._get(
                    json_response['pagination']['next_page_url']
                )
            except KeyError:
                break
            if json_response[basename]:
                for row in json_response[basename]:
                    yield row

    def _post(self, url: str, json: dict) -> dict:
        """
        Executes post request and returns dict formatted json response

        :param url: Url to search on
        :param json:  Dict formatted json query
        :returns: dict formatted json response
        :raises HTTPError: If response != 200

        """
        response = requests.post(url, json={'query': json})
        response.raise_for_status()
        return response.json()

    def _post_paginated(self, url, json) -> Iterator:
        """
        Executes post request for paginated responses

        :param url: Url to search on
        :param json:  Dict formatted json query
        :returns: List of dict formmated json responses
        :raises HTTPError: If response != 200

        """
        json_response = self._post(url, json=json)
        while True:
            try:
                json_response = self._get(
                    json_response['pagination']['next_page_url']
                )
            except KeyError:
                break
            if json_response['data']:
                for row in json_response['data']:
                    yield row

    def get_table_list(self) -> Iterator:
        """
        List all tables associated with the url.

        :returns: Dataframe formatted responses
        :raises HTTPError: If response != 200

        """
        return self._get_paginated(
            os.path.join(self.base_url, 'tables')
        )

    def get_table_info(self, table_name: str) -> pd.DataFrame:
        """
        get all info associated with table_name.

        :param table_name: Table name of choice
        :returns: Dataframe formatted responses
        :raises HTTPError: If response != 200

        """
        return pd.DataFrame(
            self._get(os.path.join(self.base_url, 'table', table_name, 'info'))
        )

    def get_table_data(self, table_name: str) -> Iterator:
        """
        Get all data associated with table_name.

        :param table_name: Table name of choice
        :returns: Dataframe formatted responses
        :raises HTTPError: If response != 200

        """
        return self._get_paginated(
            os.path.join(self.base_url, 'table', table_name, 'data')
        )

    def search_table(self, query: str) -> Iterator:
        """
        Executes an SQL query on table of choice and returns associated data.

        :param table_name: Table name of choice
        :returns: Dataframe formatted responses
        :raises HTTPError: If response != 200

        :Example: query = 'SELECT * FROM coronavirus_dnastack_curated.covid_cloud_production.sequences_view LIMIT 1000'

        """
        return self._post_paginated(
                os.path.join(self.base_url, 'search'), query
        )
