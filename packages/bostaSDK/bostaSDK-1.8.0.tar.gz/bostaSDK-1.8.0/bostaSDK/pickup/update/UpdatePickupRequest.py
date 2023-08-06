import json


class UpdatePickupRequest:
    def __init__(
            self, _id, businessId=None, scheduledDate=None,
            scheduledTimeSlot=None, contactPerson=None,
            businessLocationId=None, warehouseId=None,
            noOfPackages=None, notes=None):
        """ Initialize new instance from UpdatePickupRequest class

        Parameters:
        _id (str): Pickup Id
        businessId (str)
        scheduledDate (str)
        scheduledTimeSlot (str)
        contactPerson (ContactPerson)
        businessLocationId (str)
        warehouseId (str)
        noOfPackages (str)
        notes (str)


        Returns: instance from UpdatePickupRequest

        """
        self._id = _id
        self.businessId = businessId
        self.scheduledDate = scheduledDate
        self.scheduledTimeSlot = scheduledTimeSlot
        self.businessLocationId = businessLocationId
        self.contactPerson = contactPerson
        self.noOfPackages = noOfPackages
        self.notes = notes
        self.warehouseId = warehouseId

    def get_id(self):
        return self._id

    def toJSONPayload(self):
        """
        Returns:
        JSON object from current instance

        """
        payload = {}
        if self.scheduledDate is not None:
            payload['scheduledDate'] = self.scheduledDate
        if self.scheduledTimeSlot is not None:
            payload['scheduledTimeSlot'] = self.scheduledTimeSlot
        if self.contactPerson is not None:
            payload['contactPerson'] = self.contactPerson.toJSON()
        if self.businessId is not None:
            payload['businessId'] = self.businessId
        if self.businessLocationId is not None:
            payload['businessLocationId'] = self.businessLocationId
        if self.noOfPackages is not None:
            payload['noOfPackages'] = self.noOfPackages
        if self.notes is not None:
            payload['notes'] = self.notes
        if self.warehouseId is not None:
            payload['warehouseId'] = self.warehouseId
        return json.dumps(payload)
