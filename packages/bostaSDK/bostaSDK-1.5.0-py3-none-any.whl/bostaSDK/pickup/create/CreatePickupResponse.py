

class CreatePickupResponse:

    def __init__(self, jsonResponseObj):
        """
        Initialize new instance from CreatePickupResponse class

        Parameters:
        jsonResponse (dict): JSON response object

        Returns:
        instance from CreatePickupResponse

        """
        self.fromJSONPayload(jsonResponseObj)

    def fromJSONPayload(self, responseObj):
        """
        Extract _id, puid, business, businessLocationId,
        scheduledDate, scheduledTimeSlot, contactPerson,
        createdAt and updatedAt fields from json response object

        Parameters:
        jsonResponse (dict): JSON response object
        """
        newPickup = responseObj["data"]
        self._id = newPickup["_id"]
        self.puid = newPickup["puid"]
        self.business = newPickup["business"]
        self.businessLocationId = newPickup["businessLocationId"]
        self.scheduledDate = newPickup["scheduledDate"]
        self.scheduledTimeSlot = newPickup["scheduledTimeSlot"]
        self.contactPerson = newPickup["contactPerson"]
        self.createdAt = newPickup["createdAt"]
        self.updatedAt = newPickup["updatedAt"]

    def __str__(self):
        return self._id
