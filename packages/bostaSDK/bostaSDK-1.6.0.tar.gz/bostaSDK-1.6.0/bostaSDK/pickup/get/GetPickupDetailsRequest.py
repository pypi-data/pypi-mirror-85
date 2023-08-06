

class GetPickupDetailsRequest:
    def __init__(self, pickupId):
        """ Initialize new instance from GetPickupDetailsRequest class

        Parameters:
        pickupId (str): Pickup Id

        Returns: instance from GetPickupDetailsRequest

        """
        self._id = pickupId

    def get_pickupId(self):
        return self._id

    def __str__(self):
        return str(self._id)
