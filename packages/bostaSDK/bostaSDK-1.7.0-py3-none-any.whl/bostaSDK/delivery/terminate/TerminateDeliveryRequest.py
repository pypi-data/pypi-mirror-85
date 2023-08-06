

class TerminateDeliveryRequest:
    def __init__(self, deliveryId):
        """ Initialize new instance from TerminateDeliveryRequest class

        Parameters:
        deliveryId (str): Delivery Id

        Returns: New instance from TerminateDeliveryRequest class
        """
        self._id = deliveryId

    def get_deliveryId(self):
        return self._id

    def __str__(self): return self._id
