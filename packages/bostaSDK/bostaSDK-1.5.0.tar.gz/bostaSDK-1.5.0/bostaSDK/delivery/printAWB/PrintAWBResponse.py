
class PrintAWBResponse:
    def __init__(self, jsonResponse):
        """ Initialize new instance from PrintAWBResponse class

        Parameters:
        jsonResponse (dict): JSON response object

        Returns: instance from PrintAWBResponse

        """
        self.data = self.fromJsonResponse(jsonResponse)

    def fromJsonResponse(self, jsonResponse):
        """
        Extract data field from json response object

        Parameters:
        jsonResponse (dict): JSON response object

        Returns:
        data (str): airway bill data
        """
        return jsonResponse["data"]

    def __str__(self):
        return self.data
