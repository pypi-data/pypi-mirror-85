

class GetPickupDetailsResponse:

    def __init__(self, res):
        """
        Initialize new instance from GetPickupDetailsResponse class

        Parameters:
        res (dict, str): JSON response object or response text message

        Returns:
        instance from GetPickupDetailsResponse

        """
        self.fromResponseObj(res)

    def fromResponseObj(self, res):
        """
        Extract _id, puid, business, businessLocationId,
        scheduledDate, scheduledTimeSlot, contactPerson,
        createdAt, deliveries, state, and tickets fields from json response object

        Parameters:
        res (dict, str): JSON response object or response text message
        """
        if type(res) is dict and res.get("data") is not None:

            pickup = res["data"]
            self._id = pickup["_id"]
            self.puid = pickup["puid"]
            self.business = pickup["business"]
            self.scheduledDate = pickup["scheduledDate"]
            self.scheduledTimeSlot = pickup["scheduledTimeSlot"]
            self.contactPerson = pickup["contactPerson"]
            self.businessLocationId = pickup["businessLocationId"]
            self.deliveries = pickup["deliveries"]
            self.state = pickup["state"]
            self.createdAt = pickup["createdAt"]
            self.tickets = pickup["tickets"]
        else:
            self.message = str(res)

    def __str__(self):
        return self._id or self.message
    def get_message(self):
        return self.message

