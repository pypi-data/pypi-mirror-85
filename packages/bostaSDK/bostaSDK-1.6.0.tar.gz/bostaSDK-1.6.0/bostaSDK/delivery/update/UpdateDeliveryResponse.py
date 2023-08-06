
class UpdateDeliveryResponse:

    def __init__(self, jsonPayload):
        """
        Initialize new instance from UpdateDeliveryResponse class

        Parameters:
        jsonResponse (dict): JSON response object

        Returns:
        instance from UpdateDeliveryResponse

        """
        self._id, self.message = self.fromJSONPayload(jsonPayload)

    def fromJSONPayload(self, jsonPayload):
        """
        Extract _id and message fields from json response object

        Parameters:
        jsonResponse (dict): JSON response object

        Returns:
        _id (str): Delivery Id
        message (str): Update delivery response message
        """
        message = jsonPayload["message"]
        _id = jsonPayload["_id"]
        return _id, message

    def __str__(self):
        return self.message
