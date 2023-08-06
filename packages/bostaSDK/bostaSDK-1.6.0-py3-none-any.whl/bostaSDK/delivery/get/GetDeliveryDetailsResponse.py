

class GetDeliveryDetailsResponse:

    def __init__(self, jsonResponse):
        """ Initialize new instance from GetDeliveryDetailsResponse class

        Parameters:
        jsonResponse (dict): JSON Response object

        Returns: New instance from GetDeliveryDetailsResponse class
        """
        self.fromJSONResponse(jsonResponse)

    def fromJSONResponse(self, jsonResponse):
        """
        Extract _id, pickupAddress, dropOffAddress,
        cod, receiver, state, type, creationTimestamp,
        trackingNumber, holder, timeline,
        and history fields from json response object

        Parameters:
        jsonResponse (dict): JSON response object
        """
        self._id = jsonResponse["_id"]
        self.pickupAddress = jsonResponse["pickupAddress"]
        self.dropOffAddress = jsonResponse["dropOffAddress"]
        self.cod = jsonResponse["cod"]
        self.receiver = jsonResponse["receiver"]
        self.state = jsonResponse["state"]
        self.type = jsonResponse["type"]
        self.trackingNumber = jsonResponse["trackingNumber"]
        self.holder = jsonResponse["holder"]
        self.timeline = jsonResponse["timeline"]
        self.history = jsonResponse["history"]
        self.creationTimestamp = jsonResponse["creationTimestamp"]

    def __str__(self):
        str(self._id)
