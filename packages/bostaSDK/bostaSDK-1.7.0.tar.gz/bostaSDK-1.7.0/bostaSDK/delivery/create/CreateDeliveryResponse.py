

class CreateDeliveryResponse:
    def __init__(self, res):
        """
        Initialize new instance from CreateDeliveryResponse class

        Parameters:
        res (dict): JSON response object or response text message

        Returns:
        instance from CreateDeliveryResponse

        """
        self.fromResponseObj(res)

    def fromResponseObj(self, res):
        """
        Extract _id, trackingNumber and message fields from json response object

        Parameters:
        res (dict): JSON response object or response text message

        Returns:
        _id (str): Delivery Id
        trackingNumber (str): Delivery trackingNumber
        message (str): Create delivery response message
        """
        if type(res) is dict and res.get('data') is not None:
            self._id = res["data"]["_id"]
            self.trackingNumber = res["data"]["trackingNumber"]
            self.message = res["data"]["message"]
        else:
            self.message = str(res)
            self._id = self.trackingNumber = None


    def get_deliveryId(self):
        return self._id

    def get_trackingNumber(self):
        return self.trackingNumber

    def get_message(self):
        return self.message

    def __str__(self):
        return self.message
