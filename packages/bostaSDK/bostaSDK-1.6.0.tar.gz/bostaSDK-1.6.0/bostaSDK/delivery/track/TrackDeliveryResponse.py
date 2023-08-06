

class TrackDeliveryResponse:

    def __init__(self, jsonResponse):
        """ Initialize new instance from TrackDeliveryResponse class

        Parameters:
        jsonResponse (dict): JSON Response object

        Returns: New instance from TrackDeliveryResponse class
        """
        self._id, self.trackingNumber, self.state_history = self.fromJSONResponse(
            jsonResponse)

    def fromJSONResponse(self, jsonResponse):
        """
        Extract message field from json response object

        Parameters:
        jsonResponse (dict): JSON response object

        Returns:
        id (str): Delivery Id
        trackingNumber (str): Delivery tracking number
        state_history (array): List of delivery states
        """
        state_history = []
        for obj in jsonResponse["state-history"]:
            state_history.append({
                "state": obj["state"],
                "time": obj["timestamp"],
                "takenBy": obj["takenBy"]["userName"]
            })
        return jsonResponse["_id"], jsonResponse["trackingNumber"], state_history

    def __str__(self):
        str(self._id)
