import logging

import requests


logger = logging.getLogger(__name__)


class ApiBling(object):
    """A Python API Wrapper for Bling ERP."""

    def __init__(self, api_key):
        """
        Parameters:
        -----------
            api_key (str):
                Your api key
        """

        self.api_key = api_key
        self.root_uri = 'https://bling.com.br/Api/v2'
        self.session = requests.Session()

    def _make_request(self, method, uri, params=None, data=None):
        logger.info('method = {}'.format(method))
        logger.info('uri = {}'.format(uri))
        logger.info('params = {}'.format(params))
        logger.info('data = {}'.format(data))
        url = '{}{}/json/?apikey={}'.format(self.root_uri, uri, self.api_key)
        logger.info('url = {}'.format(url))
        try:
            resp = self.session.request(method, url, data=data, params=params)
            logger.debug(resp)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.HTTPError as e:
            raise ApiError(e.request, e.response)
        except requests.exceptions.RequestException as e:
            raise ApiError(e.request)


class ApiError(Exception):
    def __init__(self, request, response=None):
        self.request = request
        self.response = response
