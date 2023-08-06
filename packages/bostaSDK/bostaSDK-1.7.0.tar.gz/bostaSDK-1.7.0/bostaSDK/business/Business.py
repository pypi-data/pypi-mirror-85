import os
import json
import logging

from bostaSDK.apiClient.ApiClient import ApiClient


class BusinessInfo:
    def __init__(self, apiClient):
        """
        Initialize new instance from BusinessInfo class

        Parameters:
        apiClient:  ApiClient

        Returns:
        BusinessInfo: new instance from BusinessInfo

        """
        self.apiClient = apiClient

    def getBusinessSubAccount(self, pageId=0):
        """
        List all business sub accounts

        Parameters:
        pageId (int, optinal): the sequence of pages

        Returns:
        list of all sub accounts
        """
        try:
            logging.info('Get Business Sub Account')
            url = "/businessSubAccount"
            params = {
                "pageId": pageId
            }
            response = self.apiClient.send('get', url, params)
            if (response.status_code != 200):
                return response.text
            return response.json()
        except Exception as exp:
            logging.error(exp)
            raise exp
