import os 

from bostaSDK.apiClient import ApiClient
from bostaSDK.utils import ContactPerson
from bostaSDK.pickup import create, list, get, update, delete

apiKey = os.getenv("BOSTA-API-KEY")
baseUrl = os.getenv("BOSTA-BASE-URL")
apiClient = ApiClient(apiKey, baseUrl)

# Create New Pickup
newPickupId = apiClient.pickup.create(
    create.CreatePickupRequest(
     "Mon Nov 7 2020 00:00:00 GMT+0200", apiClient.pickupTimeSlots[0],
      ContactPerson ("m", "010193155997", "example@bosta.co")
    )
)

#List Pickups 
apiClient.pickup.listAll(list.ListAllPickupsRequest(2))

#Get Pickup 
apiClient.pickup.get(
    get.GetPickupDetailsRequest(newPickupId)
)

#Update Pickup 
apiClient.pickup.update(update.UpdatePickupRequest(
    newPickupId, contactPerson=ContactPerson ("user", "010193155922", "user@bosta.co")
))

#Delete Pickup
apiClient.pickup.delete(delete.DeletePickupRequest(newPickupId))