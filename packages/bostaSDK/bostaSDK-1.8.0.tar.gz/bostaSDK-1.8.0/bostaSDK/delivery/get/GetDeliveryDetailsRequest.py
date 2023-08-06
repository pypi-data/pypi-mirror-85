

class GetDeliveryDetailsRequest:
    def __init__(self, deliveryId):
        """ Initialize new instance from GetDeliveryDetailsRequest class

        Parameters:
        deliveryId (str): Delivery id

        Returns: New instance from GetDeliveryDetailsRequest class
        """
        self._id = deliveryId

    def __str__(self):
        return str(self._id)

    def get_deliveryId(self):
        return self._id
