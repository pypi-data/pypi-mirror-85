

class UpdatePickupResponse:
    def __init__(self, jsonResponse):
        """
        Initialize new instance from UpdatePickupResponse class

        Parameters:
        jsonResponse (dict): JSON response object

        Returns:
        instance from UpdatePickupResponse

        """
        self.message = self.fromJSONResponse(jsonResponse)

    def fromJSONResponse(self, jsonResponse):
        """
        Extract message field from json response object

        Parameters:
        jsonResponse (dict): JSON response object

        Returns:
        message (str): Update Pickup response message
        """
        return jsonResponse["message"]

    def __str__(self):
        return self.message
