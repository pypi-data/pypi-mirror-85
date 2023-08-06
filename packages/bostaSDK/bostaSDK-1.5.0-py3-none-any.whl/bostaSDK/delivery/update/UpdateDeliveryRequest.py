import json

from bostaSDK.utils.Address import Address
from bostaSDK.utils.Receiver import Receiver


class UpdateDeliveryRequest:
    def __init__(
        self, deliveryId: int, receiver=None,
        pickUpAddress=None, dropOffAddress=None,
        returnAddress=None, notes=None,
        businessReference=None,
        webhookUrl=None, cod=None
    ):
        """ Initialize new instance from UpdateDeliveryRequest class

        Parameters:
        deliveryId (str): Delivery Id
        specs (DeliverySpecs)
        pickUpAddress (Address, optinal)
        dropOffAddress (Address, optinal)
        returnAddress (Address, optinal)
        cod (int, optinal): Cash on delivery amount
        receiver (Receiver, optinal)
        businessReference (str, optinal): Business refrence
        webhookUrl (str, optinal)

        Returns: instance from UpdateDeliveryRequest

        """
        self._id = deliveryId
        self.receiver = receiver
        self.pickUpAddress = pickUpAddress
        self.dropOffAddress = dropOffAddress
        self.returnAddress = returnAddress
        self.notes = notes
        self.businessReference = businessReference
        self.webhookUrl = webhookUrl
        self.cod = cod

    def get_deliveryId(self):
        return self._id

    def toJSONPayload(self):
        """
        Returns:
        JSON object from current instance

        """
        payload = {}
        if self.receiver is not None:
            payload['receiver'] = self.receiver.toJSON()
        if self.pickUpAddress is not None:
            payload['pickUpAddress'] = self.pickUpAddress.toJSON()
        if self.dropOffAddress is not None:
            payload['dropOffAddress'] = self.dropOffAddress.toJSON()
        if self.returnAddress is not None:
            payload['returnAddress'] = self.returnAddress.toJSON()
        if self.notes is not None:
            payload['notes'] = self.notes
        if self.businessReference is not None:
            payload['businessReference'] = self.businessReference
        if self.webhookUrl is not None:
            payload['webhookUrl'] = self.webhookUrl
        if self.cod is not None:
            payload['cod'] = self.cod
        return json.dumps(payload)
