
class TerminateDeliveryResponse:

    def __init__(self, jsonResponse):
        """ Initialize new instance from TerminateDeliveryResponse class

        Parameters:
        jsonResponse (dict): JSON Response object

        Returns: New instance from TerminateDeliveryResponse class
        """
        self.message = self.fromJsonRespose(jsonResponse)

    def fromJsonRespose(self, jsonResponse):
        """
        Extract message field from json response object

        Parameters:
        jsonResponse (dict): JSON response object

        Returns:
        message (str): Termination delivery response message
        """
        return jsonResponse['message']

    def __str__(self):
        return self.message
