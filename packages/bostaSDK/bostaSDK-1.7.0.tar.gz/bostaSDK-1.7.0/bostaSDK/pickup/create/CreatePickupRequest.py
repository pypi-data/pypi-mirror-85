import json

from bostaSDK.utils.ContactPerson import ContactPerson


class CreatePickupRequest:

    def __init__(self, scheduledDate: str,
                 scheduledTimeSlot: str, contactPerson: ContactPerson,
                 businessId=None, businessLocationId=None,
                 warehouseId=None, noOfPackages=None, notes=None):
        """ Initialize new instance from CreatePickupRequest class

        Parameters:
        scheduledDate (str): Pickup scheduled date
        scheduledTimeSlot (str): "10:00 to 13:00" or "13:00 to 16:00"
        contactPerson (ContactPerson)
        businessId (str)
        businessLocationId (str)
        warehouseId (str)
        noOfPackages (int)
        notes (str)

        Returns: instance from CreatePickupRequest
        """

        self.businessId = businessId
        self.scheduledDate = scheduledDate
        self.scheduledTimeSlot = scheduledTimeSlot
        self.businessLocationId = businessLocationId
        self.contactPerson = contactPerson
        self.noOfPackages = noOfPackages
        self.notes = notes
        self.warehouseId = warehouseId

    def toJSONPayload(self):
        """
        Returns:
        JSON object from current instance

        """
        payload = {
            "scheduledDate": self.scheduledDate,
            "scheduledTimeSlot": self.scheduledTimeSlot,
            "contactPerson": self.contactPerson.toJSON(),
        }
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
