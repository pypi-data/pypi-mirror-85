class City:
    def __init__(self, apiClient):
        self.apiClient = apiClient

    def listAll(self):
        """ List all citites

        Returns: List of available cities
        """
        try:
            headers = {
                "accept": "application/json"
            }
            response = self.apiClient.send(
                'get',
                "/cities",
                headers
            )
            if (response.status_code != 200):
                return response.text
            return response.json()
        except Exception as exp:
            raise exp
