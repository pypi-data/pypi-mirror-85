

class PrintAWBRequest:
    def __init__(self, deliveryId):
        """ Initialize new instance from PrintAWBRequest class

        Parameters:
        deliveryId (str): Delivery Id

        Returns: instance from PrintAWBRequest

        """
        self._id = deliveryId

    def __str__(self):
        return str(self._id)

    def get_deliveryId(self):
        return self._id
