

class CreatePickupResponse:

    def __init__(self, res):
        """
        Initialize new instance from CreatePickupResponse class

        Parameters:
        res (dict, str): JSON response object or response text message

        Returns:
        instance from CreatePickupResponse

        """
        self.fromResponseObj(res)

    def fromResponseObj(self, res):
        """
        Extract _id, puid, business, businessLocationId,
        scheduledDate, scheduledTimeSlot, contactPerson,
        createdAt and updatedAt fields from json response object

        Parameters:
        res (dict, str): JSON response object or response text message
        """
        if type(res) is dict and res.get('data') is not None:
            self.message = res.get("message")
            newPickup = res["data"]
            self._id = newPickup["_id"]
            self.puid = newPickup["puid"]
            self.business = newPickup["business"]
            self.businessLocationId = newPickup["businessLocationId"]
            self.scheduledDate = newPickup["scheduledDate"]
            self.scheduledTimeSlot = newPickup["scheduledTimeSlot"]
            self.contactPerson = newPickup["contactPerson"]
            self.createdAt = newPickup["createdAt"]
            self.updatedAt = newPickup["updatedAt"]
        else:
            self.message = str(res)

    def __str__(self):
        return self.message
    
    def get_pickupId(self):
        return self._id

    def get_message(self):
        return self.message
    
