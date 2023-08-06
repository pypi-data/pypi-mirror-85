

class GetDeliveryDetailsResponse:

    def __init__(self, res):
        """ Initialize new instance from GetDeliveryDetailsResponse class

        Parameters:
        res (dict, str): JSON Response object or response text message

        Returns: New instance from GetDeliveryDetailsResponse class
        """
        self.fromResponseObj(res)

    def fromResponseObj(self, res):
        """
        Extract _id, pickupAddress, dropOffAddress,
        cod, receiver, state, type, creationTimestamp,
        trackingNumber, holder, timeline,
        and history fields from json response object

        Parameters:
        jsonResponse (dict): JSON response object
        """
        if type(res) is dict and res.get('data') is not None:
            self.message = res.get("message")
            data = res["data"]
            self._id = data["_id"]
            self.pickupAddress = data["pickupAddress"]
            self.dropOffAddress = data["dropOffAddress"]
            self.cod = data["cod"]
            self.receiver = data["receiver"]
            self.state = data["state"]
            self.type = data["type"]
            self.trackingNumber = data["trackingNumber"]
            self.holder = data["holder"]
            self.timeline = data["timeline"]
            self.history = data["history"]
            self.creationTimestamp = data["creationTimestamp"]
        else:
            self.message = str(res)

    def __str__(self):
        return self.message
    def get_message(self):
        return self.message
    def get_deliveryId(self):
        return self._id
