import os

from bostaSDK.apiClient import ApiClient
from bostaSDK.delivery import list, create, update, track, printAWB, get, terminate
from bostaSDK.utils import Receiver, Address, ContactPerson

apiKey = os.getenv("BOSTA-API-KEY")
baseUrl = os.getenv("BOSTA-BASE-URL")

apiClient = ApiClient(apiKey, baseUrl)
deliveryTypes = apiClient.deliveyTypes

#List Deliveries 
apiClient.delivery.listAll(list.ListAllDeliveriesRequest(3,10))

#Create new delivery
reciever = Receiver("sohila", "Boghdady", "sohila_bogdady@hotmail.com", "01090055000")
dropOffAddress = Address("EG-01", "Maadi", "Maadi", "104")
createDeliveryReq = create.CreateDeliveryRequest(
    deliveryTypes['SEND']['code'], 100, dropOffAddress, reciever 
)
deliveryId = apiClient.delivery.create(createDeliveryReq)

#Print Airway Bill
apiClient.delivery.printAirWayBill(printAWB.PrintAWBRequest([deliveryId]))

#Track Delivery
apiClient.delivery.track(track.TrackDeliveryRequest(deliveryId))

#Get Delivery
apiClient.delivery.get(get.GetDeliveryDetailsRequest(deliveryId))

#Update Delivery
newReciever = Receiver("user", "test", "test@example.com", "01090055000")
apiClient.delivery.update(update.UpdateDeliveryRequest(deliveryId, receiver = newReciever, cod=120))

#Terminate Delivery
apiClient.delivery.terminate(terminate.TerminateDeliveryRequest(deliveryId))