

class GetPickupDetailsResponse:

    def __init__(self, jsonResponse):
        """
        Initialize new instance from GetPickupDetailsResponse class

        Parameters:
        jsonResponse (dict): JSON response object

        Returns:
        instance from GetPickupDetailsResponse

        """
        self.fromJSONPayload(jsonResponse)

    def fromJSONPayload(self, jsonResponse):
        """
        Extract _id, puid, business, businessLocationId,
        scheduledDate, scheduledTimeSlot, contactPerson,
        createdAt, deliveries, state, and tickets fields from json response object

        Parameters:
        jsonResponse (dict): JSON response object
        """
        pickup = jsonResponse["data"]
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

    def __str__(self):
        return self._id
