

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
            self._id = res["_id"]
            self.pickupAddress = res["pickupAddress"]
            self.dropOffAddress = res["dropOffAddress"]
            self.cod = res["cod"]
            self.receiver = res["receiver"]
            self.state = res["state"]
            self.type = res["type"]
            self.trackingNumber = res["trackingNumber"]
            self.holder = res["holder"]
            self.timeline = res["timeline"]
            self.history = res["history"]
            self.creationTimestamp = res["creationTimestamp"]
        else:
            self.message = str(res)

    def __str__(self):
        return str(self._id) or self.message
