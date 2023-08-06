import json

from bostaSDK.utils.Address import Address
from bostaSDK.utils.Receiver import Receiver
from bostaSDK.utils.DeliverySpecs import DeliverySpecs


class CreateDeliveryRequest:

    def __init__(
        self, deliveryType, cod,
        dropOffAddress: Address, receiver: Receiver,
        deliverySpecs=None, notes=None,
        businessReference=None,
        ):
        """ Initialize new instance from CreateDeliveryRequest class

        Parameters:
        deliveryType (int)
        cod (int): Cash on delivery amount
        dropOffAddress (Address)
        cashOnDelivery (int): Cash on delivery amount
        receiver (Receiver)
        deliverySpecs (DeliverySpecs)
        notes (str)
        businessReference (str)

        Returns: instance from CreateDeliveryRequest

        """
        self.type = deliveryType
        self.cod = cod
        self.dropOffAddress = dropOffAddress
        self.receiver = receiver

    def toJSONPayload(self):
        """
        Returns:
        JSON object from current instance

        """
        return json.dumps({
            "type": self.type,
            "cod": self.cod,
            "dropOffAddress": self.dropOffAddress.toJSON(),
            "receiver": self.receiver.toJSON()
        })
