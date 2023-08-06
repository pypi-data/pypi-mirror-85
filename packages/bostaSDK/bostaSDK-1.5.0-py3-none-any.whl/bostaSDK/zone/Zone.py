class Zone:
    def __init__(self, apiClient):
        self.apiClient = apiClient

    def listAll(self):
        """ List all zones

        Returns: List of available zones
        """
        try:
            headers = {
                "accept": "application/json"
            }
            response = self.apiClient.send(
                'get',
                "/zones",
                headers
            )
            if (response.status_code != 200):
                return response.text
            return response.json()
        except Exception as exp:
            raise exp
