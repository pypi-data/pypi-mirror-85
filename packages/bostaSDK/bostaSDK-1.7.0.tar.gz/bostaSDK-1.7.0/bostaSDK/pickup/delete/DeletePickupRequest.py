
class DeletePickupRequest:
    def __init__(self, pickupId):
        """ Initialize new instance from DeletePickupRequest class

        Parameters:
        pickupId (str): Pickup Id

        Returns: instance from DeletePickupRequest

        """
        self._id = pickupId

    def get_pickupId(self):
        return self._id
