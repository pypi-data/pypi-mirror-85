

class DeletePickupResonse:
    def __init__(self, jsonResponse):
        """
        Initialize new instance from DeletePickupResonse class

        Parameters:
        jsonResponse (dict): JSON response object

        Returns:
        instance from DeletePickupResonse

        """
        self.message = self.fromJsonResponse(jsonResponse)

    def fromJsonResponse(self, jsonResponse):
        """
        Extract message field from json response object

        Parameters:
        jsonResponse (dict): JSON response object

        Returns: Delete pickup response message

        """
        return jsonResponse["message"]

    def __str__(self):
        self.message
