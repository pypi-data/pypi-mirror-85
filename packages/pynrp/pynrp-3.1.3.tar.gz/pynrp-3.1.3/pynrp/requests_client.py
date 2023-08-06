""" Class which uses requests to do http calls """

import requests


class RequestsClient(object):
    """ Class which uses requests to do http calls """

    def __init__(self, headers):
        """
        :param headers: The headers to use for each request
        """
        self.__headers = headers

    def get(self, url):
        """
        :param url: The url to do a request on
        """
        response = requests.get(url, headers=self.__headers)
        return response.status_code, response.content

    def post(self, url, body):
        """
        :param url: The url to do a post to
        :param body: The content to post to the url
        """
        try:
            typeB = isinstance(body)
        except TypeError:
            typeB = type(body)
        if typeB != dict:
            response = requests.post(url, headers=self.__headers, data=body)
        else:
            response = requests.post(url, headers=self.__headers, json=body)
        return response.status_code, response.content

    def put(self, url, body):
        """
        :param url: The url to do a request to
        :param body: The content to put to
        """
        try:
            typeB = isinstance(body)
        except TypeError:
            typeB = type(body)
        if typeB != dict:
            response = requests.put(url, headers=self.__headers, data=body)
        else:
            response = requests.put(url, headers=self.__headers, json=body)
        return response.status_code, response.content

    def delete(self, url, body):
        """
        :param url: The url to do a request on
        :param body: The content to delete
        """
        response = requests.delete(url, headers=self.__headers, json=body)
        return response.status_code
